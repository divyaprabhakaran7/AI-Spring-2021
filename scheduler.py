# File name: scheduler.py
# Authors: Team 6 - Ludwik Huth, Mackenzie Macdonald, Divya Prabhakaran, Regan Siems, Kelly Wolfe
# Class: CS4269
# Date: March 14th, 2021
# Honor statement: We pledge on our honor that we have neither given nor received any unauthorized aid
# on this assignment.
# Project Part: 1
# Description: This file implements the scheduler, which is used to generate the output schedules for a given world


from depq import DEPQ  # Provides the double-ended queue functionality
import statequality as sq  # To run the state quality functions
import copy  # Used to make deep copies of world objects

TRANSFORM_RESOURCES = ['R21', 'R22', 'R23', 'R24']  # List of resources which may be created
TRANSFER_RESOURCES = ['R2', 'R3', 'R21', 'R22', 'R23', 'R24']  # List of resources which may be transferred
UPPER_BOUND = 10  # Default upper bound for a resource (indicating abundance) - scaled by resource weight
LOWER_BOUND = 5  # Default lower bound for a resource (indicating sufficiency) - scaled by resource weight


# This function creates the schedule of tranforms and transfers for the resources
# @param world_object is the world state to be passed in for the schedule to start from
# @param country_name is the name of our given country
# @param num_output_schedules is the number of desired schedules to output
# @param depth_bound is how deep to look for the schedule
# @param frontier_max_size is the size of the frontier to explore
# @return schedule as a list of strings
def scheduler(world_object, country_name, num_output_schedules, depth_bound, frontier_max_size):
    frontier = DEPQ(maxlen=frontier_max_size)  # Successors
    schedules = DEPQ(maxlen=num_output_schedules)  # Output schedules
    initial_state = world_object
    frontier.insert(initial_state, sq.state_quality(country_name, initial_state))

    # While there are states to explore and we still want more schedules
    while (frontier.is_empty() is not True) and (schedules.size() < num_output_schedules):
        current_state = frontier.popfirst()[0]  # just the state not the tuple (state, util)

        # If we still want to explore further (if not add to list of finished schedules
        if current_state.get_depth() < depth_bound:
            successor_states = get_successors(current_state, country_name)  # Get successors

            # insert successors by their expected utility
            for successor in successor_states:
                frontier.insert(successor, successor.expected_utility(country_name, initial_state))
        else:
            schedules.insert(current_state,
                             current_state.expected_utility(country_name, initial_state))
    return schedules_to_string(schedules)


# This function generates the successors for the schedule
# @param world_object is the world state that it is currently in
# @param country_name is the name of our country
# @return the successors that were found
def get_successors(world_object, country_name):
    successors = []

    # add transforms
    for resource in TRANSFORM_RESOURCES:
        tmp_world = copy.deepcopy(world_object)

        # Transform is possible
        if tmp_world.transform(country_name, resource, 1) is True:
            successors.append(tmp_world)

    # add transfers
    for resource in TRANSFER_RESOURCES:
        tmp_world = copy.deepcopy(world_object)
        resource_val = tmp_world.get_country(country_name).get_resource_val(resource)
        resource_weight = tmp_world.get_resource_weight(resource)

        # We have resource in abundance
        if resource_val > UPPER_BOUND * resource_weight:
            to_country = tmp_world.get_min_resource(resource)
            to_country_name = to_country.get_name()

            # no need to trade if everyone has in abundance
            if to_country_name != country_name:
                tmp_world.transfer(country_name, to_country_name, resource, 1)
                successors.append(tmp_world)

        # We lack resource
        elif resource_val < LOWER_BOUND * resource_weight:
            from_country = tmp_world.get_max_resource(resource)
            from_country_name = from_country.get_name()

            # no need to trade if everyone has in abundance
            if from_country_name != country_name:
                tmp_world.transfer(from_country_name, country_name, resource, 1)
                successors.append(tmp_world)

    return successors


# This function takes the schedules and outputs it as a string
# @param schedules are the schedules to put into a string
# @return the list of schedules as strings
def schedules_to_string(schedules):
    schedule_list = []
    for schedule, quality in schedules:
        schedule_list.append("Expected Utility: " + str(quality) + "|" + schedule.get_path_as_string())
    return schedule_list
