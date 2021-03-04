from depq import DEPQ  # double-ended queue
import statequality as sq

TRANSFORM_RESOURCES = ['R20', 'R21', 'R22', 'R23', 'R24', 'R25', 'R26']
TRANSFER_RESOURCES = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R20', 'R21', 'R22', 'R23', 'R24', 'R25', 'R26']
UPPER_BOUND = 10
LOWER_BOUND = 5

def scheduler(world_object, country_name, num_output_schedules, depth_bound, frontier_max_size):
    frontier = DEPQ(maxlen=frontier_max_size)
    initial_state = world_object
    frontier.insert(initial_state, sq.state_quality(country_name, initial_state))
    next_state = frontier.popfirst()
    return 0


def get_successors(world_object, country_name):
    successors = []

    # add transforms
    for resource in TRANSFORM_RESOURCES:
        tmp_world = world_object

        # Transform is possible
        if world_object.transform(country_name, resource, 1) is True:
            successors.append(tmp_world)

    # add transfers
    for resource in TRANSFER_RESOURCES:
        tmp_world = world_object
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

