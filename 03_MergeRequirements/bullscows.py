import argparse
from os.path import isfile
from urllib.request import urlopen
from collections import Counter
from random import choice


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = sum(map(str.__eq__, guess, secret))
    cows = (Counter(guess) & Counter(secret)).total()
    return bulls, cows

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = choice(words)
    attempt = 0
    guess = ""
    while guess != secret:
          attempt += 1
          guess = ask("Введите слово: ", words)
          b, c = bullscows(guess, secret)
          inform("Быки: {}, Коровы: {}", b, c)
          

    return attempt

def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        word = input(prompt) 
        if valid and word in valid:
              break
        
    return word
    

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

parser = argparse.ArgumentParser()

parser.add_argument("dictionary", type=str, default=None)
parser.add_argument("wordlength", type=int, nargs='?', default=5)

args = parser.parse_args()

wordLength = args.wordlength if args.wordlength else 5

try:
    if isfile(args.dictionary):
	    with open(args.dictionary, 'rb') as f:
		    allWords = f.read().decode().split()
    else:
	    with urlopen(args.dictionary) as f:
		    allWords = f.read().decode().split()
except:
      print("Словарь не найден!")
      exit()

dictionary = [word for word in allWords if len(word) == wordLength]

attempt = gameplay(ask, inform, dictionary)
print(attempt)