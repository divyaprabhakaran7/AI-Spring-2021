class Country:

    # Name: string with country name
    # Resources: Dictionary of resources and the amount present
    def __init__(self, name, resources):
        self.__name = name
        self.__resources = resources

    def set_resource(self, resource, newVal):
        self.__resources[resource] = newVal

    def get_resources(self):
        return self.__resources

    def get_name(self):
        return self.__name

    def __str__(self):
        name = self.get_name()
        resources = ""
        for resource in self.__resources:
            resources += str(resource) + ": " + str(self.__resources[resource]) + " "
        return '{:<20}{:>4}'.format(name, resources)