import math


# threshold high = you don't need a lot of it to have a positive value
# weight high = important if you have more or less than you need
# threshold low = you need a lot of it for it to have a positive value
# weight low = not that important if you have more or less than you need
# high threshold, high weight = you don't need a lot of it but if you do have a lot you get big impact
# high threshold low weight = you don't need a lot of it and it dpesn't really matter if you have
# low threshold, high weight = you need a lot of it, and moving away from threshold has big impact
# low threshold, low weight = you need a lot of it but it isn't that big of an impact if you are more
# or less than you need

def state_quality(country, world):
    quality_country = world.get_country(country)
    essential_val = essential_state(quality_country, world)
    land_val = land_state(quality_country, world)
    manmade_val = manmade_state(quality_country, world)

    return essential_val + land_val + manmade_val


def essential_state(country, world):
    # population must be proportional the other resources
    population = country.get_resource_val('R1')
    # each member of population needs food
    food_val = log_value(world, country, 'R23', 1 / population)
    # 3 people per house would be ideal, but they can live with more than that
    housing_val = log_value(world, country, 'R22', 1 / (population / 6))
    # each member of population needs water
    water_val = log_value(world, country, 'R7', 1 / population)

    # calculate waste
    food_waste = country.get_resource_val('R23X') * world.get_resource_weight('R23X')
    final_food = food_val - food_waste

    housing_waste = country.get_resource_val('R22X') * world.get_resource_weight('R22X')
    final_housing = housing_val - housing_waste

    water_waste = country.get_resource_val('R7X') * world.get_resource_weight('R7X')
    final_water = water_val - water_waste

    return final_water + final_housing + final_food


def land_state(country, world):
    population = country.get_resource_val('R1')

    # threshold of 1/10 because it is a very standard resource
    # this allows you to have enough for transformations
    # would be better if you had more than this though
    metallic_elements_val = log_value(world, country, 'R2', 1 / 5)
    renewable_energy_capacity_val = log_value(world, country, 'R5', 1 / 5)
    fossil_energy_capacity_val = log_value(world, country, 'R6', 1 / 5)
    timber_val = log_value(world, country, 'R3', 1 / 5)

    # want at least enough land for everyone to have a house and for extra land for other uses
    # this would be bare minimum at 0, you want more land than that
    land_val = log_value(world, country, 'R4', (1 / (population / 3)))

    # waste calculations
    metallic_elements_waste = country.get_resource_val('R2X') * world.get_resource_weight('R2X')
    final_metallic_elements = metallic_elements_val - metallic_elements_waste

    rec_waste = country.get_resource_val('R5X') * world.get_resource_weight('R5X')
    final_rec = renewable_energy_capacity_val - rec_waste

    fec_waste = country.get_resource_val('R6X') * world.get_resource_weight('R6X')
    final_fec = fossil_energy_capacity_val - fec_waste

    timber_waste = country.get_resource_val('R6X') * world.get_resource_weight('R6X')
    final_timber = timber_val - timber_waste

    land_waste = country.get_resource_val('R4X') * world.get_resource_weight('R4X')
    final_land = land_val - land_waste

    return final_land + final_fec + final_timber + final_metallic_elements + final_rec


def manmade_state(country, world):
    population = country.get_resource_val('R1')
    # you want some of your available land to go to farm land
    farm_val = log_value(world, country, 'R8', 1 / (population / 4))

    # You don't need that much of it for it to have high value
    military_val = log_value(world, country, 'R20', 2)
    metallic_alloys_val = log_value(world, country, 'R21', 2)
    prepared_fossil_energy_val = log_value(world, country, 'R24', 2)
    prepared_renewable_energy_val = log_value(world, country, 'R26', 2)
    electronics_val = log_value(world, country, 'R25', 2)

    # waste calculations

    farm_waste = country.get_resource_val('R8X') * world.get_resource_weight('R8X')
    final_farm = farm_val - farm_waste

    military_waste = country.get_resource_val('R20X') * world.get_resource_weight('R20X')
    military_final = military_val - military_waste

    metallic_alloys_waste = country.get_resource_val('R21X') * world.get_resource_weight('R21X')
    metallic_alloys_final = metallic_alloys_val - metallic_alloys_waste

    pfe_waste = country.get_resource_val('R24X') * world.get_resource_weight('R24X')
    pfe_final = prepared_fossil_energy_val - pfe_waste

    pre_waste = country.get_resource_val('R26X') * world.get_resource_weight('R26X')
    pre_final = prepared_renewable_energy_val - pre_waste

    electronics_waste = country.get_resource_val('R25X') * world.get_resource_weight('R25X')
    electronics_final = electronics_val - electronics_waste

    return final_farm + military_final + metallic_alloys_final + pfe_final + pre_final + electronics_final


def log_value(world, country, resource, threshold):
    quantity = country.get_resource_val(resource)  # food
    weight = world.get_resource_weight(resource)
    # if there isn't 0 amount of a quantity, then return a negative value
    if quantity < 1/threshold:
        val = 0
    else:
        val = weight * math.log(threshold * quantity)
    return val
