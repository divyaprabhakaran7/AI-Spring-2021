from country import Country  # To create the countries objects
from world import World  # To create the world objects

import scheduler as sd  # To call the scheduler on a given set of parameters
import pandas as pd  # To draw the data to and from the excel files


# Prototype function as described in the project spec (we'll initiate the scheduler from here)

# This function initializes the date and passes it into the scheduler as well as printing the data to our output
# @param your_country_name is the our country
# @param resources_filename is the file for the resources to be read
# @param initial_state_filename is the file that holds the initial world state
# @param output_schedule_filename is the file to output the completed schedule to
# @param num_output_schedules is the number of schedules to output
# @param depth_bound is the depth of exploration that we want to bound our scheduler to
# @param frontier_max_size is the maximum size of our frontier
def my_country_scheduler(your_country_name, resources_filename, initial_state_filename, output_schedule_filename,
                         num_output_schedules, depth_bound, frontier_max_size):
    df_resources = get_data_from_file(resources_filename)  # Load resources data frame
    df_countries = get_data_from_file(initial_state_filename)  # Load country data frame
    world_matrix = create_matrix(df_countries, df_resources)  # Get the two data frames into a matrix
    world_object = generate_world(world_matrix,
                                  df_resources)  # Create the world object with country objects and weights

    # Call the scheduler on the created world object, with the specified parameters
    schedules = sd.scheduler(world_object, your_country_name, num_output_schedules, depth_bound, frontier_max_size)

    # Print output schedules to the output_data file
    print_data_to_file(output_schedule_filename, world_object, schedules, depth_bound)

    # If this prints, scheduler completed successfully
    print("Scheduling complete -- Check output_data file for results")


# This function loads a data frame of an excel sheet
# @param file_name is the file to load our data from
# @return df is the data frame being returned
def get_data_from_file(file_name):
    df = pd.read_excel(file_name)  # Need to install openpyxl package to run this
    df = df.loc[:df.last_valid_index()]  # This ensures that there are no trailing blank rows (weird bug with openpyxl)
    return df


# Prints our output state into a .xlsx file
# @param file_name is the name of the file to print the data to
# @param world is the world object that we want to output to our file
# @param schedules is the list of all output-schedules to be printed to the file
# @param depth_bound is the depth of the individual schedules (used to format the excel output file)
def print_data_to_file(file_name, world, schedules, depth_bound):
    # Load schedules into a dictionary of schedule number and actual schedule
    dict_schedules = {}
    schedule_num = 1
    for schedule in schedules:
        schedule_name = "Schedule " + str(schedule_num)
        schedule_as_list = schedule.split("|")
        schedule_as_list.pop()
        dict_schedules[schedule_name] = schedule_as_list
        schedule_num += 1

    # Turn this into a data frame (schedule number as index)
    cols = ["Expected Utility of Schedule"]
    for x in range(1, depth_bound + 1):
        cols.append("Depth " + str(x))
    df_schedules = pd.DataFrame.from_dict(dict_schedules, orient='index')
    df_schedules.columns = cols

    # Write the schedule and world data frames into excel (using XlsxWriter and pandas)
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df_schedules.to_excel(writer, sheet_name='Output Schedules')
    writer.save()


# Create a matrix of countries and resources (used for initializing the country and world objects)
# @param df_countries is the country in that given data frame
# @param df_resources are the resources in the given data frame
# @returns df_all returns the data frame of the whole world in its given state
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
    resource_dict = pd.Series(df_resources.Weight.values, index=df_resources.Resource).to_dict()
    names_dict = pd.Series(df_resources.Names.values, index=df_resources.Resource).to_dict()  # Get resource names
    world = World()
    world.set_resources(resource_dict)
    world.set_resource_names(names_dict)
    for country, resources in matrix.iterrows():
        new_country = Country(country, dict(resources))
        world.add_country(new_country)
    return world


# This is the main program that calls the scheduler to run
def main():
    my_country_scheduler('self', 'data/resource_data.xlsx', 'data/country_data.xlsx',
                         'data/output_data.xlsx', 10, 10, 50)


if __name__ == '__main__':
    main()
