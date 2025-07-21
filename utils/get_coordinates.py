import pandas as pd

def get_coordinates(file_path):
    try:
        df = pd.read_excel(file_path , sheet_name="orders")
        arr = list(df[["latitude" , "longitude"]].itertuples(index=False , name=None))
        
        # adjustments
        start = arr[0] # act as a depot
        end = arr[-1] # act as a end point **
        arr.insert(0 , start)
        arr.append(end)
        
        
        return True,arr
    except Exception as e:
        msg = "Error reading orders from file: {e}"
        return False , msg
