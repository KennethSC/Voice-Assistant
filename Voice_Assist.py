import speech_recognition as sr
from geotext import GeoText
import webbrowser
import requests
import random
import json
import time

# Opens a new tab and visits
# the specified website
def visit_Site(audio):

    if '.com' in audio or '.org' in audio:
        site = audio.partition("visit ")[2]
        print("\nVisiting " + str(site))
        time.sleep(1)

        # Opens new tab to website
        webbrowser.open_new_tab("http://www." + str(site))

    else:
        site = audio.partition("visit ")[2]
        print("\nVisiting " + str(site))
        time.sleep(1)

        # Opens new tab to website
        webbrowser.open_new_tab("http://www." + str(site) + ".com")

    time.sleep(4)


# Opens a new tab and performs a 
# Google search for the given query
def search_Google(audio):

    query = audio.partition("search ")[2]
    print("Searching Google for: " + str(query))

    # Opens Google with specified search
    webbrowser.open("https://www.google.com/search?q=" + str(query))

    time.sleep(4)


# Inititates a game of hangman with the user
def play_hangman():
    
    # All the possible words to guess
    words = ["pizza", "sleep", "bike", "apple", "tea",
             "java", "facebook", "helsinki", "develope", "hammer"]

    # Picks a random word from the list
    word = random.choice(words)

    blanks = ["_"] * len(word)

    num_guesses = 0
    guesses = ""

    print("\nLets play hangman. You can only get 6 guesses wrong or else you lose.\n")
    time.sleep(3)

    while num_guesses != 6:

        # Prints out status of the current game
        print("\n" + "-" * 43)
        print("Strikes: " + str(num_guesses) + "/6")
        print("Status: ", end = '')
        print(*blanks, sep = ' ')
        print("\nGuesses: ", end ='')
        print(*guesses, sep = ' ')

        # Uses given methods from the 
        # speech recognition module
        rec = sr.Recognizer()
        mic = sr.Microphone()

        # Listens and get user input through internal Microphones
        with mic as source:
            print("\nWhat is your guess? (speak loud and clear)")
            print("Listening.....\n")
            rec.adjust_for_ambient_noise(source)
            audio = rec.listen(source)
            
        # Tries to recognize what the user said
        try:
            phrase = rec.recognize_google(audio)
            print("Your guess: " + str(phrase))

        except sr.UnknownValueError:
            phrase = "Unable to recognize speech. Try again....."
            print(phrase + "\n")

    
        if not phrase.isalpha():
            print("\nMake sure your guess is only a letter.")
        
        elif phrase.lower() == word:

            print("\n" + "*" * 37)
            print("YOU WON! The word was: " + str(word))
            print("*" * 37 + "\n")
            time.sleep(2)

            print_Menu()
            time.sleep(2)
            return

        elif len(phrase.lower()) > 1 and phrase.lower() != word:

            print("\nINCORRECT GUESS. " + str(phrase.lower()) + " is not the word.\n")

            num_guesses += 1
            time.sleep(1.5)

        elif phrase.lower() not in word:

            print("\nINCORRECT GUESS. " + str(phrase.lower()) + " is not in the word.\n")

            guesses += phrase.lower()

            num_guesses += 1
            time.sleep(1.5)

        elif phrase.lower() in word:

            guesses += phrase.lower()
            blanks = [word[x] if word[x] in guesses else '_' for x in range(len(word))]

            check = ""
            status = check.join(blanks)

            if status == word:
                print("\n" + "*" * 37)
                print("YOU WON! The word was: " + str(word))
                print("*" * 37 + "\n")
                time.sleep(2)

                print_Menu()
                time.sleep(2)
                return

    # Prints loser message if the user
    # gets 6 strikes
    print("\n" + ":( " * 11)
    print("YOU LOST! The word was: " + str(word))
    print(":( " * 11 + "\n")
    time.sleep(1.5)
    
    print_Menu()
    time.sleep(2)



