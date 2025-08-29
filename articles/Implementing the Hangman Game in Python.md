# Implementing the Hangman Game in Python

Hangman was a really fun game in our home. We would grab a pen and paper and take turns choosing words for the other to guess. Today, it is used in classroom settings to help kids practice their spellings, understand strategic decision making by choosing vowels first, and brainstorm possible words from hints.

In this article, we will go through the Hangman Game by implementing it in Python. This is a beginner-friendly project where we will learn the basics of the Python language, such as defining variables, commonly used functions, loops, and conditional statements.

Understanding the Project

First, we will understand the game and get into the depths of how our code should work.

In a typical 2-player Hangman Game, Player 1 chooses a word, hiding it from Player 2, and generates blanks corresponding to the number of letters in the word he chose for guessing. Player 2 has to guess the word by guessing one letter at a time. Player 2 has a defined number of lives at the beginning, and with each wrong guess of letters, they lose a life (to the point where the man is hanged). With each right guess, the lives remain the same as before. If Player 2 loses all their lives without guessing the word, the game is over, and they lose. If they manage to guess the word, they win the game. This is the outline of the game in its traditional sense.

In this project, the computer will be Player 1, generating the word to guess, while we, the user, will be Player 2. Let us implement the above using a flowchart for better comprehension.

Image by AltumCode on Unsplash

Drawing a flowchart and defining each step helps in turning our thought process into code, so it’s always a good practice to draw one. Now let us start with coding the problem!

Step 1: List of Words and the Random Module

The first step in this project is for the computer to choose a random word that the user will have to guess. For this purpose, we will need both a list of words from which the computer picks one word to be guessed, and a Python function called `random`, which will randomly pick out that word from the given list.

To generate the list, I googled the 100 most common nouns used in the English language and found a list. I used these words and created a Python list with it to be used in this project.

As the name suggests, a Python List is a datatype that stores in itself a collection of items. A list of colors will be defined in Python as `colors = ["red", "yellow", "green", "blue", "pink"]`. You can check out the List syntax and additional information from the Python official page on List.

`word_list = [ "time", "year", "people", "way", "day", "man", "thing", ...]`

You can access the project files from my GitHub repository. `hangman_words.py` is the Python file that contains the list of words from which the computer will randomly pick out a word for the game.

Now, once our list is created, we need the computer to choose a random word from the given list of words `word_list`. Python has a module especially for this purpose called “random”. We will import the module and use it to allow the computer to randomly choose a word `word_to_guess` from the list `words_list`. You can print the word_to_guess while coding the project to enhance understanding, and comment it out when playing with the computer!

`import random`
`word_to_guess = random.choice(word_list)`
`print(word_to_guess)`

For more information on the `random.choice()` function, click here.

Step 2: Generating Blanks

The next step is to generate blanks equal to the number of letters in the word_to_guess so that the user gets an idea of the number of letters in the word he has to guess. For this, we will define a variable called `blanks` which will act as a container for the unguessed letters of the word. It will contain the number of “\_” equal to the number of letters in the word_to_guess .

To calculate the number of letters in the word_to_guess that has been randomly picked by the computer from the `words_list`, we will use the Python function `len()` that calculates the length of a string. More information on this in-built function can be accessed through this link.

`blanks = ""`
`word_length = len(word_to_guess)`

As we now know the number of letters in `word_to_guess`, we will use this number to add an equal number of “\_” in the variable `blanks`. For this purpose, we will use the `for` loop, a Python functionality that allows us to iterate over items in a sequence, in our case, the string that is stored in the variable `word_to_guess`. Click here to learn more about `for` loop and its syntax.

`for i in range(word_length):`
`    blanks += "_"`

Step 3: Creating the While Loop that runs until the Game is Over

Let us refer back to the flowchart we created to help us understand the project. In order to code this project, we need to keep in mind the following points:

The user has a defined number of lives at the beginning

For each letter guessed wrong, the lives are reduced by 1 If the user runs out of lives, the user loses and the game is over If the user has lives left, the computer will ask the user to guess another letter

For each letter guessed right, the lives remain unchanged, and a blank is replaced by a letter in the placeholder blanks If the variable `your_word` is all filled, the user wins the game, and the game is over If the variable `<code>your_word` has blank spaces left, then the computer will again ask the user to guess the next letter

