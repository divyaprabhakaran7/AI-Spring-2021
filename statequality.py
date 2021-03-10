import math


# threshold high = you don't need a lot of it to have a positive value
# weight high = important if you have more or less than you need
# threshold low = you need a lot of it for it to have a positive value
# weight low = not that important if you have more or less than you need
# high threshold, high weight = you don't need a lot of it but if you do have a lot you get big impact
# high threshold low weight = you don't need a lot of it and it dpesn't really matter if you have
# low threshold, high weight = you need a lot of it, and moving away from threshold has big impact
# low threshold, low weight = you need a lot of it but it isn't that big of an impact if you are more
# or less than you need

def state_quality(country, world):
    quality_country = world.get_country(country)
    resource_sum = 0
    for resource in quality_country.get_resources():
        resource_sum += world.get_resource_weight(resource) * quality_country.get_resource_val(resource)

    return resource_sum
