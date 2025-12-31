def load_vehicles_info(city: str) -> dict[str, dict]:
    if city == "SP":
        return {
            "V1": {
                "capacity": 45,
                "max_range_M": 0.065,     # autonomia em unidades Manhattan
                "cost_M": 180.0           # custo por unidade Manhattan
            },
            "V2": {
                "capacity": 30,
                "max_range_M": 0.045,
                "cost_M": 120.0
            },
            "V3": {
                "capacity": 20,
                "max_range_M": 0.030,
                "cost_M": 85.0
            },
            "V4": {
                "capacity": 12,
                "max_range_M": 0.020,
                "cost_M": 60.0
            },
            "V5": {
                "capacity": 6,
                "max_range_M": 0.012,
                "cost_M": 35.0
            }
        }
    else:
        return {}
