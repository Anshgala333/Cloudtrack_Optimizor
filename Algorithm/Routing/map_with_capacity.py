from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.distance import geodesic
from Algorithm.Routing.mapVisual import draw_routes_on_map

# from mapVisual import draw_routes_on_map
import json
from fastapi import BackgroundTasks

# Truck metadata
truck_types = [
    {
        "type_index": 0,
        "name": "24-ft Truck",
        "length": 7.32,
        "width": 2.44,
        "height": 2.6,
        "volume": 7.32 * 2.44 * 2.6,
        "max_weight": 8000,
        "maximum_capacity": 500,
    },
    {
        "type_index": 1,
        "name": "32-ft Truck",
        "length": 9.75,
        "width": 2.44,
        "height": 2.6,
        "volume": 9.75 * 2.44 * 2.6,
        "max_weight": 10000,
        "maximum_capacity": 700,
    },
]

# Coordinates and customer mapping
coordinates = [
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
    (23.2584857, 77.401989),  # added on purpose to end here this is bhopal
    # (28.0937702,94.5921326),

]


# coordinates = [
#     (19.054999, 72.9692035), #depot  mumbai
#     (19.054999, 72.9892035), # near mumbai
#     (17.8499067, 75.2763203),# solapur
#     (18.3553347, 76.7548997),#latur
#     (17.7214822, 83.2900977), # vishakapatnam
#     (20.2602964,85.8394521), # bhubaneshwar
#     # (19.054999, 72.9692035),#end
#     (20.2602964,85.8394521),#end vishakapatnam
# ]
customer_names = [
    "AGRTLA",
    "SLCHR",
    "SLCHR-02",
    "SHILLONG",
    "GW-3-ADBR",
    "SLIGURI",
    "BRPT",
    "BRPT-2",
    "NALBARI",
    "GWHT",
    "BONGAIGAON",
    "ITNGR",
    "TINSUKIA",
    "TEZPUR",
    "JRHT",
    "DIPHU",
    "GOALPARA",
    "BHANGEL",
    "FBD-2",
    "BAREILLY (GURUDWARA)",
    "BRLY",
    "BUDAUN-(V2)",
    "BHRCH-2",
    "SITAPUR",
    "BLRMPR",
    "RAMPUR",
    "LAKHIMPUR",
    "GONDA",
    "HARDOI-(V2)",
    "LUCKNOW(KURSI RAOD)",
    "KNPR",
    "LKNW-TELIBAGH",
    "ALAMBAGH",
    "LKNW-SITAPUR ROAD",
    "LKNW",
    "JNK PRM",
    "RBRLY",
]


# def create_distance_matrix(coords):
#     size = len(coords)
#     return [
#         [int(geodesic(coords[i], coords[j]).km) for j in range(size)]
#         for i in range(size)
#     ]

end_index = len(coordinates) - 1


def create_distance_matrix(coords):
    size = len(coords)
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            dist = geodesic(coords[i], coords[j]).km
            if dist < 5:
                dist = 0  # ⚠️ Artificial preference for near points
            row.append(int(dist))
        matrix.append(row)
    return matrix


def create_data_model():
    data = {}
    data["distance_matrix"] = create_distance_matrix(coordinates)
    # data["demands"] = [0, 1, 580, 100, 100,100, 0]
    data["demands"] = [243, 300,245,104,232,58,265,185,76,343,20,234,135,109,168,45,20,78,149,204,
        130,81,115,108,71,118,120,72,126,115,135,84,83,74,50,55,137,0
        ]
    data["vehicle_capacities"] = [500] * 25 + [700] * 25
    data["num_vehicles"] = 50
    data["depot"] = 18
    # data["depot"] = 0
    return data


def generate_output(data, manager, routing, solution):
    final_output = {"message": []}
    print(routing)

    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route = [data["depot"]]  # ✅ Start from depot

        total_demand = 0
        stop_sequence = []

        while True:
            node_index = manager.IndexToNode(index)

            # If the current node is depot and it's the only stop, break
            if routing.IsEnd(index):
                break

            if node_index != data["depot"]:
                route.append(node_index)
                stop_sequence.append((node_index, len(stop_sequence) + 1))
                total_demand += data["demands"][node_index]

            index = solution.Value(routing.NextVar(index))

        if not stop_sequence:
            continue  # Skip empty trucks
        print(vehicle_id, "ansh")

        truck_type = truck_types[1] if vehicle_id > 25 else truck_types[0]
        box_list = []
        print(stop_sequence)

        for stop_index, (node, priority) in enumerate(stop_sequence):
            box_count = data["demands"][node]
            for b in range(box_count):
                box_list.append(
                    {
                        "customer_name": customer_names[node],
                        "priority": priority,
                        "weight": 12,
                        "box_number": b + 1,
                    }
                )
        path_list = []
        total_distance = 0
        for i in range(len(route) - 1):
            from_node = route[i]
            to_node = route[i + 1]
            dist = data["distance_matrix"][from_node][to_node]
            path_list.append({"from": from_node, "to": to_node, "distance": dist})
            total_distance += dist

        truck_data = {
            **truck_type,
            "boxes": box_list,
            "weight": total_demand,
            "path": path_list,  # 👈 NEW
            "total_distance": total_distance,
        }
        final_output["message"].append(truck_data)

    with open("final_output.json", "w") as f:
        json.dump(final_output, f, indent=4)
    print("✅ Output saved to final_output.json")
    return final_output


def main():
    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]),
        data["num_vehicles"],
        #  data["depot"]
        [data["depot"]] * data["num_vehicles"],
        [end_index] * data["num_vehicles"],
    )
    routing = pywrapcp.RoutingModel(manager)

    # for i in range(data["num_vehicles"]):
    #     if i < 25:
    #         routing.SetFixedCostOfVehicle(100, i)  # Prefer these
    #     else:
    #         routing.SetFixedCostOfVehicle(300, i)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, 0, data["vehicle_capacities"], True, "Capacity"
    )

    # for i in range(len(coordinates)):
    #     for j in range(i + 1, len(coordinates)):
    #         if geodesic(coordinates[i], coordinates[j]).km < 5:
    #             idx_i = manager.NodeToIndex(i)
    #             idx_j = manager.NodeToIndex(j)
    #             routing.solver().Add(routing.VehicleVar(idx_i) == routing.VehicleVar(idx_j))
    group_candidates = [
        (1, 2),  # SLCHR & SLCHR-02 → 300 + 245 = 545 ✅
        (30, 31),  # KNPR & LKNW-TELIBAGH → 115 + 135 = 250 ✅
        (32, 33),  # ALAMBAGH & LKNW-SITAPUR → 83 + 74 = 157 ✅
    ]
    # for i, j  in group_candidates:
    #     idx_i = manager.NodeToIndex(i)
    #     idx_j = manager.NodeToIndex(j)
    #     routing.solver().Add(routing.VehicleVar(idx_i) == routing.VehicleVar(idx_j))

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(2)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        structured_data = generate_output(data, manager, routing, solution)
        draw_routes_on_map(
            data, manager, routing, solution, coordinates, "withCapacity.html"
        )
        return structured_data
    else:
        print("❌ No solution found!")


if __name__ == "__main__":
    main()
