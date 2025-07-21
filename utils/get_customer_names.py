import pandas as pd


def get_customer_names(file_path):
    try:
        dp = pd.read_excel(file_path, sheet_name="orders")
        name = dp["name"].tolist()
        name.append("depot")
        name.insert( 0,"start")
        return True, name
    except Exception as e:
        err_msg = "Error reading customer name from file: {e}"
        return False, err_msg
