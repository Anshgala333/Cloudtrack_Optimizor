import pandas as pd
import json
from collections import defaultdict
import time
import math

# Constants
BOX_LENGTH = 0.46
BOX_WIDTH = 0.46
BOX_HEIGHT = 0.41
BOX_VOLUME = BOX_LENGTH * BOX_WIDTH * BOX_HEIGHT

# Truck definitions with count
TRUCKS = [
    {"name": "12-ft Truck", "length": 3.66, "width": 2.0, "height": 2.0, "max_weight": 3000, "count": 20},
    {"name": "24-ft Truck", "length": 7.32, "width": 2.44, "height": 2.6, "max_weight": 8000, "count": 20},
    {"name": "32-ft Truck", "length": 9.75, "width": 2.44, "height": 2.6, "max_weight": 10000, "count": 20}
]
def calculate_max_capacity(length, width, height):
    return (
        math.floor(length / BOX_LENGTH) *
        math.floor(width / BOX_WIDTH) *
        math.floor(height / BOX_HEIGHT)
    )
for truck in TRUCKS:
    truck["maximum_capacity"] = calculate_max_capacity(
        truck["length"], truck["width"], truck["height"]
    )
def beautify_truck_data(truck_fleet):
    beautified = {
        "total_trucks_used": 0,
        "trucks": []
    }

    truck_num = 1
    for truck in truck_fleet:
        if not truck["boxes"]:
            continue

        positioned_boxes = []
        max_x, max_y, max_z = truck['width'], truck['length'], truck['height']

        # Sort boxes by priority (lower number = higher priority)
        sorted_boxes = sorted(truck["boxes"], key=lambda b: b.get("priority", float('inf')), reverse=True)

        box_index = 0
        total_boxes = len(sorted_boxes)

        y = 0.0
        while round(y + BOX_LENGTH, 2) <= round(max_y, 2):
            z = 0.0
            while round(z + BOX_HEIGHT, 2) <= round(max_z, 2):
                x = 0.0
                while round(x + BOX_WIDTH, 2) <= round(max_x, 2):
                    if box_index >= total_boxes:
                        break
                    box = sorted_boxes[box_index]
                    positioned_boxes.append({
                        "custom_id": f"{box['customer_name']}#{box['box_number']}",
                        "customer_name": box['customer_name'],
                        "box_number": box['box_number'],
                        "priority": box.get("priority", None),
                        "weight": round(box["weight"], 2),
                        "position": {
                            "x": round(x, 2),
                            "y": round(y, 2),
                            "z": round(z, 2)
                        }
                    })
                    box_index += 1
                    x += BOX_WIDTH
                z += BOX_HEIGHT
            y += BOX_LENGTH

        volume_used = len(positioned_boxes) * BOX_VOLUME
        volume_percent = (volume_used / truck["volume"]) * 100
        weight_percent = (truck["weight"] / truck["max_weight"]) * 100

        truck_info = {
            "truck_number": truck_num,
            "name": truck["name"],
            "max_weight": round(truck["max_weight"], 2),
            "used_weight": round(truck["weight"], 2),
            "occupied_volume": f"{round(volume_percent, 2)}%",
            "occupied_weight": f"{round(weight_percent, 2)}%",
            "volume": f"{round(truck['volume'], 2)} cubic meter",
            "total_boxes": len(positioned_boxes),
            "boxes": positioned_boxes
        }

        beautified["trucks"].append(truck_info)
        truck_num += 1

    beautified["total_trucks_used"] = len(beautified["trucks"])
    return beautified

def group_unplaced_by_customer(unplaced):
    customer_map = defaultdict(list)
    for box in unplaced:
        customer_map[box['customer_name']].append({
            "box_number": box['box_number'],
            "weight": round(box['weight'], 2),
            "priority": box.get("priority", None)
        })
    return dict(customer_map)

def pack_trucks_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df['box_number'] = df.groupby('customer_name').cumcount() + 1
    df = df.sort_values(by='priority', ascending=True)
    boxes = df.to_dict('records')

    truck_fleet = []
    for truck_idx, truck_def in enumerate(TRUCKS):
        truck_volume = truck_def['length'] * truck_def['width'] * truck_def['height']
        for _ in range(truck_def.get('count', 0)):
            truck_fleet.append({
                'type_index': truck_idx,
                'name': truck_def['name'],
                'length': truck_def['length'],
                'width': truck_def['width'],
                'height': truck_def['height'],
                'volume': truck_volume,
                'max_weight': truck_def['max_weight'],
                'boxes': [],
                'weight': 0.0,
                "maximum_capacity" : truck_def["maximum_capacity"] 
            })

    truck_fleet.sort(key=lambda x: (x['max_weight'], x['volume']), reverse=True)

    unplaced_boxes = []

    for box in boxes:
        placed = False
        for truck in truck_fleet:
            maxCapacity = truck["maximum_capacity"]
            if(len(truck["boxes"]) == maxCapacity):continue
            used_volume = len(truck['boxes']) * BOX_VOLUME
            if (used_volume + BOX_VOLUME <= truck['volume']) and (truck['weight'] + box['weight'] <= truck['max_weight']):
                truck['boxes'].append(box)
                truck['weight'] += box['weight']
                placed = True
                break

        if not placed:
            # print(f"❌ Cannot assign box {box['customer_name']} - Box {box['box_number']} ({box['weight']}kg). All trucks full.")
            unplaced_boxes.append(box)

    structured_output = beautify_truck_data(truck_fleet)
    structured_output["not_placed"] = group_unplaced_by_customer(unplaced_boxes)

    # print(json.dumps(structured_output, indent=3))
    return structured_output




# pack_trucks_from_csv(csv_file_path= "../uploads/1750513113.5196495_main.csv")
# pack_trucks_from_csv(csv_file_path= "../uploads/test2.csv")
# pack_trucks_from_csv(csv_file_path= "../uploads/test3.csv")
# pack_trucks_from_csv(csv_file_path= "../uploads/test4.csv")
start = time.time()
# pack_trucks_from_csv(csv_file_path= "../uploads/test5.csv")
print(time.time()-start)

# pack_trucks_from_csv(csv_file_path= "../uploads/test6.csv")