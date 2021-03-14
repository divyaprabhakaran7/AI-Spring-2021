#Test cases for the scheduler to run
def main():
my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_1.xslx', 'data/output_data.xslx',
                     5, 3, 10)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_2.xslx', 'data/output_data.xslx',
                     7, 4, 8)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_2.xslx', 'data/output_data.xslx',
                     5, 3, 10)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_3.xslx', 'data/output_data.xslx',
                     7, 4, 8)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_3.xslx', 'data/output_data.xslx',
                     5, 3, 10)

my_country_scheduler('Atlantis', 'data/resource_data.xslx', 'data/test_case_4.xslx', 'data/output_data.xslx',
                     7, 4, 8)

if __name__ == '__main__':
    main()