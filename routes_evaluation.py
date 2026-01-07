class RouteEvaluator:
    def __init__(self, routes_metadata: dict[int, list[tuple[str, str]]], vehicle_data: dict, delivery_data: dict):
        self.routes_metadata = routes_metadata
        self.vehicle_data = vehicle_data
        self.delivery_data = delivery_data

    def capacity_utilization(self) -> dict[int, float]:
        utilization = {}
        for route_id, deliveries in self.routes_metadata.items():
            vehicle_id = deliveries[0][1]  # Assuming all deliveries in the route use the same vehicle
            vehicle_capacity = self.vehicle_data[vehicle_id]["capacity"]
            total_demand = sum(self.delivery_data[int(delivery[0])]["demand"] for delivery in deliveries)
            utilization[route_id] = total_demand / vehicle_capacity if vehicle_capacity > 0 else 0.0
        return utilization
    
    def travel_costs(self) -> dict[int, float]:
        costs = {}
        for route_id, deliveries in self.routes_metadata.items():
            vehicle_id = deliveries[0][1]  # Assuming all deliveries in the route use the same vehicle
            vehicle_cost_per_M = self.vehicle_data[vehicle_id]["cost_M"]
            total_distance_M = len(deliveries) * 0.01  # Example: each delivery adds 0.01 Manhattan units
            costs[route_id] = total_distance_M * vehicle_cost_per_M
        return costs
    
    def critical_delivery_count_by_deliveries(self) -> dict[int, int]:
        critical_counts = {}
        for route_id, deliveries in self.routes_metadata.items():
            critical_count = sum(1 for delivery in deliveries if self.delivery_data[int(delivery[0])]["priority"] > 2)
            critical_counts[route_id] = critical_count
        return critical_counts

    def metric_summary(self) -> dict[str, float]:
        capacity_util = self.capacity_utilization()
        travel_costs = self.travel_costs()
        critical_counts = self.critical_delivery_count_by_deliveries()
        
        weighted_sum = 0
        for i in critical_counts.keys():
            weighted_sum += critical_counts[i] * (1 - (i * 0.1))

        return {
            "capacity_utilization_metric_positive": round(sum(capacity_util.values()) / len(capacity_util.keys()), 2),
            "travel_costs_metric_negative": round(sum(travel_costs.values()), 2),
            "critical_delivery_metric_positive": round(weighted_sum, 2)
        }
    
if __name__ == "__main__":
    from genetic_algorithm import GeneticAlgorithm
    city_code = "SP"

    ga = GeneticAlgorithm(
        city_code=city_code,
        population_length=50,
        max_generations=100, # 18000 * 20 executions for 10h
        ratio_elitism=0.1,
        ratio_mutation=0.3,
        tournament_k=2
    )
    ga_metadata = ga.run(iterator=1)
    routes_metadata = ga_metadata['routes_metadata']

    evaluator = RouteEvaluator(routes_metadata=routes_metadata, vehicle_data=ga.vehicles, delivery_data=ga.deliveries)
    print(ga_metadata)
    print(evaluator.metric_summary())
