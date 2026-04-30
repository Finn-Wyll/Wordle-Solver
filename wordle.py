import json
import time
import os
from collections import Counter
GUESSES=6
TOTAL_WORDS=12972
with open('data/freq_map.json') as f:
    freq_map= json.load(f)

_current_words = None

def reset_solver():
    global _current_words
    _current_words = freq_map.copy()
    return

def green_letter(dictionary,letter,pos):
    for word in list(dictionary):
        if word[pos] != letter:
            del dictionary[word]
    return len(dictionary)


def yellow_letter(words_dict, letter, pos):
    for word in list(words_dict):
        if letter not in word or word[pos] == letter:
            del words_dict[word]
    return len(words_dict)

def handle_black(words_dict, letter, confirmed_count):
    for word in list(words_dict):
        if confirmed_count == 0:
            if letter in word:
                del words_dict[word]
        else:
            if word.count(letter) < confirmed_count:
                del words_dict[word]

    return (len(words_dict))

def enter_guess(words_dict, guess):
    colours = []
    for letter in guess:
        colour = input(f"What colour is {letter.upper()} (y/g/b): ").lower()
        while colour not in ["y", "g", "b"]:
            colour = input("Your answer must be y, g, or b: ").lower()
        colours.append(colour)

    confirmed = Counter()
    for i, letter in enumerate(guess):
        if colours[i] in ("g", "y"):
            confirmed[letter] += 1

    # Apply rules
    for i, letter in enumerate(guess):
        if colours[i] == "g":
            green_letter(words_dict, letter, i)
        elif colours[i] == "y":
            yellow_letter(words_dict, letter,i)
        elif colours[i] == "b":
            handle_black(words_dict, letter, confirmed[letter])

    print("Suggested guesses:")
    print()
    best_word, best_score = min(
    ((w, calc_feedback(words_dict, w)) for w in words_dict),
    key=lambda x: x[1])

    print(f"Best word: {best_word}")
    print(f"Expected remaining words: {best_score:.2f}")



    print("Most common word: "+max(words_dict,key=words_dict.get))
    print("Total number of possible words left: "+str(len(words_dict)))

    return                 

CACHE_FILE = 'cache.json'

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_cache(cache_data):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_data, f)


_feedback_cache = load_cache()

def calc_feedback(words_dict, guess):
    
    key_list = sorted(words_dict.keys())
    cache_key = f"{','.join(key_list)}|{guess}"
    
    if cache_key in _feedback_cache:
        return _feedback_cache[cache_key]
    
    total_remaining = 0

    for possible in words_dict:
        temp_dict = words_dict.copy()
        confirmed = Counter()

      
        for i in range(5):
            if guess[i] == possible[i]:
                confirmed[guess[i]] += 1
            elif guess[i] in possible:
                confirmed[guess[i]] += 1

        for i in range(5):
            letter = guess[i]
            if guess[i] == possible[i]:
                green_letter(temp_dict, letter, i)
            elif letter in possible:
                yellow_letter(temp_dict, letter, i)
            else:
                handle_black(temp_dict, letter, confirmed[letter])

        total_remaining += len(temp_dict)
    
    result = total_remaining / len(words_dict)
    
    _feedback_cache[cache_key] = result
    save_cache(_feedback_cache)
    
    return result


def auto_guess(guess, colours):
    global _current_words

    
    if _current_words is None:
        _current_words = freq_map.copy()

    if not _current_words:
        raise RuntimeError("No possible words left — solver over-pruned")

    confirmed = Counter()
    for i, letter in enumerate(guess):
        if colours[i] in ("g", "y"):
            confirmed[letter] += 1

    
    for i, letter in enumerate(guess):
        if colours[i] == "g":
            green_letter(_current_words, letter, i)
        elif colours[i] == "y":
            yellow_letter(_current_words, letter, i)
        elif colours[i] == "b":
            handle_black(_current_words, letter, confirmed[letter])

    
    best_word, best_score = min(
        ((w, calc_feedback(_current_words, w)) for w in _current_words),
        key=lambda x: x[1]
    )

    return best_word
              



def calc_entropy(words_dict):
    data=dict()
    for word in list(words_dict):
        data.update({word: calc_feedback(words_dict,word)})

    return data

def start():
    d=freq_map.copy()
    print("Suggested starter: stoae")
    for i in range(GUESSES):
        guess=input("Enter wordle guess: ")
        enter_guess(d,guess)
    return                
  
def testSpeed():
    


    start_time = time.perf_counter()
    
    print(auto_guess("stoae","bbbbb"))
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"The code block executed in {elapsed_time:.4f} seconds")









