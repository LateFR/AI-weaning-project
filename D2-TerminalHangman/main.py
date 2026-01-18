import random
import os
import argparse
import re

default_wordlist = ["python", "test", "humain", "drôle", "anticonstitutionnellement"]

def choice_the_secret(wordlist_path="wordlist.txt", is_worlist_optional=True, default_wordlist=default_wordlist):
    wordlist = []
    print("[SELECTING THE WORD...]")
    if os.path.exists(wordlist_path) and os.path.isfile(wordlist_path):
        try:
            with open(wordlist_path) as r:
                for word in r.readlines():
                    if word:
                        wordlist.append(word.strip())  # FIX: ajout du .strip() pour le bug \n
        except Exception as e:
            print(f"Error <{e}> with the wordlist")
            if is_worlist_optional:
                wordlist = default_wordlist
                print("[Warn] We are using the default wordlist")
            else:
                raise e
    else:
        if is_worlist_optional:
                wordlist = default_wordlist
                print("[Warn] We are using the default wordlist")
        else:
            raise Exception("Wordlist isn't exploitable")
    
    print(f"[WORDLIST SIZE: {len(wordlist)}]")
    print(f"[WORD SELECTED]")
    return random.choice(wordlist)

def is_allowed_try(guess):
    return re.match("^[A-Za-z]+$", guess)
    # OU version plus simple : return guess.isalpha()

def show_state(secret, found_in_secret, errors, remaining_error):
    print("\n----------")
    print(f"Currently known: {currently_known(secret, found_in_secret)}")
    print(f"You have unsuccessfully tried: {errors} | You have left {remaining_error} errors")
    print("----------\n")
    
def currently_known(secret, found_in_secret):
    word = ""
    for letter in secret:
        if letter in found_in_secret:
            word += letter
        else:
            word += "_"
    return word

if __name__=="__main__":
    parser = argparse.ArgumentParser("Hangman game in cli")
    parser.add_argument("--wordlist", "-w", default="wordlist.txt", help="Path to a wordlist. Optional. If we don't found the wordlist, we will use a small hardcoded wordlist")
    parser.add_argument("--allowed-error", default=9, help="Number of allowed errors. Default is 9, like the real hangman.")
    args = parser.parse_args()
    
    secret = choice_the_secret(args.wordlist).lower()
    
    print("\nWelcome in the hanged game!")
    remaining_error = args.allowed_error
    errors = []
    found_in_secret = []
    iteration = 0
    
    while remaining_error > 0:
        guess = input("Enter a letter or a word. No accent, number or other accepted: ").lower()
        if not is_allowed_try(guess):
            print("Invalid input")
            continue
        iteration+=1
        
        if guess == secret or currently_known(secret, found_in_secret) == secret:
            print(f"You won in {iteration} try! The word was: {secret}")
            exit()
        elif len(guess) > 1:
            print("This isn't the good word. You can maybe try a letter?")
            remaining_error -= 1
        
        print("\n")
        if guess in secret:
            print(f'Yes! The letter "{guess}" is in the secret word!')
            found_in_secret.append(guess)
        else:
            errors.append(guess)
            remaining_error -= 1
            print("You're letter isn't in the secret word")
            
        show_state(secret, found_in_secret, errors, remaining_error)
        
    print(f"You unfortunately lost... you tried {iteration} times.")
    print(f"The secret word was {secret}")