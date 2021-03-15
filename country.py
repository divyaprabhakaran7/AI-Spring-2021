# Group 6 - Ludwik Huth, Divya Prabhakaran, Kenzie Macdonald, Kelly Wolfe, Regan Seims
# CS 4269 Project Part 1
# Due March 14, 2021


# The country class is used to create the countries that will be interacting within our world

class Country:

    # This function initializes the country to itself
    # @param self is the country
    # @param name is the country name
    # @param resources is the dictionary of resources and the amount present
    def __init__(self, name, resources):
        self.__name = name
        self.__resources = resources

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
    def get_resources(self):
        return self.__resources

    # This function will allow the resources to be returned as a list
    # @param self is the country itself
    def get_resources_as_list(self):
        return list(self.__resources.values())

    # This function will return the value of the resource for a given company
    # @param self is the country itself
    # @param resource is the specific resource to find out the amount/value
    def get_resource_val(self, resource):
        return self.__resources[resource]

    # This function returns the name of the country
    # self is the country itself
    def get_name(self):
        return self.__name

    # Determine whether a country has a certain amount (or more) of a resource
    # overloaded to use dict if necessary (either input a single resource + an amount
    # or a dict of resources and amounts)

    # This function looks into country's resources and checks if meets the amount of resources
    # specified
    # @param self is the country itself
    # @param resource is the specific resource to check
    # @param amount is the amount to check the resource value against, default is none
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
