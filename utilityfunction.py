import math
from country import Country
from world import World


# essential:  LogF / p * f  + h/(p/3)  +  LogW / p * w
# Land:  T(W) + ME(W+ +  W-) + L(W+ +  W-) + REC(W+ +  W-) + FEC(W+ +  W-)  (linear)
# Manmade: MA(W+ +  W-) + E(W+ +  W-) + PRE(W+ +  W-) + PFE(W+ +  W-) + F(W+ +  W-) + M(W+ +  W-)

def state_quality(country):
    essential_val = essential_state(country)
    land_val = land_state(country)
    manmade_val = manmade_state(country)

    return essential_val + land_val + manmade_val


def essential_state(country):
    quantity_food = country.get_resource_val(country, 'food')
    population = country.get_resource_val(country, 'population')
    food_val = (math.log(quantity_food, 10)) / population

    quantity_housing = country.get_resource_val(country, 'housing')
    housing_val = quantity_housing / (population * 3)

    quantity_water = country.get_resource_val(country, 'water')
    water_val = (math.log(quantity_water, 10)) / population

    return food_val + housing_val + water_val


def land_state(country):
    return 0


def manmade_state(country):
    # return value for metallic alloys
    linear_value(country, 'R21', 'R21x')



def linear_value(country, resource, resource_waste):
    quantity = country.get_resource_val(country, resource)
    weight = world.get_resource_weight(world, resource)
    quantity_waste = country.get_resource_val(country, resource_waste)
    weight_waste = world.get_resource_weight(world, resource_waste)

    return quantity * weight - quantity_waste * weight_waste
