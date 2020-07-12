## Description

Using the SpeechRecognition module, this python script takes in user input speech through your device's microphone and is able to perform a variety of commands based off that input and ouptut the response through your device's speakers. This voice assistant is able to visit websites, search Google, give you the weather of your city, solve simple equations, and even play a game of hangman with the user, all with the sound of your voice.

## Requirements

To give SpeechRecognition access to your device's microphone, you will need to install pyaudio. For Mac users, you will first need to install portaudio by using this command in your terminal: **brew install portaudio**

And to now install pyaudio use this command in your terminal: **pip install pyaudio**

You will also need an API key from the Open Weather Map API. To do this just create a free account and get your API key from: <https://openweathermap.org/api>.

To install the rest of the requirements use this command in the directory where you stored the requirements.txt file: **pip install -r requirements.txt**


## Usage

After installing all required packages, just run Voice_Assist.py in your terminal or any other python interpreter that has access to your device's microphones and ask away.

