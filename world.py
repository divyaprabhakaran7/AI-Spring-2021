class World:

    # Countries: dict of countries (Country name: country object)
    # Resources: dict of resources and weights (Resource name: resource weight)
    def __init__(self):
        self.__countries = {}
        self.__resources = {}

    def set_countries(self, countries):
        self.__countries = countries

    def get_country(self, country):
        return self.__countries[country]

    def add_country(self, country):
        self.__countries[country.get_name()] = country

    def get_countries(self):
        return self.__countries

    def set_resources(self, resources):
        self.__resources = resources

    def get_resources(self):
        return self.__resources

    def get_resource_weight(self, resource):
        return self.__resources[resource]

    # Checks if a given transformation is feasible for a certain country:
    # Either transforms and returns true, or returns false if transformation was not feasible
    def transform(self, country, output_resource, amount):
        transform_country = self.get_country(country)

        # Transform alloys, perform check for feasibility on amount
        if output_resource == 'R21':
            alloys_dict = {'R1': 1 * amount, 'R2': 2 * amount}
            if transform_country.resource_check(alloys_dict):
                transform_alloys(transform_country, amount)
                return True

        # Transform electronics
        if output_resource == 'R22':
            elec_dict = {'R1': 1 * amount, 'R2': 3 * amount, 'R21': 2 * amount}
            if transform_country.resource_check(elec_dict):
                transform_electronics(transform_country, amount)
                return True

        # Transform housing
        if output_resource == 'R23':
            alloys_dict = {'R1': 5 * amount, 'R2': 1 * amount, 'R3': 5 * amount, 'R21': 3 * amount}
            if transform_country.resource_check(alloys_dict):
                transform_housing(transform_country, amount)
                return True

        # Transform was unsuccessful -> return false
        return False

    # Checks if a given transfer is feasible for a certain country:
    # Either transfers and returns true, or returns false if transfer was not feasible
    def transfer(self, country1, country2, resource, amount):
        from_country = self.get_country(country1)
        to_country = self.get_country(country2)
        if from_country.resource_check(resource, amount):
            from_country.dec_resource(resource, amount)
            to_country.inc_resource(resource, amount)
            return True
        else:
            return False

    def __str__(self):
        world = "Current world state:\n\n"
        weights = "Resources and weights:"
        for resource in self.__resources:
            weights += " " + resource + ": " + str(self.__resources[resource])
        weights += "\n\n"
        countries = ""
        for country in self.__countries:
            countries += str(self.__countries[country]) + "\n"
        world += weights + countries
        return world


# Default number of transforms is 1 (Population requirement is checked by verifying function)
# Requires 5 population
def transform_housing(transform_country, amount=1):
    # Decrease inputs
    transform_country.dec_resource("R2", 1 * amount)  # MetallicElements
    transform_country.dec_resource("R3", 5 * amount)  # Timber
    transform_country.dec_resource("R21", 3 * amount)  # MetallicAlloys

    # increase outputs (population unchanged)
    transform_country.inc_resource("R23", 1 * amount)  # Housing
    transform_country.inc_resource("R23X", 1 * amount)  # HousingWaste


# Requires 1 population
def transform_alloys(country, amount=1):
    # Decrease inputs
    country.dec_resource("R2", 2 * amount)  # MetallicElements

    # increase outputs (population unchanged)
    country.inc_resource("R21", 1 * amount)  # Housing
    country.inc_resource("R21X", 1 * amount)  # HousingWaste


# Requires 1 population
def transform_electronics(transform_country, amount=1):
    # Decrease inputs
    transform_country.dec_resource("R2", 3 * amount)  # MetallicElements
    transform_country.dec_resource("R21", 2 * amount)  # MetallicAlloys

    # increase outputs (population unchanged)
    transform_country.inc_resource("R22", 2 * amount)  # Housing
    transform_country.inc_resource("R22X", 1 * amount)  # HousingWaste