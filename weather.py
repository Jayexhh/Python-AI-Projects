import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError:
        print("Sorry, I'm unable to access the Google Speech Recognition service. Please check your internet connection.")
        return ""

def get_weather(city_name):
    url = f'https://www.weather-forecast.com/locations/{city_name}/forecasts/latest'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_data = soup.find_all(class_='b-forecast__table-description-content')[0].text.strip()
        return weather_data
    else:
        return f"Sorry, couldn't find weather information for {city_name}. Please check the city name and try again."

def main():
    speak("Hello! I am your weather assistant. Please tell me the city name.")
    while True:
        city = recognize_speech()
        if city == "":
            continue
        elif city == 'exit':
            speak("Goodbye!")
            break
        else:
            speak("Let me check the weather for you.")
            weather_info = get_weather(city)
            speak(weather_info)
            speak("Do you want to know the weather of another city? If yes, please say the city name. Otherwise, say exit.")

if __name__ == "__main__":
    main()
