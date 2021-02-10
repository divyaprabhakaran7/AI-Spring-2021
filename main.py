import pandas as pd

def getDataFromFile(file_name):
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


def main():
    matrix = getDataFromFile("Example-Initial-World.xls")
    print(matrix)


if __name__ == '__main__':
    main()
