import pandas as pd
import math
from config.constants import BOX_LENGTH, BOX_WIDTH, BOX_HEIGHT, BOX_WEIGHT

def get_truck_types(file_path) -> dict:
    
    df = pd.read_excel(file_path , sheet_name="vehicles")
    grouped_data = []

    # Round dimensions to avoid float precision noise
    df["length"] = df["length"].round(3)
    df["width"] = df["width"].round(3)
    df["height"] = df["height"].round(3)

    
    def calculate_max_capacity(length, width, height):
        return (
            math.floor(length / BOX_LENGTH)
            * math.floor(width / BOX_WIDTH)
            * math.floor(height / BOX_HEIGHT)
        )
    grouped_df = df.groupby(["length", "width", "height"])

    for idx, ((length, width, height), group) in enumerate(grouped_df):
        first_row = group.iloc[0]
        truck_obj = {
            "type_index": int(idx),
            "name": f"{first_row["name"]}- {first_row["size"]} Truck",
            "length": float(length),
            "width": float(width),
            "height": float(height),
            "volume": round(float(length * width * height), 5),
            "max_weight": int(first_row["weight"]),
            "maximum_capacity": int(calculate_max_capacity(length,width,height)),
            "count": int(len(group))
        }

        grouped_data.append(truck_obj)

    return {
        "total_vehicles": int(len(df)),
        "groups": grouped_data
    }
