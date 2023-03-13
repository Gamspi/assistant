import json
import queue
import sounddevice as sd
import words
import helpers
from actions import actions
from skills import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from vosk import KaldiRecognizer, Model

q = queue.Queue()
device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
model = Model('voice_model')


def callback(indata, frames, time, status):
    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    print('data', data)
    alias = words.alias.intersection(data.split())
    if not alias:
        return
    data = data.replace(list(alias)[0], '')
    print(data)
    if data:
        text_vector = vectorizer.transform([data]).toarray()[0]
        action_id = clf.predict([text_vector])[0]
        action = actions[action_id]
        if action:
            answer = action['answers'][helpers.random_index(action['answers'])]
            print(action)
            func_name = action['func_name']
            if answer:
                speaker(answer)
            if func_name:
                exec(func_name)


def main():
    print('this is test')
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))
    print(list(words.data_set.values()))
    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set
    with sd.RawInputStream(samplerate=samplerate, blocksize=18000, device=device,
                           dtype="int16", channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                if data:
                    recognize(data, vectorizer, clf)
            # else:
            #     print(rec.PartialResult())


if __name__ == '__main__':
    main()
