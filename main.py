import pyttsx3
import speech_recognition as sr
from googletrans import Translator
import webbrowser
import datetime
import pyjokes
import wikipedia
import smtplib
import os
import pywhatkit 
import requests
from youtubesearchpython import VideosSearch
import random
import cv2 
import time
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import threading
import openai

def virtual_assistant():
    while True:
        print("Virtual Assistant is running...")
        time.sleep(1)  

def run_gui():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Virtual Assistant")

        # Load the animated GIF
        self.gif = Image.open("ai.gif")
        self.frames = []
        try:
            while True:
                self.frames.append(ImageTk.PhotoImage(self.gif.copy().convert("RGBA")))
                self.gif.seek(len(self.frames))
        except EOFError:
            pass

        # Display the GIF
        self.label = tk.Label(master)
        self.label.pack()

        # Start the animation
        self.animate(0)

    def animate(self, frame):
        self.label.config(image=self.frames[frame])
        self.master.after(100, lambda: self.animate((frame + 1) % len(self.frames)))

engine=pyttsx3.init('sapi5')
voice=engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voice[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def TranslationHinToEng(text):
    line = str(text)
    translate = Translator()
    result = translate.translate(line)
    data1=result.text
    print(f"You:{data1}")
    return data1
    
def MicExcecution():
    query=sptxt()
    data=TranslationHinToEng(query)
    return data

def get_weather(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    weather_data = response.json()

    if response.status_code == 200:
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        speak(f"The current temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        error_message = weather_data.get('message', 'Unknown error')
        speak(f"Sorry, couldn't fetch the weather information. Error code: {response.status_code}, Message: {error_message}")

def get_top_news(api_key,num_headlines=10):
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'  
    response = requests.get(url)
    news_data = response.json()

    headlines = []

    if news_data['status'] == 'ok':
        articles = news_data['articles']
        for idx, article in enumerate(articles, start=1):
            if idx > num_headlines:
                break
            title = article['title']
            headlines.append(title)

    return headlines


def send_whatsapp_message(contact, message, country_code):
    if not country_code.startswith('+'):
        country_code = '+' + country_code
    full_contact = f"{country_code}{contact}"
    pywhatkit.sendwhatmsg_to_group(full_contact, message, datetime.datetime.now().hour, datetime.datetime.now().minute + 1)


def play_song(song_name):
    videosSearch = VideosSearch(song_name, limit = 1)
    result = videosSearch.result()
    if result['result']:
        song_url = result['result'][0]['link']
        webbrowser.open(song_url)
    else:
        speak("Sorry, couldn't find the song.")


def recommend_movie(genre):
    movies = {
        'action': ['The Dark Knight', 'Inception', 'Gladiator'],
        'comedy': ['The Hangover', 'Superbad', 'Anchorman'],
        'drama': ['The Shawshank Redemption', 'Forrest Gump', 'The Godfather'],
        'romance': ['Titanic', 'The Notebook', 'Pride and Prejudice'],
        'horror': ['The Conjuring', 'Get Out', 'A Quiet Place']
    }

    genre_movies = movies.get(genre.lower(), [])

    if genre_movies:
        movie = random.choice(genre_movies)
        speak(f"I recommend the movie {movie}.")
    else:
        speak("Sorry, couldn't find any movies in that genre.")

def take_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_image.jpg", frame)
        print("Image captured successfully")
    else:
        print("Error: Failed to capture image")
    cap.release()
    cv2.destroyAllWindows()


def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning !")

    elif hour>=12 and hour<18:
        speak("Good afternoon !")

    else:
        speak("Good evening !")
    speak("I am Proxima your A.I powered assistant . please tell how may i help u")

def sptxt(): 
    recognizer = sr.Recognizer()
    with sr.Microphone() as sourse:
        print("Listening.....")
        recognizer.adjust_for_ambient_noise(sourse)
        audio=recognizer.listen(sourse)
        try: 
            print("recognizing...")
            data=recognizer.recognize_google(audio)
            print(data)
            return data
        except sr.UnknownValueError:
            print("Not Understand")

to={"prabhat":"prabhatkainthola91@gmail.com","sarthak":"rsarthak100@gmail.com","ranjeet":"Sahranjeet435@gmail.com"}
    
def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('prabhatkainthola91@gmail.com','ovbd vlpk btwk swab')
    server.sendmail("prabhatkainthola91@gmail.com",to,content)
    server.close()

if __name__ == "__main__":

    gui_thread = threading.Thread(target=run_gui)
    gui_thread.start()
    wishMe()
    while True:
        data=sptxt().lower()
        data=MicExcecution().lower()


        if "who are you" in data:
            name="my name is proxima . I am a virtual assistant that can do many work for you sir"
            speak(name)

        elif "who built you" in data:
            build="prabhat kainthola"
            speak(build)

        elif "my name" in data:
            my_name="prabhat kainthola"
            speak(my_name)


        elif "my birth date" in data:
            birth_date="23 july 2002"
            speak(birth_date)

        elif "my age" in data:
            age="21 years old"
            speak(age)


        elif 'wikipedia' in data:
            speak('searching wikipedia...')
            data=data.replace("wikipedia","")
            results=wikipedia.summary(data,sentences=2)
            speak("according to wikipedia")
            print(results)
            speak(results)


        elif "old are you" in data:
            age="i am 20 years old"
            speak(age)

        elif 'time' in data:
            time=datetime.datetime.now().strftime("%I%M%p")
            speak(time)

        elif 'open youtube' in data:
            webbrowser.open("https://www.youtube.com/")

        elif 'open google' in data:
            webbrowser.open("https://www.google.com/")

        elif 'open instagram' in data:
            webbrowser.open("https://www.instagram.com/")

        elif 'open facebook' in data:
            webbrowser.open("https://www.facebook.com/") 

        elif 'open wynk music' in data:
            webbrowser.open("https://wynk.in/music") 

        elif 'open amazon' in data:
            webbrowser.open("https://amazon.in/")

        elif 'open flipkart' in data:
            webbrowser.open("https://flipkart.in/")

        elif 'open stackoverflow' in data:
            webbrowser.open("https://stackoverflow.com/")

        elif 'play music' in data:
             music_dir="C:\\Users\\DELL\\Desktop\\songs"
             songs=os.listdir(music_dir)
             print(songs)
             os.startfile(os.path.join(music_dir,songs[1]))

        elif 'open vscode' in data:
            codepath="C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\Code.exe"
            os.startfile(codepath)


        elif 'email send to' in data:
            try:
                speak("what would i say?")
                content=sptxt()
                speak("who do you want to send the mail?")
                to="prabhatkainthola91@gmail.com  "
                sendEmail(to,content)
                speak("email has been sent!")
            
            except Exception as e:
                print(e)
                speak("sorry Mr. prabhat.i am not able to send this mail")
        

        elif " tell a joke " in data:
            joke_1=pyjokes.get_joke(language="en",category="neutral")
            speak(joke_1)
            print(joke_1)


        elif 'today weather' in data:
            speak("Please tell me the city name.")
            city_name = MicExcecution().lower()
            get_weather('69363b12ffe67daaeae48f9a87921680', city_name)

        elif 'top news' in data:
            api_key = '525125de1d464288b2514e7da3b4cca8' 
            top_news_headlines = get_top_news(api_key, num_headlines=5)

            if top_news_headlines:
                speak("Here are the top news headlines:")
                for idx, headline in enumerate(top_news_headlines, start=1):
                    print(f"{idx}. {headline}")
                    speak(f"{idx}. {headline}")
            else:
                speak("Sorry, couldn't fetch top news")


        elif 'send message on whatsapp' in data:
            speak("Sure, please tell me the country code.")
            country_code = MicExcecution().lower()

            speak("Sure, please tell me the contact name or number.")
            contact_name = MicExcecution().lower()

            speak("What message would you like to send?")
            message_content = MicExcecution().lower()

            send_whatsapp_message(contact_name, message_content,country_code)
            speak("WhatsApp message sent successfully.")

        elif 'play a song' in data:
            speak("Sure, please tell me the name of the song.")
            song_name = sptxt().lower()
            play_song(song_name)


        elif "recommend a movie" in data:
            speak("Sure, please tell me the genre you're interested in.")
            genre = sptxt()
            recommend_movie(genre)

        elif "take a picture" in data:
            take_picture()
            speak("Picture taken successfully.")

        elif "exit" in data:
            speak("thank you")
            break

    
