import sys
from itertools import count

import build_data
import county_demographics

from data import CountyDemographics

#gets the county demographics data
counties = build_data.get_data()
print(len(counties), "records loaded")

#opens the file given in the command line
try:
    operation = open(sys.argv[1], "r")
    code = operation.readlines()
#prints an error statement if there is no argument given or the text file doesn't exist
except IOError as e:
    print("Error: ", e)
    exit()
except IndexError as e:
    print("Error: ", e)
    exit()

#makes a list for filtered data to be appended to and count for the line number if there's an error
result = build_data.get_data()
count = 0
#reads each line of the text file seperately and splits the task from the colon
for line in code:
    line = line.strip("\n")
    count += 1
    comps = line.split(":")

    if "" == comps[0]:
        continue
    elif "filter-state" == comps[0]:
        result = []
        state = comps[1]
        for county in counties:
            if county.state == state:
                result.append(county)
        print("Filter: state == " + state + " (" + str(len(result)) + " entries)")

    elif "filter-gt" == comps[0]:
        result = []
        field = comps[1]
        seperated_field = field.split(".")
        num = float(comps[2])
        for county in counties:
            if seperated_field[0] == "Education":
                if county.education[seperated_field[1]] > num:
                    result.append(county)
            elif seperated_field[0] == "Ethnicities":
                if county.ethnicities[seperated_field[1]] > num:
                    result.append(county)
            elif seperated_field[0] == "Income":
                if county.income[seperated_field[1]] > num:
                    result.append(county)
        print("Filter: " + str(field) + " gt " + str(num) + " (" + str(len(result)) + " entries)")

    elif "filter-lt" == comps[0]:
        result = []
        field = comps[1]
        seperated_field = field.split(".")
        num = float(comps[2])
        for county in counties:
            if seperated_field[0] == "Education":
                if county.education[seperated_field[1]] < num:
                    result.append(county)
            elif seperated_field[0] == "Ethnicities":
                if county.ethnicities[seperated_field[1]] < num:
                    result.append(county)
            elif seperated_field[0] == "Income":
                if county.income[seperated_field[1]] < num:
                    result.append(county)
        print("Filter: " + str(field) + " lt " + str(num) + " (" + str(len(result)) + " entries)")

    elif "population-total" == comps[0]:
        sum = 0
        for county in counties:
            sum += county.population["2014 Population"]
        print("2014 population:", sum)

    elif "population" == comps[0]:
        field = comps[1]
        seperated_field = field.split(".")
        sum = 0
        for county in result:
            if seperated_field[0] == "Education":
                sum += (county.population * county.education[seperated_field[1]] / 100)
                print("2014 " + field + " population: " + str(sum))
            elif seperated_field[0] == "Ethnicities":
                sum += (county.population * county.ethnicities[seperated_field[1]] / 100)
                print("2014 " + field + " population: " + str(sum))
            elif seperated_field[0] == "Income":
                sum += (county.population * county.income[seperated_field[1]] / 100)
                print("2014 " + field + " population: " + str(sum))


    elif "percent" == comps[0]:
        field = comps[1]
        seperated_field = field.split(".")
        total_pop = 0
        field_pop = 0
        for county in result:
            if seperated_field[0] == "Education":
                total_pop += county.population["2014 Population"]
                field_pop += (county.population["2014 Population"] * county.education[seperated_field[1]] / 100)
            elif seperated_field[0] == "Ethnicities":
                total_pop += county.population["2014 Population"]
                field_pop += (county.population["2014 Population"] * county.ethnicities[seperated_field[1]] / 100)
            elif seperated_field[0] == "Income":
                total_pop += county.population["2014 Population"]
                field_pop += (county.population["2014 Population"] * county.income[seperated_field[1]] / 100)
        try:
            print("2014 " + field + " percentage: " + str(field_pop / total_pop * 100))
        except ZeroDivisionError:
            print("2014 " + field + " percentage: 0")

    elif comps[0] == "display":
        for demographic in result:
            print(demographic)
