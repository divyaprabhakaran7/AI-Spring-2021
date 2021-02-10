class World:

    # Countries: Array of countries
    def __init__(self):
        self.__countries = []

    def set_countries(self, countries):
        self.__countries = countries

    def add_country(self, country):
        return self.__countries.append(country)

    def get_countries(self):
        return self.__countries

    def __str__(self):
        countries = ""
        for country in self.__countries:
            countries += str(country) + "\n"
        return countries