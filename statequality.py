import math

WASTE = ['R21X', 'R22X', 'R23X']
LOWER_BOUND = 10
UPPER_BOUND = 20


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
    waste_val = waste_state(quality_country, world)

    return essential_val + land_val + manmade_val + waste_val


def essential_state(country, world):
    # population must be proportional the other resources
    population = country.get_resource_val('R1')
    # 3 people per house would be ideal, but they can live with more than that
    housing_val = log_value(world, country, 'R23', 1 / (population / 6))

    return housing_val


def land_state(country, world):
    # threshold of 1/10 because it is a very standard resource
    # this allows you to have enough for transformations
    # would be better if you had more than this though
    metallic_elements_val = log_value(world, country, 'R2', 1 / 5)
    timber_val = log_value(world, country, 'R3', 1 / 5)

    return timber_val + metallic_elements_val


def manmade_state(country, world):
    metallic_alloys_val = log_value(world, country, 'R21', 2)
    electronics_val = log_value(world, country, 'R22', 2)

    return metallic_alloys_val + electronics_val


def log_value(world, country, resource, threshold):
    quantity = country.get_resource_val(resource)  # food
    weight = world.get_resource_weight(resource)
    # if there isn't 0 amount of a quantity, then return a negative value
    if quantity < LOWER_BOUND * weight:
        val = 2 * quantity - (LOWER_BOUND * weight) / 2

    elif quantity > UPPER_BOUND * weight:
        val = weight * math.log(UPPER_BOUND * weight)

    else:
        val = weight * math.log(quantity)
    return val


def waste_state(country, world):
    waste_sum = 0
    for waste_res in WASTE:
        waste_sum += country.get_resource_val(waste_res) * world.get_resource_weight(waste_res)
    return waste_sum
