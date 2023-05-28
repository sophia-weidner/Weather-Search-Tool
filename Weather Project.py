# DSC 510
# Week 12
# Final Project
# Sophie Weidner
# 6/4/2022

#  Function to check errors - checks overall request exceptions, http errors and connection errors.
#  If connection is successful, function returns the response.
def check_errors(requests, url):
    try:
        response = requests.get(url)
        return response
    except requests.exceptions.RequestException:
        print("There was an issue handling your request.")
    except requests.exceptions.HTTPError:
        print("An HTTP Error occurred.")
    except requests.exceptions.ConnectionError:
        print("There was an error with your connection.")


#  This function goes through the API JSON dictionary and assigns different variables to the wanted pieces
#  of information, such as current temperature, low temperature, etc.
def name_variables(json_dictionary):
    #  Goes to dictionary and finds name of city.
    city_name = json_dictionary.get('name')
    #  If the city name exists, then assigns different variables. If the user inputs an invalid zipcode
    #  or city name, then the program will not assign these variables and will print an error message
    #  instead.
    if city_name:
        #  load_main calls the 'main' dictionary from json_dictionary and makes it into a new one. From there,
        #  variables are assigned.
        load_main = json_dictionary['main']
        current_temp = load_main['feels_like']
        high_temp = load_main['temp_max']
        low_temp = load_main['temp_min']
        pressure = load_main['pressure']
        humidity = load_main['humidity']

        #  load_weather_one and load_weather_two function the same as above, except when json_dictionary['weather']
        #  is called, it was a list. I then use load_weather_two to start at index 0, and I'm able
        #  to assign variables from there. I pprinted json_dictionary to find this out and troubleshooted
        #  from there.

        load_weather_one = json_dictionary['weather']
        load_weather_two = load_weather_one[0]
        description = load_weather_two['description']
        cloud_cover = load_weather_two['main']

        #  The next section prints the wanted information from the assigned variables above. All of this
        #  information was retrieved from the API.
        print("_______________________________")
        print(f"The current weather for {city_name}, is: \n"
              f"Current Temperature: {current_temp} degrees \n"
              f"High Temp: {high_temp} degrees \n"
              f"Low Temp: {low_temp} degrees \n"
              f"Pressure: {pressure}Pa \n"
              f"Humidity: {humidity}% \n"
              f"Cloud Cover: {cloud_cover} \n"
              f"Description: {description}.")
        print("_______________________________")
    #  If the city name doesn't load, this is the error message that prints.
    else:
        print("Invalid entry. Please try again.")


#  Function that retrieves API information if the user decides to input a zipcode.
def get_weather_zipcode(zip, appid, units):
    import json
    import requests
    #  url is assigned based on just zip and units, appid is defined in main function
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip},us&appid={appid}&units={units}"

    # calls function to check for errors. If the function is successful, it will parse the JSON dictionary
    # and send it into the name_variables function to organize the information.
    if check_errors(requests, url):
        print(f"Connection to {url} was successful.")
        response = requests.get(url)
        parsed = json.loads(response.text)
        json_pretty = json.dumps(parsed, indent=4, sort_keys=True)
        json_dictionary = json.loads(json_pretty)

        name_variables(json_dictionary)
    #  If the function is not successful, it will print the error message below.
    else:
        print("Connection was unsuccessful. Please check connection or check that your"
              " input is valid.")


#  If the user decides to get information based on city or state, this function will be used instead
def get_weather_city_state(city, state, appid, units):
    import json
    import requests
    #  URL is based on city, state, and units as well as appid defined in main.
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},us&appid={appid}&units={units}"

    #  This next block of code is the exact same as the function above. I attempted to put this into a function,
    #  but I couldn't get it to work. Despite it being repeated, I've found that the code works this way and
    #  would rather have a functioning program that looks a little clunky.
    if check_errors(requests, url):
        print(f"Connection to {url} was successful.")
        response = requests.get(url)
        parsed = json.loads(response.text)
        json_pretty = json.dumps(parsed, indent=4, sort_keys=True)
        json_dictionary = json.loads(json_pretty)

        name_variables(json_dictionary)
    else:
        print("Connection was unsuccessful. Please check connection or check that your"
              " input is valid.")


# Defining the main function
def main():
    # Assigning the appid given by the API.
    appid = "1ec1136115215225a8852501359fe391"
    # Prints welcome message and requirements for the program.
    print("Welcome to the Weather forecaster!")
    print("You must enter a city and state or a zipcode to receive the weather.")
    # While loop that allows user to look up the weather as many times as they'd like.
    while True:
        entrance = input("Would you like to look up the weather? Enter 'Y' to continue or any key to exit: ")
        # If the user inputs 'y', they will then be prompted to enter 1 or 2 based on whether they wish
        # to look up the weather by zipcode or city/state.
        if entrance.upper() == 'Y':
            zip_or_city = input("Please enter 1 for lookup by zipcode or 2 for lookup by city/state: ")
            #  The next code runs if user chooses to input zipcode.
            if zip_or_city == "1":
                zip = input("Please enter the zip code: ")
                #  Assigns units to the temperature and alters the URL.
                units = input("Please enter an F for Fahrenheit, C for Celsius or any other key for Kelvin: ")
                if units.upper() == "F":
                    units = 'imperial'
                elif units.upper() == "C":
                    units = 'metric'
                else:
                    units = 'standard'
                # Call to zipcode function
                get_weather_zipcode(zip, appid, units)
            # The next code runs if user chooses to input city/state.
            elif zip_or_city == "2":
                city = input("Please enter your city name: ")
                # Separate while loop that ensures the user enters the state code and not the entire state
                # ex: FL is acceptable while Florida is not.
                while True:
                    state = input("Please enter your state code: ")
                    if len(state) == 2:
                        break
                    else:
                        print("Invalid entry. Please enter your two letter state code.")
                # User will input temperature units desired.
                units = input("Please enter F for Fahrenheit, C for Celsius or any other key for Kelvin: ")
                if units.upper() == 'F':
                    units = 'imperial'
                elif units.upper() == 'C':
                    units = 'metric'
                else:
                    units = 'standard'
                # Call to city/state function.
                get_weather_city_state(city, state, appid, units)
            else:
                # If the user does not input 1 for zipcode or 2 for city/state, this message will print
                #  to the screen.
                print("Please enter 1 or 2 to continue.")
        else:
            # If the user enters any key, the program will end and print this message.
            print("Thank you for using the program.")
            break


#  Call to main.
if __name__ == "__main__":
    main()
