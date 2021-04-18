# File name: country.py
# Authors: Team 6 - Ludwik Huth, Mackenzie Macdonald, Divya Prabhakaran, Regan Siems, Kelly Wolfe
# Class: CS4269
# Date: March 14th, 2021
# Honor statement: We pledge on our honor that we have neither given nor received any unauthorized aid
# on this assignment.
# Project Part: 1
# Description: This file implements Country class


# The country class models a current country of a game
# Its variables are the following:
# name: the country's name
# resources: a dictionary of resources and correlating amounts
class Country:

    # This function initializes the country to itself
    # @param self is the country
    # @param name is the country name
    # @param resources is the dictionary of resources and the amount present
    def __init__(self, name, resources, disaster_prob):
        self.__name = name
        self.__resources = resources
        self.__disaster_prob = disaster_prob

    # This function sets the value for the resource
    # @param self is the country itself
    # @param resource is the specific resource within the dictionary of other resources
    # @param new_val is the value that the resource amount will be set to
    def set_resource(self, resource, new_val):
        self.__resources[resource] = new_val

    # This function decrements the value of a specific resource within the dictionary
    # @param self is the country itself
    # @param resource is the specific resource that will be decremented due to transfers and
    # transforms
    # @param amount is the amount to decrement from its original value
    def dec_resource(self, resource, amount):
        self.__resources[resource] -= amount

    # This function increments the value of a specific resource within the dictionary
    # @param self is the country itself
    # @param resource is the specific resource that will be incremented due to transfers and
    # transforms
    # @param amount is the amount to increment from its original value
    def inc_resource(self, resource, amount):
        self.__resources[resource] += amount

    # This function is used to return resources of the country
    # @param self is the country itself
    # @return dictionary of resources
    def get_resources(self):
        return self.__resources

    # This function will allow the resources to be returned as a list
    # @param self is the country itself
    # @return resource values as a list (array)
    def get_resources_as_list(self):
        return list(self.__resources.values())

    # This function will return the value of the resource for a given company
    # @param self is the country itself
    # @param resource is the specific resource to find out the amount/value
    # @return the amount for this resource
    def get_resource_val(self, resource):
        return self.__resources[resource]

    # This function returns the name of the country
    # @param self is the country itself
    # @return the country's name
    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        self.__name = new_name

    def get_disaster_prob(self):
        return self.__disaster_prob

    def set_disaster_prob(self, new_prob):
        self.__disaster_prob = new_prob

    # This function looks into country's resources and checks if meets the amount of resources specified
    # It is set up to accept either a dictionary of resource value pairs (when amount is not specified) or just one
    # resource and a value (specified as amount)
    # @param self is the country itself
    # @param resource is the specific resource to check
    # @param amount is the amount to check the resource value against, default is none
    # @return true/false indicating whether the country has sufficient resources
    def resource_check(self, resource, amount=None):
        if amount is None:
            for x in resource:
                if self.__resources[x] < resource[x]:
                    return False
            return True
        else:
            return self.__resources[resource] >= amount

    # This function allows us to return the name of the country along with the resources that it has
    # @param self is the country itself
    # @return country name and resources
    def __str__(self):
        name = self.get_name()
        resources = ""
        for resource in self.__resources:
            resources += str(resource) + ": " + str(self.__resources[resource]) + " "
        return '{:<15}{:>5}'.format(name, resources)
