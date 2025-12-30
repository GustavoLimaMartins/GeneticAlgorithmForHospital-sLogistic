def load_vehicles_info(city: str) -> dict[str, dict]:
    if city == "SP":
        return {
            "V1": {
                "capacity": 25,
                "max_range_M": 0.030,     # autonomia em unidades Manhattan
                "cost_M": 120.0           # custo por unidade Manhattan
            },
            "V2": {
                "capacity": 35,
                "max_range_M": 0.045,
                "cost_M": 100.0
            },
            "V3": {
                "capacity": 15,
                "max_range_M": 0.025,
                "cost_M": 85.0
            },
            "V4": {
                "capacity": 20,
                "max_range_M": 0.032,
                "cost_M": 76.0
            },
            "V5": {
                "capacity": 10,
                "max_range_M": 0.018,
                "cost_M": 58.0
            }
        }
    else:
        return {}
