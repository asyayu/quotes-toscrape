import pandas
import random
import requests
from bs4 import BeautifulSoup


def quote_guesser():
    quotes_data = pandas.read_csv("quotes.csv")
    num_quotes = len(quotes_data.index)

    # Get random quote
    rand_index = random.randint(1, num_quotes - 1)
    rand_quote = quotes_data.iloc[rand_index]
    print(rand_quote.Author)
    # Create hints
    response = requests.get(rand_quote.Bio)
    bio_data = response.text
    soup = BeautifulSoup(bio_data, "html.parser")
    birth_date = soup.find(class_="author-born-date").get_text()
    birth_place = soup.find(class_="author-born-location").get_text()
    author_description = soup.find(class_="author-description").get_text().strip()
    hints = []
    hint_1 = f"This person was born on {birth_date} {birth_place}."
    hints.append(hint_1)
    initials = [name[0] for name in rand_quote.Author.split()]
    hint_2 = f"This person's initials are {initials[0]} and {initials[1]}."
    hints.append(hint_2)
    hint_3 = author_description
    for name_part in rand_quote.Author.split():
        hint_3 = hint_3.replace(name_part, "X")
    hints.append(hint_3)
    # Gameplay
    guesses = 0
    print(rand_quote.Text)
    player_guess = input("Who said this? ")
    while (player_guess.lower() != rand_quote.Author.lower()) and (guesses < 3):
        guesses += 1
        print("Here's a hint:")
        print(hints[guesses - 1])
        print(f"Guesses remaining: {4 - guesses}")
        player_guess = input("Who was it? ")
    if player_guess.lower() == rand_quote.Author.lower():
        print("Correct!")
    else:
        print(f"You're out of guesses... The answer was {rand_quote.Author}.")
    go_again = ''
    while go_again not in ["yes", "y", "no", "n"]:
        go_again = input("Do you want to play again? (y/n): ")
    if go_again.lower() in ["y", "yes"]:
        quote_guesser()
    else:
        print("Ok, bye!")

quote_guesser()
