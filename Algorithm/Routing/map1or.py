
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from geopy.distance import geodesic
from mapVisual import draw_routes_on_map
# coordinates = [
#     (23.8181266, 91.4363791), (24.8225239, 92.7992084), (24.8233218, 92.7997473),
#     (25.5772264, 91.8808823), (26.1580185, 91.68392709999999), (26.7220932, 88.4269844),
#     (26.3314809, 91.00615359999999), (26.485398, 90.969973), (26.448852, 91.4434068),
#     (26.1794295, 91.7510671), (26.4811277, 90.5546827), (27.1018582, 93.6296564),
#     (27.5328572, 95.3239723), (26.6203447, 92.796111), (26.7501438, 94.2162345),
#     (25.8441997, 93.44019109999999), (28.5422399, 77.3870653), (28.4670434, 77.2874178),
#     (28.3815904, 79.4343011), (28.336572, 79.4197497), (28.0312306, 79.1271625),
#     (27.5781833, 81.5990577), (27.565208, 80.6770261), (27.4371035, 82.1692972),
#     (28.7900278, 79.0215474), (27.9496461, 80.7759251), (27.1331673, 81.96911279999999),
#     (27.3877771, 80.13464479999999), (26.909252, 80.95658379999999),
#     (26.4234824, 80.3916122), (26.7778797, 80.94301720000001), (26.815645, 80.904569),
#     (26.897038, 80.9374154), (26.8809621, 81.0397476), (26.9265214, 80.94299749999999),
#     (26.2144806, 81.25281389999999)
# ]

coordinates = [
    (19.054999,72.8692035), # Mumbai
    (18.5213738,73.8545071), # Pune
    (12.9767936,77.590082) , # Bangalore
    (22.7203616,75.8681996) # Indore  
]

# Step 2: Create Distance Matrix
def create_distance_matrix(coords):
    size = len(coords)
    matrix = [[0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            matrix[i][j] = int(geodesic(coords[i], coords[j]).km)  # meters
    print(matrix)
    return matrix
def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = create_distance_matrix(coordinates)
    data["num_vehicles"] = 10 # 2457 km for mumbai wala coord
    # data["num_vehicles"] = 2 # 2823 for mumbai wala coord
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    max_route_distance = 0
    print("solution ansh")
    print(solution)
    print("vehicle_id ansh")
    print("Number of vehicles:", routing.vehicles())
    print("Number of nodes:", routing.Size())
    print("Start index for vehicle 0:", routing.Start(0))
    print("End index for vehicle 0:", routing.End(0))
    for vehicle_id in range(data["num_vehicles"]):
        
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print(f"Maximum of the route distances: {max_route_distance}m")
    

# def get_routes(data, manager, routing, solution):
#     """Extract routes from solution."""
#     routes = []
#     for vehicle_id in range(data["num_vehicles"]):
#         if not routing.IsVehicleUsed(solution, vehicle_id):
#             continue
#         index = routing.Start(vehicle_id)
#         route = []
#         while not routing.IsEnd(index):
#             node_index = manager.IndexToNode(index)
#             route.append(node_index)
#             index = solution.Value(routing.NextVar(index))
#         route.append(manager.IndexToNode(index))  # end node
#         routes.append(route)
#     return routes



def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
        # routes = get_routes(data, manager, routing, solution)
        # route_data = print_solution(data, manager, routing, solution)
        draw_routes_on_map(data, manager, routing, solution, coordinates , "withoutCapacity.html")

    else:
        print("No solution found !")


if __name__ == "__main__":
    main()