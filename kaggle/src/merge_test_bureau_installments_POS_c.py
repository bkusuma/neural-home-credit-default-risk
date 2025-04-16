def merge_test_bureau_installments_POS_credit(train_or_test_path, [bureau_path, bureau_balance_path], installments_path, POS_CASH_balance_path, credit_card_balance_path):
    # First our imports
    import pandas as pd
    # Then merge in bureau data
    application = pd.read_csv(train_or_test_path)
    bureau = pd.read_csv(input_path + "bureau.csv")
    bureau_balance = pd.read_csv(input_path + "bureau_balance.csv")
    bureau_loans_and_balances = pd.merge(bureau, bureau_balance, how="left", on="SK_ID_BUREAU")
    application = pd.merge(application, bureau_loans_and_balances, how="left", on="SK_ID_CURR")
    # drop unnecessary index
    bureau_loans_and_balances.drop(columns="SK_ID_BUREAU", inplace=True)
    # recode STATUS using CREDIT_ACTIVE information and drop CREDIT_ACTIVE
    bureau_loans_and_balances.loc[(bureau_loans_and_balances["STATUS"].isna()) & 
                              (bureau_loans_and_balances["CREDIT_ACTIVE"] == "Closed"),
                              "STATUS"] = "C"
    bureau_loans_and_balances.loc[(bureau_loans_and_balances["STATUS"].isna()) & 
                                (bureau_loans_and_balances["CREDIT_ACTIVE"] == "Active"),
                                "STATUS"] = "0"
    bureau_loans_and_balances.loc[(bureau_loans_and_balances["STATUS"].isna()) & 
                                (bureau_loans_and_balances["CREDIT_ACTIVE"] == "Sold"),
                                "STATUS"] = "5"
    bureau_loans_and_balances.loc[(bureau_loans_and_balances["STATUS"].isna()) & 
                                (bureau_loans_and_balances["CREDIT_ACTIVE"] == "Bad debt"),
                                "STATUS"] = "5"
    bureau_loans_and_balances.drop(columns="CREDIT_ACTIVE", inplace=True)



test_data_file = "application_test.csv"
application_test = pd.read_csv(input_path + test_data_file)

bureau_loans_and_balances = pd.read_csv(lib_path + "bureau_loans_and_balances.csv")

installments_payments = pd.read_csv(input_path + "installments_payments.csv")
POS_CASH_balance = pd.read_csv(input_path + "POS_CASH_balance.csv")
credit_card_balance = pd.read_csv(input_path + "credit_card_balance.csv")

application_test = pd.merge(application_test, bureau_loans_and_balances, how="left", on="SK_ID_CURR")

idx = pd.DataFrame(application_test['SK_ID_CURR'])

# INSTALL steps
installments_payments.drop(columns="SK_ID_PREV", inplace=True)
installments_payments.columns = [col + "_INSTALL" for col in installments_payments.columns]
merge_INSTALL = pd.merge(idx, installments_payments, how="inner", left_on="SK_ID_CURR", right_on="SK_ID_CURR_INSTALL")
merge_INSTALL.drop(columns="SK_ID_CURR_INSTALL", inplace=True)
merge_INSTALL = merge_INSTALL.sort_values(by="NUM_INSTALMENT_NUMBER_INSTALL", ascending=False).drop_duplicates(subset=["SK_ID_CURR"])

# POS steps
POS_CASH_balance.drop(columns="SK_ID_PREV", inplace=True)
POS_CASH_balance.columns = [col + "_POS" for col in POS_CASH_balance.columns]
merge_POS = pd.merge(idx, POS_CASH_balance, how="inner", left_on="SK_ID_CURR", right_on="SK_ID_CURR_POS")
merge_POS.drop(columns="SK_ID_CURR_POS", inplace=True)
merge_POS = merge_POS.sort_values(by="MONTHS_BALANCE_POS", ascending=False).drop_duplicates(subset=["SK_ID_CURR"])

# CC step
credit_card_balance.drop(columns="SK_ID_PREV", inplace=True)
credit_card_balance.columns = [col + "_CC" for col in credit_card_balance.columns]
merge_CC = pd.merge(idx, credit_card_balance, how="inner", left_on="SK_ID_CURR", right_on="SK_ID_CURR_CC")
merge_CC.drop(columns="SK_ID_CURR_CC", inplace=True)
merge_CC = merge_CC.sort_values(by="MONTHS_BALANCE_CC", ascending=False).drop_duplicates(subset=["SK_ID_CURR"])

# Merge down filtered data
balances_and_payments = pd.merge(merge_INSTALL, merge_POS, how="outer", left_on="SK_ID_CURR", right_on="SK_ID_CURR")
balances_and_payments = pd.merge(balances_and_payments, merge_CC, how="outer", left_on="SK_ID_CURR", right_on="SK_ID_CURR")

# Drop object columns
# balances_and_payments.select_dtypes(include="object")
balances_and_payments.drop(labels=["NAME_CONTRACT_STATUS_POS", "NAME_CONTRACT_STATUS_CC"], axis=1, inplace=True)

# Merge down onto test file
application_test = pd.merge(application_test, balances_and_payments, how="left", on="SK_ID_CURR")

# pop off index ids
ids = application_test.pop("SK_ID_CURR")

# transform data
application_test = preprocessor.transform(application_test)

# drop columns with collinear relationships (Pearson's correlation coefficients > 0.8)
application_test.drop(columns=non_co_cols, inplace=True)