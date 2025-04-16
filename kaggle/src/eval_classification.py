def eval_classification(model, X_train, y_train, X_test, y_test, model_name="model", results_frame=None,
                        pos_label=1, average="binary", roc_auc_average="macro"):
    
    from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                                 f1_score, classification_report, ConfusionMatrixDisplay, 
                                 roc_auc_score)
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # make predictions
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    # create function to print classification reports (which are strings) side by side
    def side_by_side(strings, size=54, space=1):
        strings = list(strings)
        result = []

        while any(strings):
            line = []

            for i, s in enumerate(strings):
                buf = s[:size]
                
                try:
                    n = buf.index("\n")
                    line.append(buf[:n].ljust(size))
                    strings[i] = s[n+1:]
                except ValueError:
                    line.append(buf.ljust(size))
                    strings[i] = s[size:]

            result.append((" " * space).join(line))
        
        return "\n".join(result)
    
    # set up report strings with titles
    s1 = " "*20 + "Train Evaluation" + "\n" + classification_report(y_train, train_pred)
    s2 = " "*20 + "Test Evaluation" + "\n" + classification_report(y_test, test_pred)
    print(side_by_side([s1, s2]))
    
    # print confusion matrices side by side
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))
    ConfusionMatrixDisplay.from_predictions(y_train, train_pred, normalize="true", cmap="Blues", ax=ax1,  display_labels=["Non-Defaulter", "Defaulter"],)
    ConfusionMatrixDisplay.from_predictions(y_test, test_pred, normalize="true", cmap="Greens", ax=ax2, display_labels=["Non-Defaulter", "Defaulter"])
    plt.tight_layout()  
    plt.show()

    # collect score results in data frame
    results = pd.DataFrame(index=[model_name])
    results["train_acc"] = accuracy_score(y_train, train_pred)
    results["test_acc"] = accuracy_score(y_test, test_pred)
    results["train_prec"] = precision_score(y_train, train_pred, pos_label=pos_label, average=average)
    results["test_prec"] = precision_score(y_test, test_pred, pos_label=pos_label, average=average)
    results["train_recall"] = recall_score(y_train, train_pred, pos_label=pos_label, average=average)
    results["test_recall"] = recall_score(y_test, test_pred, pos_label=pos_label, average=average)
    results["train_f1"] = f1_score(y_train, train_pred, pos_label=pos_label, average=average)
    results["test_f1"] = f1_score(y_test, test_pred, pos_label=pos_label, average=average)
    results["train_auc"] = roc_auc_score(y_train, model.predict_proba(X_train)[:, 1], multi_class="ovr", average=roc_auc_average)
    results["test_auc"] = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1], multi_class="ovr", average=roc_auc_average)  

    if results_frame is not None:
        results = pd.concat([results_frame, results])
 
    return results