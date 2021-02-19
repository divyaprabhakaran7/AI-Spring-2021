import pandas as pd
from country import Country
from world import World


# Prototype function as described in the project spec (we'll initiate the scheduler from here)
def my_country_scheduler (your_country_name, resources_filename, initial_state_filename, output_schedule_filename,
                       num_output_schedules, depth_bound, frontier_max_size):
    df_resources = get_data_from_file(resources_filename) # load resources data frame
    df_countries = get_data_from_file(initial_state_filename) # load country data frame
    world_matrix = create_matrix(df_countries, df_resources) # Get the two data frames into a matrix
    world_object = generate_world(world_matrix) # Create the world object with country objects

    print(world_object)
    print("Test transfer")
    world_object.transfer('Atlantis', 'Erewhon', 'R1', 50)
    print(world_object)
    world_object.transform_housing('Atlantis', 2)
    print(world_object)


# Load a data frame of an excel sheet
def get_data_from_file(file_name):
    excel_file = pd.ExcelFile(file_name)
    df = pd.read_excel(excel_file)
    return df


# Create a matrix of countries and resources (used for initializing the country and world objects)
def create_matrix(df_countries, df_resources):
    resources = df_resources.Resource.tolist()  # Get a list of all resources in the world
    countries = df_countries.Country.tolist()  # Get a list of all countries in the world

    # Create a data frame that represents the state of the entire world (Rows = Countries, Columns = Resources)
    df_all = df_countries.reindex(columns=resources, fill_value=0)
    df_all['Countries'] = countries
    df_all = df_all.set_index('Countries')
    return df_all


# Uses the country/resource matrix to create the country objects and load them into the world
def generate_world(matrix):
    world = World()
    for country, resources in matrix.iterrows():
        new_country = Country(country, dict(resources))
        world.add_country(new_country)
    return world


def main():
    my_country_scheduler('Atlantis', 'data/resource_data.xls', 'data/country_data.xls', 'data/output_data.xls', 1, 1, 1)


if __name__ == '__main__':
    main()
