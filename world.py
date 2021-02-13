class World:

    # Countries: Array of countries
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
            from_country.set_resource(resource, from_country.get_resource_val(resource) - amount)
            to_country.set_resource(resource, to_country.get_resource_val(resource) + amount)

    def transform(self, country, ):
        

    def __str__(self):
        countries = ""
        for country in self.__countries:
            countries += str(self.__countries[country]) + "\n"
        return countries