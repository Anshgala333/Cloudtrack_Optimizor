
from config.constants import BOX_LENGTH , BOX_WIDTH , BOX_HEIGHT , BOX_VOLUME
import math
import json



def get_beautified_output(truck_fleet):
    beautified = {"total_trucks_used": 0, "trucks": []}
    truck_num = 1
    
    for truck in truck_fleet["message"]:
        if not truck["boxes"]:
            continue

        positioned_boxes = []
        max_x, max_y, max_z = truck["width"], truck["length"], truck["height"]

        # Sort boxes by priority (lower number = higher priority)
        sorted_boxes = sorted(
            truck["boxes"], key=lambda b: b.get("priority", float("inf")), reverse=True
        )
        
            
        box_index = 0
        total_boxes = len(sorted_boxes)
        
        box_per_floor = math.floor(truck["length"] / BOX_LENGTH) * math.floor(truck["width"] / BOX_WIDTH)   
        total_floors = truck["height"] // BOX_HEIGHT
        height_of_one_floor = truck["height"] / total_floors
        total_required_floor = math.ceil(total_boxes / box_per_floor)
        final_height = total_required_floor * height_of_one_floor
        
        max_z = final_height
        
        y = 0.0
        while round(y + BOX_LENGTH, 2) <= round(max_y, 2):
            z = 0.0
            while round(z + BOX_HEIGHT, 2) <= round(max_z, 2):
                x = 0.0
                while round(x + BOX_WIDTH, 2) <= round(max_x, 2):
                    if box_index >= total_boxes:
                        break
                    box = sorted_boxes[box_index]
                    positioned_boxes.append(
                        {
                            "custom_id": f"{box['customer_name']}#{box['box_number']}",
                            "customer_name": box["customer_name"],
                            "box_number": box["box_number"],
                            "priority": box.get("priority", None),
                            "weight": round(box["weight"], 2),
                            "position": {
                                "x": round(x, 2),
                                "y": round(y, 2),
                                "z": round(z, 2),
                            },
                        }
                    )
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
            "length" : truck["length"],
            "width" : truck["width"],
            "height" : truck["height"],
            "max_weight": round(truck["max_weight"], 2),
            "used_weight": round(truck["weight"], 2),
            "occupied_weight": f"{round(weight_percent, 2)}%",
            "volume": f"{round(truck['volume'], 2)} cubic meter",
            "occupied_volume": f"{round(volume_percent, 2)}%",
            "total_boxes": len(positioned_boxes),
            "boxes": positioned_boxes,
            "maximum_capacity":truck["maximum_capacity"],
            "path" : truck["path"],
            "total_distance" : truck["total_distance"]
        }
        beautified["trucks"].append(truck_info)
        truck_num += 1
        
    beautified["total_trucks_used"] = len(beautified["trucks"])
    
    with open("final.json" , "w") as f:
        json.dump(beautified , f , indent=4)
    return beautified