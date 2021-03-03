from depq import DEPQ  # double-ended queue
import statequality as sq

TRANSFORM_RESOURCES = {'R20', 'R21', 'R22', 'R23', 'R24', 'R25', 'R26'}

def scheduler(world_object, country_name, num_output_schedules, depth_bound, frontier_max_size):
    frontier = DEPQ(maxlen=frontier_max_size)
    initial_state = world_object
    frontier.insert(initial_state, sq.state_quality(country_name, initial_state))
    next_state = frontier.popfirst()
    return 0


def get_successors(world_object, country_name):
    successor = {}




