import speech_recognition as sr
from geotext import GeoText
import webbrowser
import requests
import pyttsx3
import random
import json
import time

engine = pyttsx3.init()

# Opens a new tab and visits
# the specified website
def visit_Site(audio):

    if '.com' in audio or '.org' in audio:
        site = audio.partition("check ")[2]
        engine.say("Visiting " + str(site))
        engine.runAndWait()

        # Opens new tab to website
        webbrowser.open_new_tab("http://www." + str(site))

    else:
        site = audio.partition("check ")[2]
        engine.say("Visiting " + str(site))
        engine.runAndWait()

        # Opens new tab to website
        webbrowser.open_new_tab("http://www." + str(site) + ".com")

    time.sleep(3)


# Opens a new tab and performs a 
# Google search for the given query
def search_Google(audio):

    query = audio.partition("search ")[2]
    engine.say("Searching Google for: " + str(query))
    engine.runAndWait()

    # Opens Google with specified search
    webbrowser.open("https://www.google.com/search?q=" + str(query))

    time.sleep(3)


# Inititates a game of hangman with the user
def play_hangman():
    
    # All the possible words to guess
    words = ["pizza", "sleep", "bike", "apple", "tea",
             "", "facebook", "helsinki", "develope", "hammer"]

    # Picks a random word from the list
    word = random.choice(words)

    blanks = ["_"] * len(word)

    num_guesses = 0
    guesses = ""

    engine.say("Lets play hangman. You can only get 6 guesses wrong or else you lose. Let's begin")
    engine.runAndWait()
    time.sleep(2)

    while num_guesses != 6:

        exception = 0

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
            engine.say("What is your guess?")
            engine.runAndWait()
            rec.adjust_for_ambient_noise(source)
            audio = rec.listen(source)
            
        # Tries to recognize what the user said
        try:
            phrase = rec.recognize_google(audio)
            engine.say("Your guess was the letter " + str(phrase))
            engine.runAndWait
            print("\nYour guess: " + str(phrase))

        except sr.UnknownValueError:
            phrase = "Unable to recognize speech. Try again"
            engine.say(str(phrase))
            engine.runAndWait()
            exception = 1

    
        if not phrase.isalpha() and not exception:
            engine.say("Invalid guess, make sure your guess is only a letter.")
            engine.runAndWait()
        
        elif phrase.lower() == word:

            print("\n" + "*" * 37)
            print("YOU WON! The word was: " + str(word))
            print("*" * 37 + "\n")
            
            engine.say("YOU WON! The word was " + str(word))
            engine.runAndWait()

            print_Menu()
            time.sleep(1)
            return

        elif len(phrase.lower()) > 1 and phrase.lower() != word and not exception:

            engine.say("INCORRECT GUESS. " + str(phrase.lower()) + " is not the word.")
            engine.runAndWait()

            num_guesses += 1
            time.sleep(1)

        elif phrase.lower() not in word and not exception:

            engine.say("INCORRECT GUESS. The letter " + str(phrase.lower()) + " is not in the word.")
            engine.runAndWait()

            guesses += phrase.lower()

            num_guesses += 1
            time.sleep(1)

        elif phrase.lower() in word:

            guesses += phrase.lower()
            blanks = [word[x] if word[x] in guesses else '_' for x in range(len(word))]

            check = ""
            status = check.join(blanks)

            engine.say("CORRECT! The letter " + str(phrase.lower()) + " is in the word")
            engine.runAndWait()

            if status == word:
                print("\n" + "*" * 37)
                print("YOU WON! The word was: " + str(word))
                print("*" * 37 + "\n")
               
                engine.say("YOU WON! The word was: " + str(word))
                engine.runAndWait()

                print_Menu()
                time.sleep(1)
                return

    # Prints loser message if the user
    # gets 6 strikes
    print("\n" + ":( " * 11)
    print("YOU LOST! The word was: " + str(word))
    print(":( " * 11 + "\n")
    
    engine.say("YOU LOST! The word was: " + str(word))
    engine.runAndWait()
    
    print_Menu()
    time.sleep(1)



# Solves simple equations 
# using the eval() function
def calculate(audio):

    equation = str(audio)
    
    # Gets all the numbers from the user input speech
    nums = [int(i) for i in equation.split() if i.isdigit()]

    # Extract the whole expression from the user input speech
    expression = audio.partition("compute ")[2]


    if len(nums) > 1 and len(expression) > 0:    

        answer = eval(expression)

        rounded = round(answer, 2)

        engine.say(str(expression) + " is equal to: " + str(rounded))
        engine.runAndWait()

    else:
        engine.say("Sorry, can you say the equation one more time?")
        engine.runAndWait()

    time.sleep(1)



# Gets the current weather of the 
# specified city through the OpenWeatherMap API
def get_Weather(audio):

    my_API_key = "bcad6bb03994e7963067bad0a49294b9"

    # URL to the OpenWeatherMap API
    url = "http://api.openweathermap.org/data/2.5/weather?"

    # Uses the GeoText module to find the 
    # city in the user specified string
    extract_city = GeoText(audio)
    cities = extract_city.cities

    # If no city is found in the input,
    # throws an error.
    if len(cities) == 0:
        engine.say("Sorry, this city was not found.")
        engine.runAndWait()
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

        y = x["main"]

        # Converts to °F from Kelvin
        temp = y["temp"] 
        updated_temp = int(((int(temp) - 273.15) * 9/5) + 32)

        humidity = y["humidity"]

        WS = x["wind"]

        wind_speed = int(WS["speed"])

        WD = x["weather"] 

        weather_description = WD[0]["description"] 

        engine.say("It is currently " + str(updated_temp) + " degrees fahrenheit")
        engine.runAndWait()
        engine.say("With a " + str(humidity) + " percent humidity percentage")
        engine.runAndWait()
        engine.say("Wind speed is " + str(wind_speed) + " miles per hour")
        engine.runAndWait()
        engine.say("And it is currently " + str(weather_description))
        engine.runAndWait()

    else:
        engine.say("Sorry, this city does not exist in the database.")
        engine.runAndWait()

    time.sleep(2)



# Prints out main menu message
def print_Menu():

    print("*" * 60)
    print("COMMANDS:\n")
    print("- To visit a specific site say: Check \'_____\'")
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
           # engine.say("What would you like me to do? (speak loud and clear)")
            #engine.runAndWait()
            engine.say("Now Listening")
            engine.runAndWait()

            rec.adjust_for_ambient_noise(source)
            audio = rec.listen(source)
            
        # Tries to recognize what the user said
        # else, throws an error
        try:
            phrase = rec.recognize_google(audio)
            engine.say("You said: " + str(phrase))
            engine.runAndWait()
            print("\nYou said: " + str(phrase) + "\n")

        except sr.UnknownValueError:
            phrase = "Unable to recognize command. Try again....."
            engine.say(str(phrase))
            engine.runAndWait()
            exception = 1

        # Checks the recognized speech to see if it 
        # is a valid command, else throws error message
        if "check" in phrase:
            visit_Site(phrase)

        elif "search" in phrase:
            search_Google(phrase)

        elif "let's play" in phrase:
            play_hangman()

        elif "compute" in phrase:
            calculate(phrase)

        elif "weather" in phrase:
            get_Weather(phrase)

        elif "quit" in phrase:
            engine.say("Now exiting voice assistant.")
            engine.runAndWait()
            run = False

        elif not exception:
            engine.say(str(phrase) + " is not a valid command. Try again")
            engine.runAndWait()
        

if __name__ == '__main__':
    main()