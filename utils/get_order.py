import pandas as pd

def get_order(file_path):
   try:
        df = pd.read_excel(file_path, sheet_name="orders")
        orders = df['orders'].tolist()
        orders.append(0)
        orders.insert(0,0)
        return True,orders
   except Exception as e:
        err_msg = "Error reading orders from file: {e}"
        return False,err_msg
