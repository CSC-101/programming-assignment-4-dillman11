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

#skips the line if it's empty
    if "" == line:
        continue

#checks if the line shows display and if it is it prints each counties information from the result list
#prints an error if the lines malformed
    elif comps[0] == "display":
        if len(comps) == 1:
            for demographic in result:
                print(demographic)
        else:
            print("Error: line " + str(count) + " is malformed")

#checks if the line shows "filter-state"
#if it does, it filters the full data set into the counties that match the given state
#prints an error if the lines malformed
    elif "filter-state" == comps[0]:
        result = []
        if len(comps) == 2:
            state = comps[1]
            for county in counties:
                if county.state == state:
                    result.append(county)
            print("Filter: state == " + state + " (" + str(len(result)) + " entries)")
        else:
            print("Error: line " + str(count) + " is malformed")

# checks if the line shows "filter-gt"
# if it does, it filters the full data set into the counties that have the given field greater than the number given
#prints an error if the lines malformed (if there are more or less comps, if the field doesn't exist)
    elif "filter-gt" == comps[0]:
        result = []
        if len(comps) == 3:
            field = comps[1]
            seperated_field = field.split(".")
            try:
                num = float(comps[2])
                if num > 0 and num < 100 and len(seperated_field) == 2 and (seperated_field[0] == "Education"
                                    or seperated_field[0] == "Ethnicities" or seperated_field[0] == "Income"):
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
                else:
                    print("Error: line " + str(count) + " is malformed")
            except:
                print("Error: line " + str(count) + " is malformed")
        else:
            print("Error: line " + str(count) + " is malformed")

# checks if the line shows "filter-lt"
# if it does, it filters the full data set into the counties that have the given field less than the number given
# prints an error if the lines malformed (if there are more or less comps, if the field doesn't exist)
    elif "filter-lt" == comps[0]:
        result = []
        if len(comps) == 3:
            field = comps[1]
            seperated_field = field.split(".")
            try:
                num = float(comps[2])
                if num > 0 and num < 100 and len(seperated_field) == 2 and (seperated_field[0] == "Education"
                                            or seperated_field[0] == "Ethnicities" or seperated_field[0] == "Income"):
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
                else:
                    print("Error: line " + str(count) + " is malformed")
            except:
                print("Error: line " + str(count) + " is malformed")
        else:
            print("Error: line " + str(count) + " is malformed")

#checks if line shows "population-total"
#prints the total population of all counties in the result list
#prints an error if line is malformed
    elif "population-total" == comps[0]:
        sum = 0
        if len(comps) == 1:
            for county in result:
                sum += county.population["2014 Population"]
            print("2014 population:", sum)
        else:
            print("Error: line " + str(count) + " is malformed")

#checks if line shows "population"
#prints the population of all the people in the given field for each county
#prints an error if line is malformed
    elif "population" == comps[0]:
        sum = 0
        if len(comps) == 2:
            field = comps[1]
            seperated_field = field.split(".")
            try:
                for county in result:
                    if seperated_field[0] == "Education":
                        sum += (county.population["2014 Population"] * county.education[seperated_field[1]] / 100)
                    elif seperated_field[0] == "Ethnicities":
                        sum += (county.population["2014 Population"] * county.ethnicities[seperated_field[1]] / 100)
                    elif seperated_field[0] == "Income":
                        sum += (county.population["2014 Population"] * county.income[seperated_field[1]] / 100)
                    else:
                        print("Error: line " + str(count) + " is malformed")
                        break
            except KeyError:
                 print("Error: line " + str(count) + " is malformed")
            if sum != 0:
                print("2014 " + field + " population: " + str(sum))
        else:
            print("Error: line " + str(count) + " is malformed")

#checks if line shows "percent"
#prints the percent of the population of people in the given field for each county in the result list divided by the total population in the result list
#prints an error if line is malformed
    elif "percent" == comps[0]:
        total_pop = 0
        field_pop = 0
        if len(comps) == 2:
            field = comps[1]
            seperated_field = field.split(".")
            try:
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
                    else:
                        print("Error: line " + str(count) + " is malformed")
                        break
                try:
                    print("2014 " + field + " percentage: " + str(field_pop / total_pop * 100))
                except ZeroDivisionError:
                    print("Error: divided by 0")
            except KeyError:
                print("Error: line " + str(count) + " is malformed")
        else:
            print("Error: line " + str(count) + " is malformed")

#prints an error statement if the operation does not exist
    else:
        print("Error: line " + str(count) + " is malformed")

operation.close()
