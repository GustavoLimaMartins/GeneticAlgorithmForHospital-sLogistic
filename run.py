from delivery_setup.deliveries import load_deliveries_info
from a_generate_population import generate_population_coordinates

print(load_deliveries_info("SP"))
print(generate_population_coordinates("SP", 5))