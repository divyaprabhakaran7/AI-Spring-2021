from depq import DEPQ  # double-ended queue
import statequality as sq
import copy # we need this to act as our copy constructor to avoid memory problems with lists

TRANSFORM_RESOURCES = ['R20', 'R21', 'R22', 'R23', 'R24', 'R25', 'R26']
TRANSFER_RESOURCES = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R20', 'R21', 'R22', 'R23', 'R24', 'R25', 'R26']
UPPER_BOUND = 10
LOWER_BOUND = 5


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
    return schedules_to_string(schedules)  # Return Schedule as a list of strings


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

        # We have resource in abundance
        if resource_val > UPPER_BOUND:
            to_country = tmp_world.get_min_resource(resource)
            to_country_name = to_country.get_name()

            # no need to trade if everyone has in abundance
            if to_country_name is not country_name:
                tmp_world.transfer(country_name, to_country_name, resource, 1)
                successors.append(tmp_world)

        # We lack resource
        elif resource_val < LOWER_BOUND:
            from_country = tmp_world.get_max_resource(resource)
            from_country_name = from_country.get_name()

            # no need to trade if everyone has in abundance
            if from_country_name is not country_name:
                tmp_world.transfer(from_country_name, country_name, resource, 1)
                successors.append(tmp_world)

    return successors


def schedules_to_string(schedules):
    schedule_list = []
    for schedule, quality in schedules:
        schedule_list.append("Expected Utility: " + str(quality) + "\nPath:\n" + schedule.get_path_as_string())
    return schedule_list
