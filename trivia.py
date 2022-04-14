#!/usr/bin/env python3
"""Open API Trivia Game"""

# documentation for this API can be found at 
# https://opentdb.com/api_config.php

from secrets import choice
import requests
import random


# URL builder
BASE_URL = "https://opentdb.com/"

# must add QUERY and AMOUNT + n < 50 to base
QUERY = "api.php?"
AMOUNT = "amount="
# optional query params
CATEGORY = "category="
DIFFICULTY = "difficulty="
# not using type, but is an option
# TYPE = "type="

# add to base to lookup categories
CATEGORY_LOOKUP = "api_category.php"

def createGame():
    print("Welcome to Trivia!")
    TRIVIA_URL = BASE_URL + QUERY
    no_of_questions = 0
    play_category = ""
    category = 0
    diff_list = ["easy", "medium", "hard"]
    play_diff = ""
    difficulty = ""
    
    # Choose how many questions
    while no_of_questions < 1 or no_of_questions >= 50:
        try:
            print("\nHow many questions would you like to be asked?\nPick a number less than 50.")
            no_of_questions = int(input(">"))
            TRIVIA_URL += AMOUNT + str(no_of_questions)
        # if anything other than int 1 - 50, go back in loop
        except:
            no_of_questions = 0
    
    # print(f"You chose {no_of_questions} questions")

    # Choose any category or specific category
    while play_category != "n":        
        if play_category == "y":
            trivia_categories_dict = requests.get(BASE_URL + CATEGORY_LOOKUP).json()
            trivia_categories = trivia_categories_dict["trivia_categories"]
            print()
            for cat in trivia_categories:
                print("[", cat["id"], "] ", cat["name"])
            while category < 9 or category > 32:
                try:
                    print("\nPlease pick a number from 9 - 32.")
                    category = int(input(">"))
                    TRIVIA_URL += "&" + CATEGORY + str(category)
                except:
                    category = 0
            break
        print("\nWould you like to choose a category? y/n")
        play_category = input(">").lower()

    # if play_category == "y":
    #     print("You chose the category, ")
    # else:
    #     print("You chose ANY category")
    # Choose any difficulty or specific difficulty
    while play_diff != "n":
        if play_diff == "y":
            print()
            for diff in diff_list:
                print(diff)            
            while difficulty not in diff_list:                
                print("\nChoose difficulty level.")
                difficulty = input(">").lower()
                TRIVIA_URL += "&" + DIFFICULTY + difficulty
            break
        print("\nWould you like to choose a difficulty? y/n")
        play_diff = input(">").lower()

    return TRIVIA_URL

def playGame(url):
    trivia_dict = requests.get(url).json()
    questions = trivia_dict["results"]
    score = 0

    for qobj in questions:
        question = qobj["question"]
        correct_answer = qobj["correct_answer"]
        incorrect_answers = qobj["incorrect_answers"]
        answers = incorrect_answers
        answers.append(correct_answer)
        random.shuffle(answers)

        print()
        print(question)
        for i, answer in enumerate(answers):
           print(f"[{i}] {answer}")

        choice = ""
        while choice == "":
            choice = input("\nYour answer >")
        
        
        
        if answers[int(choice)] == correct_answer:
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect! The correct answer was {correct_answer}")
            

    print(f"\nYour final score was {score} our of {len(questions)}")  


def main():
    playGame(createGame())

if __name__ == "__main__":
        main()