#!/usr/bin/env python3
"""Open API Trivia Game"""

# documentation for this API can be found at 
# https://opentdb.com/api_config.php

import requests
import random
from html import unescape

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

MAX_QUESTIONS = 50 # API defined


# ask questions to build get request
def createGame():
    print("\nWelcome to Trivia!")

    # initial url to possibly be appended depending on choices
    trivia_url = BASE_URL + QUERY   
    
    no_of_questions = 0
    # Choose how many questions
    while no_of_questions < 1 or no_of_questions > MAX_QUESTIONS:
        try:
            # get number of questions to play
            print(f"\nHow many questions would you like to be asked?\nPick a number between 0 and {MAX_QUESTIONS}.")
            no_of_questions = int(input(">"))
            # append the url
            trivia_url += AMOUNT + str(no_of_questions)
        # if anything other than int 1 - 50, go back in loop
        except:
            no_of_questions = 0
    
    # print(f"You chose {no_of_questions} questions")

    play_category = ""
    # Choose any category or specific category
    while play_category != "n":        
        if play_category == "y":
            # get categories
            trivia_categories_dict = requests.get(BASE_URL + CATEGORY_LOOKUP).json()
            trivia_categories = trivia_categories_dict["trivia_categories"]

            print()

            # for each, print the id and category name
            ids = []
            for cat in trivia_categories:                
                print("[", cat["id"], "] ", unescape(cat["name"]))
                ids.append(int(cat["id"]))

            category = 0
            # get category number
            # prefer not in 
            while category not in ids:
                try:
                    # get category number
                    print("\nPlease pick a number from the categories above.")
                    category = int(input(">"))
                    # append the url
                    trivia_url += "&" + CATEGORY + str(category)
                # handles not int and goes back in loop
                except:
                    category = 0
            # break out of loop if "y"
            break
        print("\nWould you like to choose a category? y/n")
        # get choose category y or n
        play_category = input(">").lower()

    # if play_category == "y":
    #     print("You chose the category, ")
    # else:
    #     print("You chose ANY category")

    
    play_diff = ""    
    # Choose any difficulty or specific difficulty
    while play_diff != "n":
        if play_diff == "y":
            print()

            diff_list = ["easy", "medium", "hard"]
            for diff in diff_list:
                print(diff)

            difficulty = ""
            while difficulty not in diff_list:
                # get difficulty level                
                print("\nChoose difficulty level.")
                difficulty = input(">").lower()
                # append the url
                trivia_url += "&" + DIFFICULTY + difficulty
            # break out of loop if "y"    
            break
        # get choose difficulty y or no
        print("\nWould you like to choose a difficulty? y/n")
        play_diff = input(">").lower()

    # return the final url
    return trivia_url

def playGame(url):
    # get then define dictionary
    trivia_dict = requests.get(url).json()
    questions = trivia_dict["results"]
    # set score
    score = 0

    # for each question object
    for qobj in questions:
        # define values
        question = unescape(qobj["question"])        
        correct_answer = unescape(qobj["correct_answer"])        
        incorrect_answers = qobj["incorrect_answers"]
        # create list and append correct and incorrect
        answers = []
        answers.append(correct_answer)        
        for inc_ans in incorrect_answers:            
            answers.append(unescape(inc_ans))        
        random.shuffle(answers)

        print()

        # ask question
        print(question)
        # print choices
        for i, answer in enumerate(answers):
           print(f"[{i}] {answer}")

        # get choice
        choice = -1
        while choice < 0 or choice >= len(answers):
            try:
                choice = int(input("\nYour answer >"))
            # handle incorrect inputs and reloop
            except:
                choice = -1
        
        # add to score if correct, otherwise display correct answer
        if answers[int(choice)] == correct_answer:
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect! The correct answer was {correct_answer}")
            
    # final score
    print(f"\nYour final score was {score} our of {len(questions)}")  
    if score/len(questions) > 0.5:
        print("Great job!")
    else:
        print("Better luck next time!")
def main():
    playGame(createGame())

if __name__ == "__main__":
        main()