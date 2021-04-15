# File name: world.py
# Authors: Team 6 - Ludwik Huth, Mackenzie Macdonald, Divya Prabhakaran, Regan Siems, Kelly Wolfe
# Class: CS4269
# Date: March 14th, 2021
# Honor statement: We pledge on our honor that we have neither given nor received any unauthorized aid
# on this assignment.
# Project Part: 1
# Description: This file implements the World class


import copy  # Used to make deep copies of world objects
import math  # Used for the math operations in the expected utility function calculation
import statequality as sq  # Used to implement the expected utility methods

RAW_RESOURCES = ['R2', 'R3', 'R5']


# The world class models a current state of a game
# Its variables are the following:
# Countries: dict of countries (Country name: country object)
# Resources: dict of resources and weights (Resource name: resource weight)
# Resource_names: dict of resource abbreviations (as used in code) and resource string (necessary for printing)
# Path: a list keeping track of all actions in the world (transfers/transform) for scheduler
# Depth: length of the path
# Active_countries: a list of all countries that have been active (and thus need to accept a schedule)
class World:

    # Initializes the world and its attributes
    # self is the current instance of the world
    def __init__(self):
        self.__countries = {}
        self.__resources = {}
        self.__resource_names = {}
        self.__path = []
        self.__depth = 0
        self.__active_countries = []

    # This function gets the countries that are in this world
    # @param self is the current instance of the world
    # @return the active countries
    def get_active_countries(self):
        return self.__active_countries

    # This function sets the country to be active within the world
    # @param self is the current instance of the world
    # @param country is the country to set to active
    def set_active_country(self, country):
        if country not in self.__active_countries:
            self.__active_countries.append(country)

    # This function sets the countries into the world
    # @param self is the current instance of the world
    # @param countries are the countries to set
    def set_countries(self, countries):
        self.__countries = countries

    # This function fetches the country for access
    # @param self is the current instance of the world
    # @param country is the country to get
    # @return returns the country
    def get_country(self, country):
        return self.__countries[country]

    # This function adds a country's name to the world
    # @param self is the current instance of the world
    # @param country is the country to add
    def add_country(self, country):
        self.__countries[country.get_name()] = country

    # This function gets all of the countries in the world object
    # @param self is the current instance of the world
    # @return the countries dictionary
    def get_countries(self):
        return self.__countries

    # This function sets the resource for the world
    # @param self is the current instance of the world
    def set_resources(self, resources):
        self.__resources = resources

    # This function gets the resources of the world
    # @param self is the current instance of the world
    # @return the resources dictionary
    def get_resources(self):
        return self.__resources

    # This function sets the resource names in the world
    # @param self is the current instance of the world
    # @param resource_names are the names of the resources
    def set_resource_names(self, resource_names):
        self.__resource_names = resource_names

    # This function gets the resource
    # @param self is the current instance of the world
    # @param resource is the specific resource to get
    # @return the name of the resource in question (non-abbreviated)
    def get_resource_name(self, resource):
        return self.__resource_names[resource]

    # This function gets the weight of the resource
    # @param self is the current instance of the world
    # @param resource is the resource specified to get its weight
    # @return the weight of the resource in question
    def get_resource_weight(self, resource):
        return self.__resources[resource]

    def set_path(self, path):
        self.__path = path
        self.__depth = len(path)

    # This function gets the path and returns it
    # @param self is the current instance of the world
    # @return the current path of the world
    def get_path(self):
        return self.__path

    # This function gets the path as a string
    # @param self is the current instance of the world
    # @return the string of actions for the current world
    def get_path_as_string(self):
        action_str = ""
        for action in self.__path:
            action_str += action + "\n"
        return action_str

    # This function resets the path to nothing in it and a depth of zero to restart
    # @param self is the current instance of the world
    def reset_path(self):
        self.__depth = 0
        self.__path = []

    def reset_depth(self):
        self.__depth = 0

    # This function returns the depth
    # @param self is the current instance of the world
    # @return current depth (length of the actions path)
    def get_depth(self):
        return self.__depth

    # This function simulates the affects of a tornado on a country
    # Diminishes the housing and farm resources
    # @param self is the current instance of the world
    # @param country is the country where the tornado will take place
    def tornado(self, country):
        tornado_country = self.get_country(country)
        tornado_country.set_resource('R26', math.floor(tornado_country.get_resource_val('R26') * 0.8))
        tornado_country.set_resource('R23', math.floor(tornado_country.get_resource_val('R23') * 0.95))

    # This function simulates the affects of an earthquake on a country
    # Diminishes the housing resource
    # @param self is the current instance of the world
    # @param country is the country where the earthquake will take place
    def earthquake(self, country):
        earthquake_country = self.get_country(country)
        earthquake_country.set_resource('R23', math.floor(earthquake_country.get_resource_val('R23') * 0.9))

    # This function simulates the affects of a fire on a country
    # Diminishes the timber resource
    # @param self is the current instance of the world
    # @param country is the country where the fire will take place
    def fire(self, country):
        fire_country = self.get_country(country)
        fire_country.set_resource('R3', math.floor(fire_country.get_resource_val('R3') * 0.7))

    # This function simulates the affects of a hurricane on a country
    # Diminishes the electronics, housing, and farm resources
    # @param self is the current instance of the world
    # @param country is the country where the hurricane will take place
    def hurricane(self, country):
        hurricane_country = self.get_country(country)
        hurricane_country.set_resource('R22', math.floor(hurricane_country.get_resource_val('R22') * 0.9))
        hurricane_country.set_resource('R23', math.floor(hurricane_country.get_resource_val('R23') * 0.9))
        hurricane_country.set_resource('R26', math.floor(hurricane_country.get_resource_val('R26') * 0.8))

    # This function gets the country that has the most of the specified resource
    # @param self is the current instance of the world
    # @param resource is the resource to compare amounts of
    # @return the country with the most of that resource
    def get_max_resource(self, resource):
        max_country = ""
        max_count = -1
        for country in self.__countries:
            count = self.__countries[country].get_resource_val(resource)
            if count > max_count:
                max_country = country
                max_count = count
        return self.get_country(max_country)

    # This function gets the country that has the least of the specified resource
    # @param self is the current instance of the world
    # @param resource is the resource to compare amounts of
    # @return the country with the least amount of that resource
    def get_min_resource(self, resource):
        min_country = ""
        min_count = 10000
        for country in self.__countries:
            count = self.__countries[country].get_resource_val(resource)
            if count < min_count:
                min_country = country
                min_count = count
        return self.get_country(min_country)

    # This function checks if a given transformation is feasible for a certain country:
    # Either transforms and returns true, or returns false if transformation was not feasible
    # @param self is the current instance of the world
    # @param country is the country to pass in for the transform
    # @param output_resource is the desired output of the transform
    # @param amount is the desired amount of the desired resource
    # @return true/false, indicating whether the transform is successful
    def transform(self, country, output_resource, amount):
        transform_country = self.get_country(country)

        # Transform alloys, perform check for feasibility on amount
        if output_resource == 'R21':
            alloys_dict = {'R1': 1 * amount, 'R2': 2 * amount}
            if transform_country.resource_check(alloys_dict):
                self.transform_alloys(transform_country, amount)
                return True

        # Transform electronics
        if output_resource == 'R22':
            elec_dict = {'R1': 1 * amount, 'R2': 3 * amount, 'R21': 2 * amount}
            if transform_country.resource_check(elec_dict):
                self.transform_electronics(transform_country, amount)
                return True

        # Transform housing
        if output_resource == 'R23':
            housing_dict = {'R1': 5 * amount, 'R2': 1 * amount, 'R3': 5 * amount, 'R21': 3 * amount}
            if transform_country.resource_check(housing_dict):
                self.transform_housing(transform_country, amount)
                return True

        # Transform food
        if output_resource == 'R24':
            food_dict = {'R1': 1 * amount, 'R3': 3 * amount, 'R23': 1 * amount}
            if transform_country.resource_check(food_dict):
                self.transform_food(transform_country, amount)
                return True

        # Transform fossil energy
        if output_resource == 'R25':
            fossil_dict = {'R1': 3 * amount, 'R22': 2 * amount, 'R5': 1 * amount}
            if transform_country.resource_check(fossil_dict):
                self.transform_fossil(transform_country, amount)
                return True

        # Transform weapons
        if output_resource == 'R26':
            weapons_dict = {'R1': 6 * amount, 'R22': 2 * amount, 'R2': 3 * amount}
            if transform_country.resource_check(weapons_dict):
                self.transform_weapons(transform_country, amount)
                return True

        # Transform military
        if output_resource == 'R27':
            military_dict = {'R1': 1 * amount, 'R22': 12 * amount, 'R26': 12 * amount, 'R23': 5 * amount,
                             'R24': 10 * amount, 'R30': 5 * amount, 'R29': 3 * amount}
            if transform_country.resource_check(military_dict):
                self.transform_military(transform_country, amount)
                return True

        # Transform medicine
        if output_resource == 'R28':
            medicine_dict = {'R1': 5 * amount, 'R22': 6 * amount, 'R29': 2 * amount}
            if transform_country.resource_check(medicine_dict):
                self.transform_medicine(transform_country, amount)
                return True

        # Transform telecommunications
        if output_resource == 'R29':
            telecomm_dict = {'R1': 2 * amount, 'R22': 4 * amount, 'R21': 6 * amount}
            if transform_country.resource_check(telecomm_dict):
                self.transform_telecomm(transform_country, amount)
                return True

        # Transform transportation
        if output_resource == 'R30':
            transportation_dict = {'R1': 2 * amount, 'R25': 3 * amount, 'R22': 2 * amount}
            if transform_country.resource_check(transportation_dict):
                self.transform_transportation(transform_country, amount)
                return True

        return False

    # This function checks if a given transfer is feasible for a certain country:
    # Either transfers and returns true, or returns false if transfer was not feasible
    # @param self is the current instance of the world
    # @param country1 is the first country to do the transfer
    # (i.e. country which the resource comes from)
    # @param country2 is the country that the resource is going to
    # @param resource is the desired resource to transfer
    # @param is the desired amount of the resource to transfer
    # @return true/false indicating whether the transfer was successful
    def transfer(self, country1, country2, resource, amount, cur_country):
        tmp_world = copy.deepcopy(self)
        from_country = self.get_country(country1)
        to_country = self.get_country(country2)
        if from_country.resource_check(resource, amount):
            from_country.dec_resource(resource, amount)
            to_country.inc_resource(resource, amount)
            self.__depth += 1
            self.__path.append("(TRANSFER " + country1 + " " + country2 + " ("
                               + self.get_resource_name(resource) + " " + str(amount) + "))"
                               + " EU: " + str(self.expected_utility(cur_country, tmp_world)))
            self.set_active_country(country1)
            self.set_active_country(country2)

            return True
        else:
            return False

    # This function outputs the world state and the resources with their weights
    # @param self is the current instance of the world
    # @return a string representing the current state of the world
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

    # This function gets the undiscounted reward for transfers using the state quality function
    # @param self is the current instance of the world
    # @param country is the country for the reward
    # @param initial_world is the world instance prior to the transfer
    # @return the difference between final utility and initial utility
    def get_undiscounted_reward(self, country, initial_world):
        initial_utility = sq.state_quality(country, initial_world)
        final_utility = sq.state_quality(country, self)
        return final_utility - initial_utility

    # This function gets the discounted reward for the transfer
    # @self is the current instance of the world
    # @param country is the country for the reward calculation
    # @param intial_world is the world instance prior to the transfer
    # @return the discounted calculated reward value
    def get_discounted_reward(self, country, initial_world):
        gamma = 0.99
        n = self.__depth  # this is how many times the scheduler ran
        discount_reward = gamma ** n * self.get_undiscounted_reward(country, initial_world)
        return discount_reward

    # This function calculates the probability of a country accepting a transfer
    # @param self is the current instance of the world
    # @param country is the country for the probability to be calculated for
    # @param intial_world is the world instance prior to the transfer
    # @return the probability
    def country_accept_prob(self, country, initial_world):
        # Different constants, values determined through testing
        l = 1.0
        x0 = 0.0
        k = 5.0
        discount_reward = self.get_discounted_reward(country, initial_world)
        prob = l / (1.0 + math.e ** (-k * (discount_reward - x0)))  # Logistics function
        return prob

    # This function calculates the probability product of countries accepting the transfer for
    # the whole schedule
    # @param self is the current instance of the world
    # @param initial_world is the world instance prior to any changes
    # @return the probability that the active countries will all accept the schedule
    def schedule_accept_prob(self, inital_world):
        prob_product = 1
        countries = self.get_active_countries()

        # Calculate the product of all the countries' probabilities
        for country in countries:
            prob_product *= self.country_accept_prob(country, inital_world)
        return prob_product

    # This function calculates the expected utility
    # @param self is the current instance of the world
    # @param country is the country that the utility is calculated for
    # @param initial_world is the world instance prior to changes
    # @return the expected utility of the schedule
    def expected_utility(self, country, initial_world):
        c = -.5  # Low constant value since we have low expected utility values
        probability = self.schedule_accept_prob(initial_world)
        discount_reward = self.get_discounted_reward(country, initial_world)

        expected_util = probability * discount_reward + ((1 - probability) * c)
        return expected_util

    # This function does the work of transforming resources to housing
    # Requires 5 population
    # @param self is the current instance of the world
    # @param transform_country is the country performing the transform
    # @param amount is the desired amount, defaulted to 1
    def transform_housing(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R2", 1 * amount)  # MetallicElements
        transform_country.dec_resource("R3", 5 * amount)  # Timber
        transform_country.dec_resource("R21", 3 * amount)  # MetallicAlloys

        # increase outputs (population unchanged)
        transform_country.inc_resource("R23", 1 * amount)  # Housing
        transform_country.inc_resource("R23X", 1 * amount)  # HousingWaste

        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS ((Population " + str(amount) +
                           ") (MetallicElements " + str(amount) + ") (Timber " + str(5 * amount) +
                           ") (MetallicAlloys " + str(3 * amount) + "))  (OUTPUTS (Population " + str(amount) +
                           ") (Housing " + str(amount) + ") " + "(HousingWaste " + str(amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))

    # This function does the work of transforming resources into metallic alloys
    # Requires 1 population
    # @param self is the current instance of the world
    # @param transform_country is the country performing the transform
    # @param amount is the desired amount, defaulted to 1
    def transform_alloys(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R2", 2 * amount)  # MetallicElements

        # increase outputs (population unchanged)
        transform_country.inc_resource("R21", 1 * amount)  # MetallicAlloys
        transform_country.inc_resource("R21X", 1 * amount)  # MetallicAlloysWaste

        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS (Population " + str(amount) +
                           ") (MetallicElements " + str(2 * amount) + "))  (OUTPUTS (Population " + str(amount) +
                           ") (MetallicAlloys " + str(amount) + ") (MetallicAlloysWaste " + str(amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))

    # This function does the work to transform electronics from resources
    # Requires 1 population
    # @param self is the current instance of the world
    # @param transform_country is the country performing the transform
    # @param amount is the desired amount, defaulted to 1
    def transform_electronics(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R2", 3 * amount)  # MetallicElements
        transform_country.dec_resource("R21", 2 * amount)  # MetallicAlloys

        # increase outputs (population unchanged)
        transform_country.inc_resource("R22", 2 * amount)  # Electronics
        transform_country.inc_resource("R22X", 1 * amount)  # ElectronicsWaste

        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS (Population " + str(5 * amount)
                           + ") (MetallicElements " + str(3 * amount) + ") (MetallicAlloys " + str(2 * amount) +
                           ")) (OUTPUTS (Population " + str(5 * amount) + ") (Electronics " + str(2 * amount) +
                           ") (ElectonicsWaste " + str(amount) +
                           "))) EU: " + str(self.expected_utility(transform_country.get_name(), prior_world)))

    def transform_food(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R3", 3 * amount)  # Timber

        # increase outputs (population unchanged)
        transform_country.inc_resource("R24", 2 * amount)  # Food
        transform_country.inc_resource("R24X", 1 * amount)  # FoodWaste
        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS (Population " + str(amount)
                           + ") (Timber " + str(3 * amount) + ") (Housing " + str(amount) +
                           "))  (OUTPUTS (Population " + str(amount) + ") (Food " + str(2 * amount) +
                           ") (Housing " + str(amount) + ") (FoodWaste " + str(amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))

    def transform_waste(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R24X", 3 * amount)  # FoodWaste

        # increase outputs (population unchanged)
        transform_country.inc_resource("R26", 2 * amount)  # Fertilizer
        transform_country.inc_resource("R26X", 1 * amount)  # FertilizerWaste

        self.__depth += 1

        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS (Population " + str(amount)
                           + ") (FoodWaste " + str(3 * amount) + ")) (OUTPUTS (Population " + str(
            amount) + ") (Fertilizer " + str(2 * amount) +
                           ") (FertilizerWaste " + str(amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))

        # This function does the work of transforming resources to fossil fuel
        # Requires 3 population
        # @param self is the current instance of the world
        # @param transform_country is the country performing the transform
        # @param amount is the desired amount, defaulted to 1

    def transform_fossil(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R22", 2 * amount)  # Electronics

        # increase outputs (population unchanged)
        transform_country.inc_resource("R22", 1 * amount)  # Electronics
        transform_country.inc_resource("R25", 4 * amount)  # Fossil
        transform_country.inc_resource("R25X", 2 * amount)  # Fossil Waste

        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS ((Population " + str(3 * amount) +
                           ") (Electronics " + str(2 * amount) + ") (Renewable Energy " + str(1 * amount) + "))"
                            "(OUTPUTS (Population " + str(3 * amount) + ") (Electronics" + str(amount) + ") "
                            "(Renewable Energy " + str(amount) + ") (Fossil Energy" + str(4 * amount) + ") "
                            "(FossilWaste " + str(amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))

    # This function does the work of transforming resources to weapons
    # Requires 6 population
    # @param self is the current instance of the world
    # @param transform_country is the country performing the transform
    # @param amount is the desired amount, defaulted to 1
    def transform_weapons(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R22", 2 * amount)  # Electronics
        transform_country.dec_resource("R21", 3 * amount)  # Metallic Alloys

        # increase outputs (population unchanged)
        transform_country.inc_resource("R26", 5 * amount)  # Weapons
        transform_country.inc_resource("R26X", 3 * amount)  # Weapons Waste

        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS ((Population " + str(6 * amount) +
                           ") (Electronics " + str(2 * amount) + ") (Metallic Alloys " + str(3 * amount) + "))"
                           "(OUTPUTS (Population " + str(6 * amount) + ") (Weapons" + str(5 * amount) + ") "
                           "(WeaponsWaste " + str(3 * amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))

    # This function does the work of transforming into a military
    # Requires 12 population
    # @param self is the current instance of the world
    # @param transform_country is the country performing the transform
    # @param amount is the desired amount, defaulted to 1
    def transform_military(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R1", 10 * amount)  # Population
        transform_country.dec_resource("R22", 12 * amount)  # Electronics
        transform_country.dec_resource("R26", 12 * amount)  # Weapons
        transform_country.dec_resource("R23", 5 * amount)  # Housing
        transform_country.dec_resource("R24", 10 * amount)  # Food
        transform_country.dec_resource("R30", 5 * amount)  # Transportation
        transform_country.dec_resource("R29", 3 * amount)  # Telecommunications

        # increase outputs
        transform_country.inc_resource("R1", 7 * amount)  # Population
        transform_country.inc_resource("R22", 8 * amount)  # Electronics
        transform_country.inc_resource("R26", 6 * amount)  # Weapons
        transform_country.inc_resource("R23", 3 * amount)  # Housing
        transform_country.inc_resource("R30", 3 * amount)  # Transportation
        transform_country.inc_resource("R29", 2 * amount)  # Telecommunications
        transform_country.inc_resource("R27X", 4 * amount)  # Military Waste

        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS ((Population " + str(10 * amount) +
                           ") (Electronics " + str(12 * amount) + ") (Weapons " + str(12 * amount) + ") (Housing " +
                           str(5 * amount) + ") (Food " + str(10 * amount) + ") (Transportation " + str(5 * amount) +
                           ")(Telecommunications " + str(3 * amount) + "))" "(OUTPUTS (Population " + str(7 * amount) +
                           ") (Electronics " + str(8 * amount) + ") (Weapons " + str(6 * amount) + ") (Housing " +
                           str(3 * amount) + ") (Transportation " + str(3 * amount) + ") (Telecommunications " +
                           str(2* amount) + ") (MilitaryWaste " + str(4 * amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))

        # This function does the work of transforming resources to telecommunications
        # Requires 2population
        # @param self is the current instance of the world
        # @param transform_country is the country performing the transform
        # @param amount is the desired amount, defaulted to 1
    def transform_telecomm(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R22", 4 * amount)  # Electronics
        transform_country.dec_resource("R21", 6 * amount)  # Metallic Alloys

        # increase outputs (population unchanged)
        transform_country.inc_resource("R22", 2 * amount)  # Electronics
        transform_country.inc_resource("R21", 4 * amount)  # Metallic Alloys
        transform_country.inc_resource ("R29", 3 * amount)  # Telecommunications
        transform_country.inc_resource("R29X", 1 * amount)  # Telecommunications Waste

        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS ((Population " + str(2 * amount) +
                           ") (Electronics " + str(4 * amount) + ") (Metallic Alloys " + str(6 * amount) + "))"
                           "(OUTPUTS (Population " + str(2 * amount) + ") (Electronics" + str(2 * amount) + ") "
                           "(Metallic Alloys " + str(4 * amount) + ") (Telecommunications " + str(3 * amount) + ") "
                            "(TelecommunicationsWaste " + str(1 * amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))

    # This function does the work of transforming resources to medicine
    # Requires 5 population
    # @param self is the current instance of the world
    # @param transform_country is the country performing the transform
    # @param amount is the desired amount, defaulted to 1
    def transform_medicine(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R22", 6 * amount)  # Electronics
        transform_country.dec_resource("R29", 2 * amount)  # Telecommunications

        # increase outputs (population unchanged)
        transform_country.inc_resource("R22", 5 * amount)  # Electronics
        transform_country.inc_resource("R29", 2 * amount)  # Telecommunications
        transform_country.inc_resource("R28", 4 * amount)  # Medicine
        transform_country.inc_resource("R28X", 1 * amount)  # Medicine Waste

        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS ((Population " + str(5 * amount) +
                           ") (Electronics " + str(6 * amount) + ") (Telecommunications " + str(2 * amount) + "))"
                           "(OUTPUTS (Population " + str(5 * amount) + ") (Electronics" + str(5 * amount) + ") "
                           "(Telecommunications " + str(2 * amount) + ") (Medicine " + str(4 * amount) + ") "
                            "(MedicineWaste " + str(1 * amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))

# This function does the work of transforming resources to transportation
    # Requires 2 population
    # @param self is the current instance of the world
    # @param transform_country is the country performing the transform
    # @param amount is the desired amount, defaulted to 1
    def transform_transportation(self, transform_country, amount=1):
        prior_world = copy.deepcopy(self)

        # Decrease inputs
        transform_country.dec_resource("R25", 3 * amount)  # Fossil Energy
        transform_country.dec_resource("R22", 2 * amount)  # Electronics

        # increase outputs (population unchanged)
        transform_country.inc_resource("R22", 1 * amount)  # Electronics
        transform_country.inc_resource("R30", 3 * amount)  # Transportation
        transform_country.inc_resource("R30X", 1 * amount)  # Transportation Waste

        self.__depth += 1
        self.__path.append("(TRANSFORM " + transform_country.get_name() + " (INPUTS ((Population " + str(2 * amount) +
                           ") (Electronics " + str(2 * amount) + "))"
                           "(OUTPUTS (Population " + str(2 * amount) + ") (Electronics" + str(1 * amount) + ") "
                           "(Transportation " + str(3 * amount) + ") (TransportWaste " + str(1 * amount) + "))) EU: "
                           + str(self.expected_utility(transform_country.get_name(), prior_world)))


# FIXME do allocation of resources to everyone and then PASS is just an empty operation
def country_passes(self, country):
    self.__path.append("(PASSES " + country + " )")


# Adds ten percent of current value of all raw resources each turn (round function s.t. we don't get decmials)
def turn_resources(self):
    for country in self.__countries:
        cur = self.__countries[country]
        for resource in RAW_RESOURCES:
            cur.inc_resource(resource, round(0.1 * cur.get_resource_val(resource)))

