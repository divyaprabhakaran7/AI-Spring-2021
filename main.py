# File name: main.py
# Authors: Team 6 - Ludwik Huth, Mackenzie Macdonald, Divya Prabhakaran, Regan Siems, Kelly Wolfe
# Class: CS4269
# Date: April 18, 2021
# Honor statement: We pledge on our honor that we have neither given nor received any unauthorized aid
# on this assignment.
# Project Part: 2
# Description: This file is the program driver, running the test cases, and loading/printing the data form/to files

from country import Country  # To create the countries objects
from world import World  # To create the world objects

import scheduler as sd  # To call the scheduler on a given set of parameters
import pandas as pd  # To draw the data to and from the excel files


# This function runs the world scheduler, which will print out the schedule produced
# @param resources_filename is the file name to be read in for the resources
# @param initial_state_filename is the file name that has the initial world state
# @param output_filename is the file to write out the results
# @param num_turns are the number of turns to be taken for the players
# @param depth_bound is the bound for the depth of the search
# @frontier_max_size is the maximum size of the frontier
def my_world_scheduler(resources_filename, initial_state_filename, output_filename,
                       num_turns, depth_bound, frontier_max_size):
    choice_num = prompt_user_choice()  # Get user's game setting choice
    df_resources = get_data_from_file(resources_filename)  # Load resources data from data frame
    df_countries = get_data_from_file(initial_state_filename)  # Load country data frame
    world_matrix = create_matrix(df_countries, df_resources)  # Get the two data frames into a matrix
    world_object = generate_world(world_matrix,
                                  df_resources,
                                  df_countries)  # Create the world object with country objects and weights
    valid_transforms, valid_transfers = initialize_resources_list(
        choice_num)  # Set of resources which will be valid in this mode
    countries = world_object.get_countries()
    world_object.set_user_setting(choice_num)  # set the world object into user's desired mode
    country_name, population, timber, metallic_elements, disaster_prob = user_resource_input(choice_num)
    cur_world_object = world_object

    # Updates user country according to user preferences
    update_user_country(cur_world_object, country_name, population, timber, metallic_elements, disaster_prob)

    dict_moves = {}

    for x in range(num_turns):
        print("\n----- Turn # " + str(x + 1) + " -----\n")
        for country in countries:
            move_name = "Turn #" + str(x + 1) + ": " + country + ": "
            new_world = sd.scheduler(cur_world_object, country, 1, depth_bound
                                     , frontier_max_size, valid_transforms, valid_transfers)
            cur_world_object = new_world
            if choice_num is 4:  # Run disaster mode if user selects option 4
                cur_world_object.disaster(country)  # Whether disaster was called or not (necessary for path)
            moves_as_list = cur_world_object.get_path()
            cur_move = moves_as_list[len(moves_as_list) - 1]
            dict_moves[move_name] = cur_move
            print(move_name + str(cur_move))
        cur_world_object.turn_resources()  # Adds resources after every turn (I figured after made sense bc of 1st turn)

    print_game_output_to_file(output_filename, cur_world_object, num_turns, countries, dict_moves)
    print("\n\nScheduling complete -- Check " + output_filename + " file for results")


# Returns a tuple of lists. First list is the list of transformable resources.
# Second list is the list of transferrable resources
# @param choice is the choice that the user selects
def initialize_resources_list(choice):
    if choice == 1:
        return ['R21', 'R22', 'R23', 'R24', 'R25', 'R29', 'R30', 'R31', 'R32'], ['R2', 'R3', 'R21', 'R22', 'R23', 'R24',
                                                                                 'R25',
                                                                                 'R29', 'R30', 'R31', 'R32']
    elif choice == 2:
        return ['R21', 'R22', 'R23', 'R24', 'R25', 'R28', 'R29', 'R30', 'R31', 'R32'], ['R2', 'R3', 'R21', 'R22', 'R23',
                                                                                        'R24', 'R25', 'R28',
                                                                                        'R29', 'R30', 'R31', 'R32']
    elif choice == 3:
        return ['R21', 'R22', 'R23', 'R24', 'R25', 'R26', 'R27', 'R28', 'R29', 'R30', 'R31', 'R32'], ['R2', 'R3', 'R21',
                                                                                                      'R22', 'R23',
                                                                                                      'R24', 'R25',
                                                                                                      'R26', 'R27',
                                                                                                      'R28', 'R29',
                                                                                                      'R30', 'R31',
                                                                                                      'R32']
    else:  # choice is 4
        return ['R21', 'R22', 'R23', 'R24', 'R25', 'R29', 'R30', 'R31', 'R32'], ['R2', 'R3', 'R21', 'R22', 'R23', 'R24',
                                                                                 'R25',
                                                                                 'R29', 'R30', 'R31', 'R32']


def update_user_country(cur_world, country_name, population, timber, metallic_elements, disaster_prob):
    user_country = cur_world.get_country("self")
    cur_world.delete_country("self")
    user_country.set_name(country_name)  # set name

    # set resources
    user_country.set_resource("R1", population)
    user_country.set_resource("R2", timber)
    user_country.set_resource("R3", metallic_elements)

    # Set disaster prob - value will be -1 if it should not be changed
    if disaster_prob is not -1:
        user_country.set_disaster_prob(disaster_prob)

    # Add country back into the list of countries
    cur_world.add_country(user_country)


