import pandas as pd
from country import Country
from world import World
import statequality as sq
import scheduler as sd


# Prototype function as described in the project spec (we'll initiate the scheduler from here)
def my_country_scheduler(your_country_name, resources_filename, initial_state_filename, output_schedule_filename,
                         num_output_schedules, depth_bound, frontier_max_size):
    df_resources = get_data_from_file(resources_filename)  # load resources data frame
    df_countries = get_data_from_file(initial_state_filename)  # load country data frame
    world_matrix = create_matrix(df_countries, df_resources)  # Get the two data frames into a matrix
    world_object = generate_world(world_matrix,
                                  df_resources)  # Create the world object with country objects and weights

    # Simple transform/transfer tests
    #print(world_object)
    # world_object.transform('Atlantis', 'R21', 10)
    # world_object.transform('Atlantis', 'R22', 5)
    # print(world_object)
    # print(sq.state_quality(world_object.get_country('Atlantis'), world_object))

    world_object.transform('Atlantis', 'R22', 3)
    world_object.transform('Atlantis', 'R22', 2)
    world_object.transform('Atlantis', 'R22', 1)
    world_object.transfer('Atlantis', 'Carpania', 'R22', 3)
    print(world_object.get_path_as_string())
    #sd.scheduler(world_object, your_country_name, num_output_schedules, depth_bound, frontier_max_size)

    print_data_to_file(output_schedule_filename, world_object)


# Load a data frame of an excel sheet
def get_data_from_file(file_name):
    df = pd.read_excel(file_name, engine='openpyxl')  # FIXME Need to install openpyxl package to run this
    df = df.loc[:df.last_valid_index()]  # This ensures that there are no trailing blank rows (weird bug with openpyxl)
    return df


# Prints our output state into a .xlsx file
def print_data_to_file(file_name, world):
    resources = world.get_resources()
    countries = world.get_countries()

    # Load countries into a dictionary of countries and their resource values
    dict_all = {}
    for country in countries:
        dict_all[country] = countries[country].get_resources_as_list()

    df_all = pd.DataFrame.from_dict(dict_all, orient='index')  # Turn this into a data frame (countries as index)
    df_all.columns = resources.keys()  # Add resources as column headers
    df_all.to_excel(file_name, sheet_name='Output Data')  # Print into our output excel file


# Create a matrix of countries and resources (used for initializing the country and world objects)
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


def main():
    my_country_scheduler('Atlantis', 'data/resource_data.xlsx', 'data/country_data.xlsx',
                         'data/output_data.xlsx', 1, 1, 1)


if __name__ == '__main__':
    main()
