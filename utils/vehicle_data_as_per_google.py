def vehicle_details_as_per_google(truck_types):
    data = {"vehicle_capacities": [], "num_vehicles": 0}

    vehicle_info_list = []
    for group in truck_types["groups"]:
        for _ in range(group["count"]):
            # Append capacity
            data["vehicle_capacities"].append(group["maximum_capacity"])

            # Append detailed info
            vehicle_info_list.append(
                {
                    "type_index": group["type_index"],
                    "name": group["name"],
                    "length": group["length"],
                    "width": group["width"],
                    "height": group["height"],
                    "volume": group["volume"],
                    "max_weight": group["max_weight"],
                    "maximum_capacity": group["maximum_capacity"],
                }
            )

    # Final vehicle count
    data["num_vehicles"] = len(data["vehicle_capacities"])
    
    return data , vehicle_info_list