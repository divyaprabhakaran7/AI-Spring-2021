# File name: scheduler.py
# Authors: Team 6 - Ludwik Huth, Mackenzie Macdonald, Divya Prabhakaran, Regan Siems, Kelly Wolfe
# Class: CS4269
# Date: April 18, 2021
# Honor statement: We pledge on our honor that we have neither given nor received any unauthorized aid
# on this assignment.
# Project Part: 2
# Description: This file implements the scheduler, which is used to generate the output schedules for a given world


from depq import DEPQ  # Provides the double-ended queue functionality
import statequality as sq  # To run the state quality functions
import copy  # Used to make deep copies of world objects

UPPER_BOUND = 20  # Default upper bound for a resource (indicating abundance) - scaled by resource weight
LOWER_BOUND = 10  # Default lower bound for a resource (indicating sufficiency) - scaled by resource weight


# This function creates the schedule of tranforms and transfers for the resources
# @param world_object is the world state to be passed in for the schedule to start from
# @param country_name is the name of our given country
# @param num_output_schedules is the number of desired schedules to output
# @param depth_bound is how deep to look for the schedule
# @param frontier_max_size is the size of the frontier to explore
# @param transforms is the list of available transforms
# @param transfers is the list of available transfers
# @return schedule as a list of strings
def scheduler(world_object, country_name, num_output_schedules, depth_bound, frontier_max_size, transforms, transfers):
    frontier = DEPQ(maxlen=frontier_max_size)  # Successors
    schedules = DEPQ(maxlen=num_output_schedules)  # Output schedules
    initial_state = world_object
    current_path = initial_state.get_path()
    initial_state.reset_path()

    # Our queue is now keeps track of the first step and the final step (because we want to search for best
    # move several layers deep but only want the first move to be made)
    frontier.insert((initial_state, initial_state), 0)

    # While there are states to explore and we still want more schedules
    while (frontier.is_empty() is not True) and (schedules.size() < num_output_schedules):
        current_state, current_first_step = frontier.popfirst()[0]  # just the state not the tuple (state, util)

        # If we still want to explore further (if not add to list of finished schedules
        if current_state.get_depth() < depth_bound:
            successor_states = get_successors(current_state, country_name, transforms, transfers)  # Get successors

            # insert successors by their expected utility
            if len(successor_states) != 0 and successor_states[0].get_depth() == 1:
                for successor in successor_states:
                    frontier.insert((successor, successor), successor.expected_utility(country_name, initial_state))
            else:
                for successor in successor_states:
                    frontier.insert((successor, current_first_step),
                                    successor.expected_utility(country_name, initial_state))
        else:
            schedules.insert((current_state, current_first_step),
                             current_state.expected_utility(country_name, initial_state))
    # return schedules_to_string(schedules) this is what we used for our previous runs
    # There is a problem here where some countries seem to run out of schedules
    # I am also resetting the path at the start of this method so countries act as if this was their first turn
    final_state = initial_state
    if schedules.size() > 0:
        schedule_tuple = schedules.popfirst()[0]
        final_state = schedule_tuple[1]
    else:
        initial_state.country_passes(country_name)
        final_state = copy.deepcopy(initial_state)

    # This adds back the old path + the move that was just made
    new_path = final_state.get_path()
    current_path.append(new_path)
    final_state.set_path(current_path)
    return final_state


# This function generates the successors for the schedule
# @param world_object is the world state that it is currently in
# @param country_name is the name of our country
# @param transforms is the list of available transforms
# @param transfers is the list of available transfers
# @return the successors that were found
def get_successors(world_object, country_name, transforms, transfers):
    successors = []

    # add transforms
    for resource in transforms:
        tmp_world = copy.deepcopy(world_object)

        # Transform is possible
        if tmp_world.transform(country_name, resource, 1):
            successors.append(tmp_world)

    # add transfers
    for resource in transfers:
        tmp_world = copy.deepcopy(world_object)
        resource_val = tmp_world.get_country(country_name).get_resource_val(resource)
        resource_weight = tmp_world.get_resource_weight(resource)

        # We have resource in abundance
        if resource_val > UPPER_BOUND * resource_weight:
            to_country = tmp_world.get_min_resource(resource)
            to_country_name = to_country.get_name()

            # no need to trade if everyone has in abundance
            if to_country_name != country_name and verify_transfer(world_object, tmp_world, to_country_name):
                if tmp_world.transfer(country_name, to_country_name, resource, 1):
                    successors.append(tmp_world)

        # We lack resource
        elif resource_val < LOWER_BOUND * resource_weight:
            from_country = tmp_world.get_max_resource(resource)
            from_country_name = from_country.get_name()

            # no need to trade if everyone lacks
            if from_country_name != country_name and verify_transfer(world_object, tmp_world, from_country_name):
                if tmp_world.transfer(from_country_name, country_name, resource, 1):
                    successors.append(tmp_world)

    return successors


# Make sure that the transfer is helpful for both countries before performing it
# @param cur_world is the current world being used
# @param proposed_new_world is the world that would happen is the transfer took place
# @param other_country_name is the country being transferred with
def verify_transfer(cur_world, proposed_new_world, other_country_name):
    return proposed_new_world.get_undiscounted_reward(other_country_name, cur_world) >= 0
