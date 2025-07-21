import pandas as pd

def cleanse_data(file_path):
    xls = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")

    # Strip whitespace from column names
    for sheet_name, df in xls.items():
        df.columns = [col.strip() for col in df.columns]
        xls[sheet_name] = df

    # Clean 'orders' sheet
    orders = xls["orders"]
    for col in orders.columns:
        if orders[col].dtype == "object":
            orders[col] = orders[col].astype(str).str.strip()
    orders["latitude"] = pd.to_numeric(orders["latitude"], errors="coerce")
    orders["longitude"] = pd.to_numeric(orders["longitude"], errors="coerce")
    orders["orders"] = pd.to_numeric(orders["orders"], errors="coerce")
    xls["orders"] = orders

    # Clean 'vehicles' sheet
    vehicles = xls["vehicles"]
    for col in vehicles.columns:
        if vehicles[col].dtype == "object":
            vehicles[col] = vehicles[col].astype(str).str.strip()
    vehicles["size"] = vehicles["size"].astype(str).str.strip()
    vehicles["weight"] = pd.to_numeric(vehicles["weight"], errors="coerce")
    xls["vehicles"] = vehicles

    return xls
