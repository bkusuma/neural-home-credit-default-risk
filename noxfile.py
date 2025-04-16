from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()

nox.needs_version = ">=2024.3.2"
nox.options.sessions = ["lint", "pylint", "tests"]
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session
def lint(session: nox.Session) -> None:
    """Run the linter.
    
    This function sets up a Nox session and runs the pre-commit linter on all files, showing a diff if any changes are made.
    """
    session.install("pre-commit")
    session.run(
        "pre-commit", "run", "--all-files", "--show-diff-on-failure", *session.posargs
    )


@nox.session
def pylint(session: nox.Session) -> None:
    # This needs to be installed into the package environment, and is slower
    # than a pre-commit check
    """Run Pylint.
    
    This function sets up and runs Pylint on a specified package or module. It installs Pylint as a development dependency
    if it's not already installed, ensuring that the environment is prepared before running the linter. The function takes
    an optional list of positional arguments which can be used to pass additional options to Pylint.
    
    Args:
        session (nox.Session): The current nox session context.
    """
    session.install("-e.", "pylint>=3.2")
    session.run("pylint", "neural_home_credit_default_risk", *session.posargs)


@nox.session
def tests(session: nox.Session) -> None:
    """Run the unit and regular tests.
    
    This function sets up a nox session to install test dependencies and run pytest with any positional arguments provided.
    
    Args:
        session (nox.Session): The nox session object used to manage the environment and run commands.
    """
    session.install("-e.[test]")
    session.run("pytest", *session.posargs)


@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:

    """Build the documentation for a project.
    
    This function sets up the Sphinx build environment and generates the documentation in the specified format (default is
    HTML). If the `--non-interactive` flag is not provided, it will start a live-reloading server to automatically update
    the docs when changes are made.
    
    Args:
        session (nox.Session): The Nox session object containing configuration for the current run.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", dest="builder", default="html", help="Build target (default: html)"
    )
    parser.add_argument("output", nargs="?", help="Output directory")
    args, posargs = parser.parse_known_args(session.posargs)
    serve = args.builder == "html" and session.interactive

    session.install("-e.[docs]", "sphinx-autobuild")

    shared_args = (
        "-n",  # nitpicky mode
        "-T",  # full tracebacks
        f"-b={args.builder}",
        "docs",
        args.output or f"docs/_build/{args.builder}",
        *posargs,
    )

    if serve:
        session.run("sphinx-autobuild", "--open-browser", *shared_args)
    else:
        session.run("sphinx-build", "--keep-going", *shared_args)


@nox.session
def build_api_docs(session: nox.Session) -> None:

    """Build (regenerate) API docs.
    
    This function uses Sphinx to generate API documentation for the neural_home_credit_default_risk module. It installs the
    necessary dependencies and then runs sphinx-apidoc to create the documentation in the docs/api/ directory.
    """
    session.install("sphinx")
    session.run(
        "sphinx-apidoc",
        "-o",
        "docs/api/",
        "--module-first",
        "--no-toc",
        "--force",
        "src/neural_home_credit_default_risk",
    )


@nox.session
def build(session: nox.Session) -> None:

    """Build an SDist and wheel.
    
    This function creates a source distribution (SDist) and wheel package for the project using the `build` tool. It first
    checks if a build directory exists and removes it if present to ensure a clean build environment. Then, it installs the
    `build` package and runs the `python -m build` command to generate the distribution files.
    """
    build_path = DIR.joinpath("build")
    if build_path.exists():
        shutil.rmtree(build_path)

    session.install("build")
    session.run("python", "-m", "build")
