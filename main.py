# File name: main.py
# Authors: Team 6 - Ludwik Huth, Mackenzie Macdonald, Divya Prabhakaran, Regan Siems, Kelly Wolfe
# Class: CS4269
# Date: March 14th, 2021
# Honor statement: We pledge on our honor that we have neither given nor received any unauthorized aid
# on this assignment.
# Project Part: 1
# Description: This file is the program driver, running the test cases, and loading/printing the data form/to files

from random import randint
from country import Country  # To create the countries objects
from world import World  # To create the world objects

import scheduler as sd  # To call the scheduler on a given set of parameters
import pandas as pd  # To draw the data to and from the excel files


def my_world_scheduler(resources_filename, initial_state_filename, output_filename,
                       num_turns, depth_bound, frontier_max_size):
    choice_num = prompt_user_choice() # Get user's game setting choice
    df_resources = get_data_from_file(resources_filename)  # Load resources data from data frame
    # df_resources = modify_resources(resources_filename, choice_num) # Modify dataframe according to selection
    df_countries = get_data_from_file(initial_state_filename)  # Load country data frame
    world_matrix = create_matrix(df_countries, df_resources)  # Get the two data frames into a matrix
    world_object = generate_world(world_matrix,
                                  df_resources)  # Create the world object with country objects and weights
    countries = world_object.get_countries()
    num_countries = len(countries.keys())
    cur_world_object = world_object
    for x in range(num_turns):
        for country in countries:
            if(choice_num == 4): # Run disaster mode if user selects option 4
                disaster = disaster_prob()
                if disaster:
                    run_disaster(world_object, country)
            new_world = sd.scheduler(cur_world_object, country, 1, depth_bound, frontier_max_size)
            cur_world_object = new_world
        cur_world_object.turn_resources()  # Adds resources after every turn (I figured after made sense bc of 1st turn)
        print("Turn " + str(x + 1) + " Complete")


    print_game_output_to_file(output_filename, cur_world_object, num_turns, num_countries, countries)
    print("Scheduling complete -- Check " + output_filename + " file for results")


# This function determines if a disaster will take place or not
# if you are working on other parts of the code and don't want any disasters just change this to "return False".
# FIXME currently is hard coded to 10%
def disaster_prob():
    num = randint(0, 10)
    if num == 0:
        return True
    return False


# This function decided which disaster is going to be run in a country
# and then runs the chosen disaster.
# @param world_object is our world
# @param country is the country which the disaster will take place in
def run_disaster(world_object, country):
    num = randint(0, 4)
    disaster_str = ""

    if num == 0:
        world_object.tornado(country)
        disaster_str = "A tornado has taken place in " + country
    elif num == 1:
        world_object.earthquake(country)
        disaster_str = "An earthquake has taken place in " + country
    elif num == 2:
        world_object.fire(country)
        disaster_str = "A fire has taken place in " + country
    else:
        world_object.hurricane(country)
        disaster_str = "A hurricane has taken place in " + country

    print(disaster_str)
    return disaster_str


def print_game_output_to_file(file_name, final_world, num_turns, num_countries, countries):
    # Load schedules into a dictionary of schedule number and actual schedule
    dict_moves = {}
    moves_as_list = final_world.get_path()

    for x in range(1, num_turns + 1):
        for country in countries:
            move_name = "Move #" + str(x) + ": " + country + ": "
            dict_moves[move_name] = moves_as_list.pop(0)

    # Turn this into a data frame (schedule number as index)
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
def generate_world(matrix, df_resources):
    # Create dict of resources
    resource_dict = pd.Series(df_resources.Weight.values, index=df_resources.Resource).to_dict()
    names_dict = pd.Series(df_resources.Names.values, index=df_resources.Resource).to_dict()  # Get resource names
    world = World()
    world.set_resources(resource_dict)  # Set up world with resources
    world.set_resource_names(names_dict)
    for country, resources in matrix.iterrows():
        new_country = Country(country, dict(resources))
        world.add_country(new_country)
    return world
  
# Displays welcome message to the game and instructs user to enter their game mode choice
# @return the user input choice corresponding to one of the four game settings
def prompt_user_choice():
    valid = False
    print("Welcome to the country simulation! You, the player, will rule your own country. Your objective is to"
          " come out on top above all the other countries by making moves that will benefit your country. "
          "In this game, you have four settings you can play through: environmental, high-tech, war, or disaster.")
    selection = int(input(
        "Make your choice: 1 for the environmentally-conscious mode, " "2 for the technologically-focused mode"
        " 3 for the war-mode, and 4 for the disaster-mode."))
    #Check that user enters valid input, otherwise prompt user to choose a valid game setting
    while not valid:
        if selection <= 0 or selection > 4:
            print("Please choose a valid input.")
            selection = int(input(
                "Make your choice: 1 for the environmentally-conscious mode, " "2 for the technologically-focused mode"
                " 3 for the war-mode, 4 for the disaster-mode."))
        else:
            valid = True
            print("You have chosen game mode " + str(selection))
    return selection  
  
# FIXME RESOURCES TO REMOVE AND KEEP, KEEP ALl RESOURCES FOR MILITARY
# Remove resources from resources file depending on user choice of game setting
# @param resources_filename the resources data file to modify
# @return the modified dataframe to work with
def modify_resources(resources_filename, user_choice):
    df_resources = get_data_from_file(resources_filename)
    if (user_choice == 1):
        df_resources.drop(index=[17, 18, 19, 20], axis=0, inplace=True)
        # Keep Housing, Metallics, Electronics, Food,Transportation, Fertilizer, Farm, FossilFuels, Telecommunications
        # Delete Weapons, Military, Medicine
    elif (user_choice == 2 or user_choice == 4):
        df_resources.drop(index=[17, 18, 19, 20, 21, 22], axis=0, inplace=True)
        #  Keep Housing, Metallics, Electronics, Food,Transportation, Fertilizer, Farm, FossilFuels, Telecommunications
        #  Delete Weapons, Military, Medicine
    return df_resources

# The 7 test cases we have created for our world
# Calls to the method my_county_scheduler to do all of this work.
def test_cases():
    my_world_scheduler('data/resource_data.xlsx', 'data/test_case_3.xlsx', 'data/output_data3.xlsx',
                       3, 10, 10)


# This is the main program that calls the scheduler to run
def main():
    test_cases()


if __name__ == '__main__':
    main()
