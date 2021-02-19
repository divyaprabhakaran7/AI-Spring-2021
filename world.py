class World:

    # Countries: dict of countries
    def __init__(self):
        self.__countries = {}

    def set_countries(self, countries):
        self.__countries = countries

    def get_country(self, country):
        return self.__countries[country]

    def add_country(self, country):
        self.__countries[country.get_name()] = country

    def get_countries(self):
        return self.__countries

    def transfer(self, country1, country2, resource, amount):
        from_country = self.get_country(country1)
        to_country = self.get_country(country2)
        if from_country.get_resource_val(resource) < amount:
            print("Transfer failed")
        else:
            from_country.dec_resource(resource, amount)
            to_country.inc_resource(resource, amount)


    # Default number of transforms is 1
    # FIXME could make theses constants if we change transforms
    def transform_housing(self, country, amount=1):
        # Decrease inputs
        transform_country = self.get_country(country)
        transform_country.dec_resource("R2", 1 * amount) # MetallicElements
        transform_country.dec_resource("R3", 5 * amount) # Timber
        transform_country.dec_resource("R21", 3 * amount) # MetallicAlloys

        # increase outputs (population unchanged)
        transform_country.inc_resource("R23", 1 * amount) # Housing
        transform_country.inc_resource("R23'", 1 * amount) # HousingWaste


    def __str__(self):
        countries = ""
        for country in self.__countries:
            countries += str(self.__countries[country]) + "\n"
        return countries