def eval_regression(model, X_train, y_train, name='model'):
    """Evaluate and calculate various regression metrics for a given model.
    
    This function takes a trained regression model, training data features (X_train),  and training data targets (y_train).
    It calculates several key performance metrics  including Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean
    Squared Error (RMSE), Mean Absolute Percentage Error (MAPE), R2 Score, and Adjusted R2 Score. The results are returned
    in a pandas DataFrame with the specified model name as the index.
    
    Args:
        model (object): A trained regression model.
        X_train (array-like): Training data features.
        y_train (array-like): Training data targets.
        name (str?): Name of the model for the results DataFrame. Defaults to 'model'.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the calculated metrics.
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error, root_mean_squared_error
    import pandas as pd
    
    def adj_r2(r2, x):
        """Calculate the adjusted R-squared value.
        
        The adjusted R-squared is a modified version of R-squared that adjusts for the number of predictors in the model. It
        provides a more accurate measure of goodness of fit when comparing models with different numbers of predictors.
        
        Args:
            r2 (float): The coefficient of determination (R-squared) value.
            x (np.ndarray): An array of predictor variables.
        
        Returns:
            float: The adjusted R-squared value.
        """
        n = x.shape[0]
        p = x.shape[1]
        return 1 - (((n - 1) / (n - p  - 1)) * (1 - r2))

    train_pred = model.predict(X_train)
    MAPE = mean_absolute_percentage_error(y_train, train_pred)
    r2 = r2_score(y_train, train_pred)
    RMSE = root_mean_squared_error(y_train, train_pred)
    MSE = mean_squared_error(y_train, train_pred)
    MAE = mean_absolute_error(y_train, train_pred)
    a_r2 = adj_r2(r2, X_train)
    metrics = ["MAE", "MSE", "RMSE", "MAPE", "R2", "Adjusted R2"]
    results = pd.DataFrame(columns=metrics, index=[name])
    results['MAE'] = [MAE]
    results['MSE'] = [MSE]
    results['RMSE'] = RMSE
    results['MAPE'] = MAPE
    results['R2'] = r2
    results['Adjusted R2'] = a_r2
    return results