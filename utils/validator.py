import pandas as pd

REQUIRED_SHEET_ORDERS = "orders"
REQUIRED_COLUMNS_ORDERS = ["name", "latitude", "longitude", "orders", "location"]
NUMERIC_COLUMNS_ORDERS = ["latitude", "longitude", "orders"]

REQUIRED_SHEET_VEHICLES = "vehicles"
REQUIRED_COLUMNS_VEHICLES = ["size", "name", "weight", "length", "width", "height"]
NUMERIC_COLUMNS_VEHICLES = ["weight", "length", "width", "height"]

def validate(file_path: str) -> tuple[bool, str]:
    try:
        # Load all sheets
        xls = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")

        # Check required sheets
        for sheet in [REQUIRED_SHEET_ORDERS, REQUIRED_SHEET_VEHICLES]:
            if sheet not in xls:
                return False, f"Sheet '{sheet}' is missing."

        # ===== ORDERS SHEET VALIDATION =====
        df_orders = xls[REQUIRED_SHEET_ORDERS]

        for col in REQUIRED_COLUMNS_ORDERS:
            if col not in df_orders.columns:
                return False, f"Column '{col}' is missing in '{REQUIRED_SHEET_ORDERS}' sheet."

        for idx, row in df_orders.iterrows():
            row_num = idx + 2
            for col in REQUIRED_COLUMNS_ORDERS:
                if pd.isna(row[col]):
                    return False, f"Missing value in column '{col}' at row {row_num} in '{REQUIRED_SHEET_ORDERS}' sheet."
            for col in NUMERIC_COLUMNS_ORDERS:
                if not isinstance(row[col], (int, float)):
                    return False, f"Value in column '{col}' at row {row_num} in '{REQUIRED_SHEET_ORDERS}' must be a number. Found: '{row[col]}'"

        # ===== VEHICLES SHEET VALIDATION =====
        df_vehicles = xls[REQUIRED_SHEET_VEHICLES]

        for col in REQUIRED_COLUMNS_VEHICLES:
            if col not in df_vehicles.columns:
                return False, f"Column '{col}' is missing in '{REQUIRED_SHEET_VEHICLES}' sheet."

        for idx, row in df_vehicles.iterrows():
            row_num = idx + 2
            for col in REQUIRED_COLUMNS_VEHICLES:
                if pd.isna(row[col]):
                    return False, f"Missing value in column '{col}' at row {row_num} in '{REQUIRED_SHEET_VEHICLES}' sheet."
            for col in NUMERIC_COLUMNS_VEHICLES:
                if not isinstance(row[col], (int, float)):
                    return False, f"Value in column '{col}' at row {row_num} in '{REQUIRED_SHEET_VEHICLES}' must be a number. Found: '{row[col]}'"

        return True, "Excel file is valid."

    except Exception as e:
        return False, f"Error reading file: {str(e)}"