# Solves a simple two number equation
def calculate(audio):

    equation = str(audio)
    
    # Gets all the numbers from the user input string
    nums = [int(i) for i in equation.split() if i.isdigit()]

    if len(nums) == 2:
        expression = audio.partition("compute ")[2]
        print("\n" + str(expression) + " is equal to: ", end = '')

        print(eval(expression))

    elif len(nums) != 2:
        print("\nSorry, I can only solve equations of two numbers for now")
        return

    else:
        print("\nSorry, can you say the equation one more time?")

    time.sleep(2)


# Gets the current weather of
# the specified city through the 
# OpenWeatherMap API
def get_Weather(audio):

    my_API_key = "YOUR OPEN_WEATHER_MAP API KEY"

    # URL to the OpenWeatherMap API
    url = "http://api.openweathermap.org/data/2.5/weather?"

    # Uses the GeoText module to find the 
    # city in the user specified string
    extract_city = GeoText(audio)
    cities = extract_city.cities

    # If no city is found in the input,
    # throws an error.
    if len(cities) == 0:
        print("Sorry, this city was not found.")
        return
    else:
        city = cities[0]
  
    complete_url = url + "appid=" + my_API_key + "&q=" + city 

    # Gets the response from the API
    response = requests.get(complete_url) 
    x = response.json()

    # Gets weather data for the 
    # specified city
    if x["cod"] != "404":

        print("\nWeather in " + str(city) + ": \n")

        y = x["main"]

        # Converts to °F from Kelvin
        temp = y["temp"] 
        updated_temp = int(((int(temp) - 273.15) * 9/5) + 32)

        humidity = y["humidity"]

        WS = x["wind"]

        wind_speed = int(WS["speed"])

        WD = x["weather"] 

        weather_description = WD[0]["description"] 

        print("- Temperature (fahrenheit): " + str(updated_temp) + "°F")
        print("- Humidity (percentage): " + str(humidity) + "%")
        print("- Wind speed (mph): " + str(wind_speed) + " mph")
        print("- Description: " + str(weather_description))

    else:
        print("Sorry, this city does not exist in the database.")

    time.sleep(2)


# Prints out main menu message
def print_Menu():

    print("*" * 60)
    print("COMMANDS:\n")
    print("- To visit a specific site say: Visit \'_____\'")
    print("- To do a Google search say:    Search \'_____\'")
    print("- To play hangman game say:     Lets play")
    print("- To solve an equation say:     Compute \'__\' + - * / \'__\'")
    print("- To get the weather say:       Weather in YOUR CITY")
    print("- To exit voice assistant say:  Quit")
    print("*" * 60)



# Main driver function
def main():

    print_Menu()

    input("\nPress \'Enter\' to continue.\n")

    run = True

    while run:

        # Uses given methods from the 
        # speech recognition module
        rec = sr.Recognizer()
        mic = sr.Microphone()
        exception = 0

        # Gets user input through internal Microphones
        with mic as source:
            print("\nWhat would you like to do? (speak loud and clear)")
            print("Listening.....\n")
            rec.adjust_for_ambient_noise(source)
            audio = rec.listen(source)
            
        # Tries to recognize what the user said
        # else, throws an error
        try:
            phrase = rec.recognize_google(audio)
            print("You said: " + str(phrase))

        except sr.UnknownValueError:
            phrase = "Unable to recognize command. Try again....."
            print(phrase)
            exception = 1

        # Checks the recognized speech to see
        # if it is a valid command, else
        # throws error message
        if phrase.split()[0] == "visit":
            visit_Site(phrase)

        elif phrase.split()[0] == "search":
            search_Google(phrase)

        elif phrase == "let's play":
            play_hangman()

        elif phrase.split()[0] == "compute":
            calculate(phrase)

        elif "weather" in phrase:
            get_Weather(phrase)

        elif "quit" in phrase:
            print("\nNow exiting voice assistant.\n")
            run = False

        elif not exception:
            print("\n" + str(phrase) + " is not a valid command. Try again.....")
            exception = 0
            time.sleep(2)
        


if __name__ == '__main__':
    main()





