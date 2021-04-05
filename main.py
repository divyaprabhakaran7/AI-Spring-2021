# File name: main.py
# Authors: Team 6 - Ludwik Huth, Mackenzie Macdonald, Divya Prabhakaran, Regan Siems, Kelly Wolfe
# Class: CS4269
# Date: March 14th, 2021
# Honor statement: We pledge on our honor that we have neither given nor received any unauthorized aid
# on this assignment.
# Project Part: 1
# Description: This file is the program driver, running the test cases, and loading/printing the data form/to files


from country import Country  # To create the countries objects
from world import World  # To create the world objects

import scheduler as sd  # To call the scheduler on a given set of parameters
import pandas as pd  # To draw the data to and from the excel files


def my_world_scheduler(resources_filename, initial_state_filename, output_filename,
                       num_turns, depth_bound, frontier_max_size):
    df_resources = get_data_from_file(resources_filename)  # Load resources data frame
    df_countries = get_data_from_file(initial_state_filename)  # Load country data frame
    world_matrix = create_matrix(df_countries, df_resources)  # Get the two data frames into a matrix
    world_object = generate_world(world_matrix,
                                  df_resources)  # Create the world object with country objects and weights
    countries = world_object.get_countries()
    num_countries = len(countries.keys())
    cur_world_object = world_object
    for x in range(num_turns):
        for country in countries:
            new_world = sd.scheduler(cur_world_object, country, 1, depth_bound, frontier_max_size)
            cur_world_object = new_world
        print("Turn " + str(x + 1) + " Complete")

    print_game_output_to_file(output_filename, cur_world_object, num_turns, num_countries, countries)
    print("Scheduling complete -- Check " + output_filename + " file for results")


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


# The 7 test cases we have created for our world
# Calls to the method my_county_scheduler to do all of this work.
def test_cases():
    my_world_scheduler('data/resource_data.xlsx', 'data/test_case_2.xlsx', 'data/output_data2.xlsx',
                       3, 10, 10)


# This is the main program that calls the scheduler to run
def main():
    test_cases()


if __name__ == '__main__':
    main()
