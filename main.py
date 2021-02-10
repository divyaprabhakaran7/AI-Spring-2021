import pandas as pd
from country import Country
from world import World


def get_data_from_file(file_name):
    excel_file = pd.ExcelFile(file_name)  # Install xlrd package to unlock Excel functionality in Pandas

    # Extract sheets from the file
    df_resources = pd.read_excel(excel_file, 'Resources')
    df_countries = pd.read_excel(excel_file, 'Countries')

    resources = df_resources.Resource.tolist()  # Get a list of all resources in the world
    countries = df_countries.Country.tolist()  # Get a list of all countries in the world

    # Create a data frame that represents the state of the entire world (Rows = Countries, Columns = Resources)
    df_all = df_countries.reindex(columns=resources, fill_value=0)
    df_all['Countries'] = countries
    df_all = df_all.set_index('Countries')
    return df_all


def generate_world(matrix):
    world = World()
    for country, resources in matrix.iterrows():
        newCountry = Country(country, dict(resources))
        world.add_country(newCountry)
    return world


def main():
    matrix = get_data_from_file("data/Example-Initial-World.xls")
    world = generate_world(matrix)
    print(world)


if __name__ == '__main__':
    main()
