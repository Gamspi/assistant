import pyttsx3
import subprocess
import sys
import os
from paths import paths
import webbrowser

# инициализация спикера
engine = pyttsx3.init()
engine.setProperty('rate', 180)


def speaker(text):
    engine.say(text)
    engine.runAndWait()


def browser():
    print('browser')
    webbrowser.open('https://www.google.com')


def browser_search(data):
    index_say = data.find('за гугле') + len('за гугле')
    word_search = '+'.join(data[index_say:].split())
    webbrowser.open(f'https://www.google.com/search?q={word_search}')


def open(data):
    index_say = data.find('открой') + len('открой')
    word_open = '_'.join(data[index_say:].split())
    try:
        path = paths[word_open]
        subprocess.Popen(path)
    except KeyError:
        speaker('я не нашла такую программу')

def say(data):
    index_say = data.find('скажи') + len('скажи')
    word_say = data[index_say:]
    speaker(word_say)



def offpc():
    os.system('shutdown /s')
    print('os off')
    sys.exit()


def offBot():
    sys.exit()

def letWork():
    subprocess.Popen(paths['вэб_шторм'])