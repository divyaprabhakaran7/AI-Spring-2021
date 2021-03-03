import math


# essential:  LogF / p * f  + h/(p/3)  +  LogW / p * w
# Land:  T(W) + ME(W+ +  W-) + L(W+ +  W-) + REC(W+ +  W-) + FEC(W+ +  W-)  (linear)
# Manmade: MA(W+ +  W-) + E(W+ +  W-) + PRE(W+ +  W-) + PFE(W+ +  W-) + F(W+ +  W-) + M(W+ +  W-)

def state_quality(country, world):
    essential_val = essential_state(country)
    land_val = land_state(country, world)
    manmade_val = manmade_state(country, world)

    return essential_val + land_val + manmade_val


def essential_state(country):
    quantity_food = country.get_resource_val('R23')  # food
    population = country.get_resource_val('R1')  # population
    food_val = quantity_food / population

    quantity_housing = country.get_resource_val('R22')  # housing
    housing_val = quantity_housing / (population * 3)

    quantity_water = country.get_resource_val('R7')  # water
    water_val = quantity_water / population

    return food_val + housing_val + water_val


def land_state(country, world):
    timber_val = linear_value(world, country, 'R3', 'R3X')
    metallic_elements_val = linear_value(world, country, 'R2', 'R2X')
    land_val = linear_value(world, country, 'R4', 'R4X')
    renewable_energy_capacity_val = linear_value(world, country, 'R5', 'R5X')
    fossil_energy_capacity_val = linear_value(world, country, 'R6', 'R6X')

    return timber_val + metallic_elements_val + land_val + fossil_energy_capacity_val + renewable_energy_capacity_val


def manmade_state(country, world):
    metallic_alloy_val = linear_value(world, country, 'R21', 'R21X')
    electronics_val = linear_value(world, country, 'R25', 'R25X')
    prep_renew_energy_val = linear_value(world, country, 'R26', 'R26X')
    prep_fossil_energy_val = linear_value(world, country, 'R24', 'R24X')
    farm_val = linear_value(world, country, 'R8', 'R8X')
    military_val = linear_value(world, country, 'R20', 'R20X')

    return metallic_alloy_val + electronics_val + prep_renew_energy_val + prep_fossil_energy_val + farm_val + military_val


def linear_value(world, country, resource, resource_waste):
    quantity = country.get_resource_val(resource)
    weight = world.get_resource_weight(resource)
    quantity_waste = country.get_resource_val(resource_waste)
    weight_waste = world.get_resource_weight(resource_waste)

    return (float(quantity) * float(weight)) - (float(quantity_waste) * float(weight_waste))
