class Country:

    # Name: string with country name
    # Resources: Dictionary of resources and the amount present
    def __init__(self, name, resources):
        self.__name = name
        self.__resources = resources

    def set_resource(self, resource, new_val):
        self.__resources[resource] = new_val

    def dec_resource(self, resource, amount):
        self.__resources[resource] -= amount

    def inc_resource(self, resource, amount):
        self.__resources[resource] += amount

    def get_resources(self):
        return self.__resources

    def get_resource_val(self, resource):
        return self.__resources[resource]

    def get_name(self):
        return self.__name

    def __str__(self):
        name = self.get_name()
        resources = ""
        for resource in self.__resources:
            resources += str(resource) + ": " + str(self.__resources[resource]) + " "
        return '{:<15}{:>5}'.format(name, resources)