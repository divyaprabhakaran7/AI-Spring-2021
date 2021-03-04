import math
import statequality as sq


class World:

    # Countries: dict of countries (Country name: country object)
    # Resources: dict of resources and weights (Resource name: resource weight)
    def __init__(self):
        self.__countries = {}
        self.__resources = {}
        self.__resource_name = {}
        self.__actions_path = []

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

    def set_resource_names(self, resource_names):
        self.__resource_names = resource_names

    def get_resource_name(self, resource):
        return self.__resource_names[resource]

    def get_resource_weight(self, resource):
        return self.__resources[resource]

    def get_path(self):
        return self.__actions_path

    def get_path_as_string(self):
        action_str = ""
        for action in self.__actions_path:
            action_str += action + "\n"
        return action_str

    def get_path_length(self):
        return len(self.__actions_path)

    def get_max_resource(self, resource):
        max_country = ""
        max_count = -1
        for country in self.__countries:
            count = self.__countries[country].get_resource_val(resource)
            if count > max_count:
                max_country = country
                max_count = count
        return max_country

    def get_min_resource(self, resource):
        min_country = ""
        min_count = 100000  # FIXME find a better way of doing this
        for country in self.__countries:
            count = self.__countries[country].get_resource_val(resource)
            if count < min_count:
                min_country = country
                min_count = count
        return min_country

    # Checks if a given transformation is feasible for a certain country:
    # Either transforms and returns true, or returns false if transformation was not feasible
    def transform(self, country, output_resource, amount):
        transform_country = self.get_country(country)

        # Transform military
        if output_resource == 'R20':
            military_dict = {'R1': 2 * amount, 'R25': 2 * amount, 'R22': 2 * amount, 'R23': 2 * amount,
                             'R7': 1 * amount}
            if transform_country.resource_check(military_dict):
                self.transform_military(transform_country, amount)
                return True

        # Transform alloys, perform check for feasibility on amount
        if output_resource == 'R21':
            alloys_dict = {'R1': 1 * amount, 'R2': 2 * amount, 'R5': 3 * amount, 'R7': 3 * amount}
            if transform_country.resource_check(alloys_dict):
                self.transform_alloys(transform_country, amount)
                return True

        # Transform housing
        if output_resource == 'R22':
            housing_dict = {'R1': 5 * amount, 'R2': 1 * amount, 'R3': 5 * amount, 'R4': 1 * amount,
                            'R7': 5 * amount,
                            'R21': 3 * amount, 'R5': 3 * amount}
            if transform_country.resource_check(housing_dict):
                self.transform_housing(transform_country, amount)
                return True

        # Transform food
        if output_resource == 'R23':
            food_dict = {'R1': 1 * amount, 'R4': 3 * amount, 'R23X': 1 * amount, 'R5': 1 * amount,
                         'R7': 3 * amount}
            if transform_country.resource_check(food_dict):
                self.transform_food(transform_country, amount)
                return True

        # Transform Fossil Energy
        if output_resource == 'R24':
            fossil_dict = {'R1': 2 * amount, 'R3': 3 * amount, 'R7': 3 * amount, 'R25': 2 * amount}
            if transform_country.resource_check(fossil_dict):
                self.transform_fossil_energy(transform_country, amount)
                return True

        # Transform electronics
        if output_resource == 'R25':
            elec_dict = {'R1': 1 * amount, 'R2': 3 * amount, 'R21': 2 * amount, 'R5': 3 * amount, 'R7': 3 * amount}
            if transform_country.resource_check(elec_dict):
                self.transform_electronics(transform_country, amount)
                return True

        # Transform Renewable Energy
        if output_resource == 'R26':
            renew_dict = {'R1': 2 * amount, 'R3': 3 * amount, 'R7': 2 * amount, 'R23X': 1 * amount, 'R25': 2 * amount}
            if transform_country.resource_check(renew_dict):
                self.transform_renewable_energy(transform_country, amount)
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
            self.__actions_path.append("(TRANSFER " + country1 + " " + country2 + " (("
                                       + self.get_resource_name(resource) + " " + str(amount) + "))")
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

    def get_undiscounted_reward(self, country, world2):
        initial_utility = sq.state_quality(country, self)
        final_utility = sq.state_quality(country, world2)
        return final_utility - initial_utility

    def get_discounted_reward(self, country, depth):
        # DR(c_i, s_j) = gamma^N * Q_end(c_i, s_j) – Q_start(c_i, s_j)), where 0 <= gamma < 1
        gamma = 0.99
        n = depth  # this is how many times the scheduler ran

        discount_reward = gamma ** n * self.get_undiscounted_reward(country)
        gamma -= .02

        return discount_reward

    def country_accept_prob(self, country, depth):
        l = 1
        x0 = 0
        k = 1
        discount_reward = self.get_discounted_reward(country, depth)
        prob = l / (1 + math.e ** (-k * (discount_reward - x0)))
        return prob

    def schedule_accept_prob(self, country, depth):
        prob_product = 0
        for x in range(depth - 1):
            if x == 1:
                prob_product = self.get_discounted_reward(country, depth)
                return prob_product
            else:
                prob_product *= self.get_discounted_reward(country, depth)
        return prob_product

    def expected_utility(self, country, depth):
        c = -0.3  # can change later
        probability = self.schedule_accept_prob(country, depth)
        discount_reward = self.get_discounted_reward(country, depth)

        expected_util = probability * discount_reward + ((1 - probability) * c)
        return expected_util

    # Default number of transforms is 1 (Population requirement is checked by verifying function)
    # Requires 5 population
    def transform_housing(self, transform_country, amount=1):
        # Decrease inputs
        transform_country.dec_resource("R4", 1 * amount)  # AvailableLand
        transform_country.dec_resource("R7", 5 * amount)  # Water
        transform_country.dec_resource("R2", 1 * amount)  # MetallicElements
        transform_country.dec_resource("R3", 5 * amount)  # Timber
        transform_country.dec_resource("R21", 3 * amount)  # MetallicAlloys
        transform_country.dec_resource("R5", 3 * amount)  # PotentialEnergyUsable

        # increase outputs (population unchanged)
        transform_country.inc_resource("R23", 1 * amount)  # Housing
        transform_country.inc_resource("R23X", 1 * amount)  # HousingWaste
        transform_country.inc_resource("R7", 4 * amount)  # Water

        self.__actions_path.append("(TRANSFORM " + transform_country.get_name() + " "
                                                                                  "\n\t(INPUTS (AvailableLand " + str(
            amount) + ") "
                      "(Population " + str(5 * amount) + ") (Water " + str(5 * amount) + ") "
                                                                                         "(MetallicElements " + str(
            amount) + ") (Timber " + str(5 * amount) + ") "
                                                       "(MetallicAlloys " + str(
            3 * amount) + ") (PotentialEnergyUsable " + str(5 * amount) + "))"
                                                                          "\n\t(OUTPUTS (Housing " + str(
            amount) + ") (HousingWaste " + str(amount) + ") "
                                                         "(Population " + str(5 * amount) + ") (Water " + str(
            4 * amount) + ")))")

    # Requires 1 population
    def transform_alloys(self, transform_country, amount=1):
        # Decrease inputs
        transform_country.dec_resource("R2", 2 * amount)  # MetallicElements
        transform_country.dec_resource("R5", 3 * amount)  # PotentialUsableEnergy
        transform_country.dec_resource("R7", 3 * amount)  # Water

        # increase outputs (population unchanged)
        transform_country.inc_resource("R21", 1 * amount)  # MetallicAlloys
        transform_country.inc_resource("R21X", 1 * amount)  # MetallicAlloysWaste
        transform_country.inc_resource("R7", 2 * amount)  # Water

        self.__actions_path.append("(TRANSFORM " + transform_country.get_name() + " "
                                                                                  "\n\t(INPUTS (AvailableLand " + str(
            amount) + ") "
                      "(Population " + str(5 * amount) + ") (Water " + str(5 * amount) + ") "
                                                                                         "(MetallicElements " + str(
            amount) + ") (Timber " + str(5 * amount) + ") "
                                                       "(MetallicAlloys " + str(
            3 * amount) + ") (PotentialEnergyUsable " + str(5 * amount) + "))"
                                                                          "\n\t(OUTPUTS (Housing " + str(
            amount) + ") (HousingWaste " + str(amount) + ") "
                                                         "(Population " + str(5 * amount) + ") (Water " + str(
            4 * amount) + ")))")

    # Requires 1 population
    def transform_electronics(self, transform_country, amount=1):
        # Decrease inputs
        transform_country.dec_resource("R2", 3 * amount)  # MetallicElements
        transform_country.dec_resource("R21", 2 * amount)  # MetallicAlloys
        transform_country.dec_resource("R5", 3 * amount)  # PotentialEnergyUsable
        transform_country.dec_resource("R7", 3 * amount)  # Water

        # increase outputs (population unchanged)
        transform_country.inc_resource("R25", 2 * amount)  # Electronics
        transform_country.inc_resource("R25X", 1 * amount)  # ElectronicsWaste

    # requires 2 population
    def transform_military(self, transform_country, amount=1):
        # Decrease inputs
        transform_country.dec_resource("R25", 2 * amount)  # Electronics
        transform_country.dec_resource("R22", 2 * amount)  # Housing
        transform_country.dec_resource("R23", 2 * amount)  # Food
        transform_country.dec_resource("R7", 1 * amount)  # Water

        # increase outputs (population unchanged)
        transform_country.inc_resource("R20", 2 * amount)  # Military
        transform_country.inc_resource("R20X", 1 * amount)  # MilitaryWaste

    # requires 1 population
    def transform_food(self, transform_country, amount=1):
        # Decrease inputs
        transform_country.dec_resource("R4", 3 * amount)  # AvailableLand
        transform_country.dec_resource("R23X", 1 * amount)  # FoodWaste as fertilizer
        transform_country.dec_resource("R5", 1 * amount)  # PotentialEnergyUsable
        transform_country.dec_resource("R7", 3 * amount)  # Water

        # increase outputs (population unchanged)
        transform_country.inc_resource("R23", 4 * amount)  # Food
        transform_country.inc_resource("R7", 1 * amount)  # Water
        transform_country.inc_resource("R23X", 2 * amount)  # FoodWaste

    # requires 2 population
    def transform_fossil_energy(self, transform_country, amount=1):
        # Decrease inputs
        transform_country.dec_resource("R3", 3 * amount)  # AvailableLand
        transform_country.dec_resource("R7", 3 * amount)  # Water
        transform_country.dec_resource("R25", 2 * amount)  # Electronics

        # increase outputs (population unchanged)
        transform_country.inc_resource("R24", 3 * amount)  # FossilEnergyUsable
        transform_country.inc_resource("R7", 1 * amount)  # Water
        transform_country.inc_resource("R24X", 2 * amount)  # FossilEnergyUsable

    # requires 2 population
    def transform_renewable_energy(self, transform_country, amount=1):
        # Decrease inputs
        transform_country.dec_resource("R3", 3 * amount)  # AvailableLand
        transform_country.dec_resource("R7", 2 * amount)  # Water
        transform_country.dec_resource("R23X", 1 * amount)  # FoodWaste for composting
        transform_country.dec_resource("R25", 2 * amount)  # Electronics

        # increase outputs (population unchanged)
        transform_country.inc_resource("R3", 2 * amount)  # AvailableLand
        transform_country.inc_resource("R7", 2 * amount)  # Water
        transform_country.inc_resource("R25", 1 * amount)  # Electronics
        transform_country.inc_resource("R26", 3 * amount)  # RenewableEnergyUsable
        transform_country.inc_resource("R26X", 1 * amount)  # RenewableEnergyUsableWaste
