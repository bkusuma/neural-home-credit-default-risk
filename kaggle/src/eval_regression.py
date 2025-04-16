def eval_regression(model, X_train, y_train, name='model'):
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error, root_mean_squared_error
    import pandas as pd
    
    def adj_r2(r2, x):
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