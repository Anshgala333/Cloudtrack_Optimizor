# import pandas as pd
# from geopy.geocoders import Nominatim
# import time
# import re

# # Step 1: Read and clean
# df = pd.read_csv("proper.csv")
# df.columns = df.columns.str.strip()
# df["Location"] = df["Location"].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()

# # Step 2: Extract last part (e.g., City, State, Pincode)
# def extract_simple_address(full_address):
#     match = re.search(r"([A-Za-z\s]+,\s*[A-Za-z\s]+,\s*\d{6})$", full_address)
#     return match.group(1).strip() if match else None

# df["CleanLocation"] = df["Location"].apply(extract_simple_address)

# # Step 3: Geocode CleanLocation instead
# geolocator = Nominatim(user_agent="my_geocoder")
# coordinates = []

# for loc in df["CleanLocation"]:
#     try:
#         if loc:
#             location = geolocator.geocode(loc)
#             if location:
#                 coordinates.append((location.latitude, location.longitude))
#                 print(f"✓ {loc} → ({location.latitude}, {location.longitude})")
#             else:
#                 coordinates.append((None, None))
#                 print(f"✗ Not found: {loc}")
#         else:
#             coordinates.append((None, None))
#     except Exception as e:
#         coordinates.append((None, None))
#         print(f"⚠️ Error: {loc} → {e}")
#     time.sleep(1)

# df["Coordinates"] = coordinates

# # Filter valid
# valid_df = df[df["Coordinates"].apply(lambda x: None not in x)]
# coordinates = valid_df["Coordinates"].tolist()
# demands = valid_df["Demands"].tolist()

# print("\nFinal coordinates =", coordinates)
# print("Final demands =", demands)
#  -------------------------------------------------------------------


import requests
import time

# API_KEY = 'YOUR_API_KEY'




locations = [
    (23.8181266, 91.4363791),
    (24.8225239, 92.7992084),
    (24.8233218, 92.7997473),
    (25.5772264, 91.8808823),
    (26.1580185, 91.68392),
    (26.7220932, 88.4269844),
    (26.3314809, 91.00615359999999),
    (26.485398, 90.969973),
    (26.448852, 91.4434068),
    (26.1794295, 91.7510671),
    (26.4811277, 90.5546827),
    (27.1018582, 93.6296564),
    (27.5328572, 95.3239723),
    (26.6203447, 92.796111),
    (26.7501438, 94.2162345),
    (25.8441997, 93.44019109999999),
    (28.5422399, 77.3870653),
    (28.4670434, 77.2874178),
    (28.3815904, 79.4343011),
    (28.336572, 79.4197497),
    (28.0312306, 79.1271625),
    (27.5781833, 81.5990577),
    (27.565208, 80.6770261),
    (27.4371035, 82.1692972),
    (28.7900278, 79.0215474),
    (27.9496461, 80.7759251),
    (27.1331673, 81.96911279999999),
    (27.3877771, 80.13464479999999),
    (26.909252, 80.95658379999999),
    (26.4234824, 80.3916122),
    (26.7778797, 80.94301720000001),
    (26.815645, 80.904569),
    (26.897038, 80.9374154),
    (26.8809621, 81.0397476),
    (26.9265214, 80.94299749999999),
    (26.2144806, 81.25281389999999),
    # (23.2584857, 77.401989),  # added on purpose to end here this is bhopal
    # (28.0937702,94.5921326),  
]



def get_distance_matrix(locations):
    n = len(locations)
    matrix = [[0]*n for _ in range(n)]

    for i in range(0, n, 10):  # origins batch (max 10)
        origin_batch = locations[i:i+10]

        for j in range(0, n, 10):  # destinations batch (max 10)
            dest_batch = locations[j:j+10]

            origins_str = '|'.join(origin_batch)
            destinations_str = '|'.join(dest_batch)

            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins_str}&destinations={destinations_str}&key={API_KEY}"

            response = requests.get(url)
            result = response.json()
            print(f"{result} \n\n\n\n")

            # Fill matrix
            for oi, row in enumerate(result['rows']):
                for di, element in enumerate(row['elements']):
                    distance = element['distance']['value'] if element['status'] == 'OK' else float('inf')
                    matrix[i+oi][j+di] = distance

            time.sleep(10)  # Respect rat limit
    return matrix

