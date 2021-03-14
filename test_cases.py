#Test cases for the scheduler to run
def test_cases():
my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_1.xslx', 'data/output_data1-1.xslx',
                     5, 3, 10)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_2.xslx', 'data/output_data1-2.xslx',
                     7, 4, 8)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_2.xslx', 'data/output_data2-1.xslx',
                     5, 3, 10)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_3.xslx', 'data/output_data2-2.xslx',
                     7, 4, 8)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_3.xslx', 'data/output_data3-1.xslx',
                     5, 3, 10)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_4.xslx', 'data/output_data3-2.xslx',
                     7, 4, 8)
