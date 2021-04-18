# File name: statequality.py
# Authors: Team 6 - Ludwik Huth, Mackenzie Macdonald, Divya Prabhakaran, Regan Siems, Kelly Wolfe
# Class: CS4269
# Date: April 18, 2021
# Honor statement: We pledge on our honor that we have neither given nor received any unauthorized aid
# on this assignment.
# Project Part: 2
# Description: This file implements the state quality functions which are used to calculate expected utility


import math  # Used for log operations in the state-quality function

WASTE = ['R21X', 'R22X', 'R23X', 'R24X', 'R25X', 'R26X', 'R27X', 'R28X', 'R29X', 'R30X']  # List of all waste resources
UPPER_BOUND = 20  # Default upper bound for a resource (indicating abundance) - scaled by resource weight
LOWER_BOUND = 10  # Default lower bound for a resource (indicating sufficiency) - scaled by resource weight


# This function calculates the final state-quality. It does so by calling several sub-functions and summing their values
# @param country represents the country for which the function calculates the state-quality
# @param world is the world in which the state-quality will be calculated
# @return state-quality value
def state_quality(country, world):
    # Get information for country evaluating
    quality_country = world.get_country(country)

    # Calculate state quality for each resource group
    essential_val = essential_state(quality_country, world)
    land_val = land_state(quality_country, world)
    manmade_val = manmade_state(quality_country, world)
    waste_val = waste_state(quality_country, world)

    return essential_val + land_val + manmade_val + waste_val


# This function calculates the value of the essential state resources. It consists of only housing based on our choices.
# The value for housing is scaled by 1/3 of the population, as, on average, a household has size of 3.
# @param country represents the country for which the function calculates the state-quality
# @param world is the world in which the state-quality will be calculated
# @return quality value for the essential state resources
def essential_state(country, world):
    population = country.get_resource_val('R1')
    housing_val = piecewise_value(country, world, 'R23') / (1 / 3 * population)
    return housing_val


# This function calculates the value of the land state resources. This consists of metallic elements
# and timber.
# @param country represents the country for which the function calculates the state-quality
# @param world is the world in which the state-quality will be calculated
# @return quality value for the land state resources
def land_state(country, world):
    metallic_elements_val = piecewise_value(country, world, 'R2')
    timber_val = piecewise_value(country, world, 'R3')
    return timber_val + metallic_elements_val


# This function calculates the value of the man-made state resources. This originally consisted of only metallic
# alloys and electronics. Many of our part 2 transforms are included here as well.
# @param country represents the country for which the function calculates the state-quality
# @param world is the world in which the state-quality will be calculated
# @return quality value for the man-made state resources
def manmade_state(country, world):
    metallic_alloys_val = piecewise_value(country, world, 'R21')
    electronics_val = piecewise_value(country, world, 'R22')
    fossil_val = piecewise_value(country, world, 'R25')
    weapons_val = piecewise_value(country, world, 'R26')
    military_val = piecewise_value(country, world, 'R27')
    medicine_val = piecewise_value(country, world, 'R28')
    telecomm_val = piecewise_value(country, world, 'R29')
    transport_val = piecewise_value(country, world, 'R30')
    fertilizer_val = piecewise_value(country, world, 'R31')
    farm_val = piecewise_value(country, world, 'R32')
    return metallic_alloys_val + electronics_val + fossil_val + weapons_val + military_val + medicine_val + \
           telecomm_val + transport_val + farm_val + fertilizer_val


# This function implements the piecewise function, which is the backbone of the state-quality function. It has three
# components and two variables. Variable 1. the amount of a resource and 2. the weight of a resource. We use the weight
# of each resource to scale the thresholds of the piecewise function. Below the bottom threshold, a country lacks this
# resource and thus quality is negative (linear to amount), once sufficiency is reached further quality gains are
# logarithmic. Then once the upper bound is hit, a country has the resource in abundance and quality stagnates
# @param country represents the country for which the function calculates the state-quality
# @param world is the world in which the state-quality will be calculated
# @param resource is the resource for which the current quality is evaluated
# @return quality value for the current resource
def piecewise_value(country, world, resource):
    # Get the amount and the weight for each resource in the country
    quantity = country.get_resource_val(resource)
    weight = world.get_resource_weight(resource)

    # For values less than the minimum desired value, calculate state quality contribution using this linear function
    if quantity < LOWER_BOUND * weight:
        val = 1 / 2 * quantity - (LOWER_BOUND * weight) / 2

    # For values greater than the upper bound, function will be constant
    elif quantity > UPPER_BOUND * weight:
        val = 5 * math.log(UPPER_BOUND * weight, math.e) - 10

    # For values in between lower and upper bounds, utilize ln function to calculate increasing value
    else:
        val = 5 * math.log(quantity, math.e) - 10
    return val


# This function calculates the value of the waste state resources. It takes a linear sum over all waste resources and
# their respective weights.
# @param country represents the country for which the function calculates the state-quality
# @param world is the world in which the state-quality will be calculated
# @return quality value for the waste resources
def waste_state(country, world):
    waste_sum = 0
    # Calculates the value for each resource with waste
    for waste_res in WASTE:
        waste_sum += country.get_resource_val(waste_res) * world.get_resource_weight(waste_res)
    return waste_sum