def user_resource_input(choice_num):
    total = 100
    country_name = str(input("First, you must name your country. What should it be called?\n"))
    print(
        "Now, it is time to select what resources you want your country to have!\nYou have " + str(
            total) + " units to "
                     "divide evenly among your basic resources (population, timber, metallic elements).\nSelect wisely!")
    selection_pop = int(input(
        "\nHow much population do you want? " + str(total) + " units of resources remaining\n"))
    # Check that user enters valid input, otherwise prompt user to choose a valid game setting
    input_check(selection_pop, total, "Population")
    total = total - selection_pop
    # world_object.set_resources("R1")
    selection_timber = int(input(
        "How much timber do you want? " + str(total) + " units of resources remaining\n"))
    # Check that user enters valid input, otherwise prompt user to choose a valid game setting
    input_check(selection_timber, total, "Timber")
    total = total - selection_timber
    # world_object.set_resources("R2")
    selection_ME = int(input(
        "How much Metallic Elements do you want? " + str(total) + " units of resources remaining\n"))
    # Check that user enters valid input, otherwise prompt user to choose a valid game setting
    input_check(selection_ME, total, "Metallic Elements")
    total = total - selection_ME
    # world_object.set_resources("R3")

    disaster_prob = -1
    if choice_num is 4:
        user_disaster_prob = str(input(
            "\nWould? you like to change your country's default disaster probability?. Type 'yes' or 'no'.\n"))
        if user_disaster_prob.upper() == 'YES':
            new_disaster_prob = float(input("\nWhat would you like to change your country's disaster probability to?"
                                            " Input as a decimal (ie if 50% then type 0.50)\n"))
            disaster_prob = new_disaster_prob

    print("Thank you for entering your resources! Good luck!")
    return country_name, selection_pop, selection_timber, selection_ME, disaster_prob


def input_check(selection, total, resource):
    valid = False
    while not valid:
        if selection < 0 or selection > total:
            print("Please choose a valid input.")
            selection = int(input(
                "How much " + resource + " do you want? 100 units of resources remaining"))
        else:
            valid = True
            print("You have chosen " + str(selection) + " units of " + resource)


def print_game_output_to_file(file_name, final_world, num_turns, countries, dict_moves):
    # Turn schedule into a data frame (schedule number as index)
    df_schedules = pd.DataFrame.from_dict(dict_moves, orient='index')
    df_schedules.columns = ["Action Taken"]

    # Write the schedule and world data frames into excel (using XlsxWriter and pandas)
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df_schedules.to_excel(writer, sheet_name='Output Schedules')
    writer.save()


# This function loads a data frame of an excel sheet
# @param file_name is the file to load our data from
# @return df is the data frame being returned
def get_data_from_file(file_name):
    df = pd.read_excel(file_name, engine="xlrd")
    return df


# Create a matrix of countries and resources (used for initializing the country and world objects)
# @param df_countries is the country in that given data frame
# @param df_resources are the resources in the given data frame
# @return the data frame of the whole world in its given state
def create_matrix(df_countries, df_resources):
    resources = df_resources.Resource.tolist()  # Get a list of all resources in the world
    countries = df_countries.Country.tolist()  # Get a list of all countries in the world

    # Create a data frame that represents the state of the entire world (Rows = Countries, Columns = Resources)
    df_all = df_countries.reindex(columns=resources, fill_value=0)
    df_all['Countries'] = countries
    df_all = df_all.set_index('Countries')
    df_all = df_all.fillna(0.0).astype(int)  # Turns matrix from floats to ints (better display since no float values)
    return df_all


# Uses the country/resource matrix to create the country objects and load them into the world
# @param matrix is the matrix used to create the country objects
# @param df_resources are the resources from the given data frame
# @return a world object initialized with the countries, resources and resource weights that were provided
def generate_world(matrix, df_resources, df_countries):
    # Create dict of resources
    disaster_dict = pd.Series(df_countries.Disaster.values,
                              index=df_countries.Country).to_dict()  # extract disaster coeff.
    del df_countries["Disaster"]  # drop disaster col
    resource_dict = pd.Series(df_resources.Weight.values, index=df_resources.Resource).to_dict()
    names_dict = pd.Series(df_resources.Names.values, index=df_resources.Resource).to_dict()  # Get resource names
    world = World()
    world.set_resources(resource_dict)  # Set up world with resources
    world.set_resource_names(names_dict)
    for country, resources in matrix.iterrows():
        new_country = Country(country, dict(resources), disaster_dict[country])
        world.add_country(new_country)
    return world


# Displays welcome message to the game and instructs user to enter their game mode choice
# @return the user input choice corresponding to one of the four game settings
def prompt_user_choice():
    valid = False
    print("Welcome to the country simulation! You, the player, will rule your own country. \nYour objective is to"
          " come out on top above all the other countries by making moves that will benefit your country. "
          "\nIn this game, you have four settings you can play through: "
          "environmental, high-tech, war, or disaster.\n\n")
    selection = int(input(
        "Make your choice: \n1. for the environmentally-conscious mode, " "\n2. for the technologically-focused mode"
        " \n3. for the military, and \n4. for the disaster-mode.\n"))

    # Check that user enters valid input, otherwise prompt user to choose a valid game setting
    while not valid:
        if selection <= 0 or selection > 4:
            print("\nPlease choose a valid input.\n")
            selection = int(input(
                "Make your choice: \n1. for the environmentally-conscious mode, "
                "\n2. for the technologically-focused mode"
                "\n3. for the military, \n4. for the disaster-mode.\n"))
        else:
            valid = True
            print("\nYou have chosen game mode " + str(selection) + "\n")
    return selection


# The test cases we have created for our world
# Calls to the method my_county_scheduler to do all of this work.
def test_cases():
    my_world_scheduler('data/resource_data.xlsx', 'data/test_case_3.xlsx', 'data/output_data3.xlsx', 3, 5, 10)


# This is the main program that calls the scheduler to run
def main():
    test_cases()


if __name__ == '__main__':
    main()