Since we have created the `for` loop previously that caters to the guessed letter, now is the time to incorporate the idea of lives, and reduce it when the user has guessed a letter wrong.

Let us define the number of lives for the user with the variable `number_of_lives`. The user has 6 chances to suggest the wrong letter in guessing the word.

`number_of_lives = 6`

Now, considering the points mentioned above, we also need a variable or a condition that tells us to stop asking the user to guess when the game is over. Let us code it with the help of a Boolean variable.

Simply stating, a Boolean is a datatype in Python that stores either `True` or `False`. We will use this Boolean variable to continue the game while it is `False` and vice versa. Initially, while the game starts, this variable will be `False`, meaning the game is not over.

`game_over = False`

Now we will introduce a `while` loop with the condition that it will run as long as the game is not over, and we will include the conditions mentioned above in this `while` loop. Check out more about the `while` loop from the Python official documentation here.

`while not game_over:`
    `print("You have ", number_of_lives, " lives remaining!")`
    `guess = input("Guess a letter: ").lower()`
    `your_word = ""`
    `for letter in word_to_guess:`
        `if letter == guess:`
            `your_word += letter`
            `break`
        `elif letter in word_to_guess:`
            `your_word += letter`
            `break`
        `else:`
            `your_word += "_"`
    `print("Word to guess: ", your_word)`

Step 4: Handling Situations

The last step is to handle different circumstances. What happens if the letter the user has guessed has already been suggested by the user, or the letter is not in the word? Also, what if all the letters have been guessed and there are no more blanks in `your_word`? This would mean that the user has guessed the word and thus won.

We will add this situation in the code with the following lines:

`if guess in your_word:`
    `print(f"You've already guessed {guess}")`
if "_" not in your_word:
    `game_over = True`
    `print("You have guessed the word! YOU WIN!")`

Step 5: Creating the While Loop that runs until the Game is Over

Let us refer back to the flowchart we created to help us understand the project. In order to code this project, we need to keep in mind the following points:

The user has a defined number of lives at the beginning

For each letter guessed wrong, the lives are reduced by 1 If the user runs out of lives, the user loses and the game is over If the user has lives left, the computer will ask the user to guess another letter

For each letter guessed right, the lives remain unchanged, and a blank is replaced by a letter in the placeholder blanks If the variable `your_word` is all filled, the user wins the game, and the game is over If the variable `<code>your_word` has blank spaces left, then the computer will again ask the user to guess the next letter

Since we have created the `for` loop previously that caters to the guessed letter, now is the time to incorporate the idea of lives, and reduce it when the user has guessed a letter wrong.

Let us define the number of lives for the user with the variable `number_of_lives`. The user has 6 chances to suggest the wrong letter in guessing the word.

`number_of_lives = 6`

Now, considering the points mentioned above, we also need a variable or a condition that tells us to stop asking the user to guess when the game is over. Let us code it with the help of a Boolean variable.

Simply stating, a Boolean is a datatype in Python that stores either `True` or `False`. We will use this Boolean variable to continue the game while it is `False` and vice versa. Initially, while the game starts, this variable will be `False`, meaning the game is not over.

`game_over = False`

Now we will introduce a `while` loop with the condition that it will run as long as the game is not over, and we will include the conditions mentioned above in this `while` loop. Check out more about the `while` loop from the Python official documentation here.

`while not game_over:`
    `print("You have ", number_of_lives, " lives remaining!")`
    `guess = input("Guess a letter: ").lower()`
    `your_word = ""`
    `for letter in word_to_guess:`
        `if letter == guess:`
            `your_word += letter`
            `break`
        `elif letter in word_to_guess:`
            `your_word += letter`
            `break`
        `else:`
            `your_word += "_"`
    `print("Word to guess: ", your_word)`

Step 6: Handling Situations

The last step is to handle different circumstances. What happens if the letter the user has guessed has already been suggested by the user, or the letter is not in the word? Also, what if all the letters have been guessed and there are no more blanks in `your_word`? This would mean that the user has guessed the word and thus won.

We will add this situation in the code with the following lines:

`if guess in your_word:`
    `print(f"You've already guessed {guess}")`
if "_" not in your_word:
    `game_over = True`
    `print("You have guessed the word! YOU WIN!")`

In conclusion, this project provides a basic implementation of the Hangman game in Python, demonstrating fundamental programming concepts such as loops, conditional statements, and user input.