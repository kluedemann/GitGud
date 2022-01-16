# GitGud

## Project Idea: 3D Tic-Tac-Toe-Tub

## Members:
 - Jake
 - Kai
 - Steven
 - Jenny
 - Gabe

## Running the game
 1. `python3 -venv env`
 2. `source env/bin/activate`
 3. `pip install -r requirements.txt`
 4. `python main.py`

## Compiling the game
  1. `pip install pyinstaller`
  2. `pyinstaller --onefile main.py`
  3. `.\dist\main`

## Game Design & Inspiration
In the standard game of Tic-Tac-Toe if both players make well-thought out moves it will always end in a tie. Inspired by 5D chess, our team decided to create a higher level version of the game, adding in a third dimension, to make it much more challenging, while adding in many new ways to enhance playability and fun.

## Gameplay & Instructions
With the same basic mechanics of Tic-Tac-Toe, our game expands it to a 4x4x4 board in a 3-Dimensional space, allowing for players to win in a multitude of ways. To win you can utilize all dimensions of this game, stringing together 4 spheres consecutively in rows, columns, or diagonals of each plane. You may also use the other dimensions of the game and make 4 in a row vertically or diagonally making use of multiple planes. To make a move, click on one of the spheres and it will change color to identify the one you have chosen. At the end, the basics is you want to ensure that the other player doesn’t get 4 in a row before you do.

## Additional Information
Instead of using ‘X’ and ‘O’ we used the colors red and blue, and we created visual lines that appear when hovering over each sphere to show how each plane connects to one another.

## How we built it
We created the game in Python through PyGame. We started by creating a basic 4x4 Tic-Tac-Toe board. Then

## Challenges we ran into
- Creating and designing a functional AI to play against
- Creating the game in a easy to visualize way

## Use & Utility
This game requires a lot more thinking and challenges than the regular game of Tic-Tac-Toe. It is a difficult, but intuitive game, and it helps the player improve on spatial awareness and puzzle solving skills, while also being a fun and exciting game.

## Accomplishments that we're proud of
- Creating a functional game of 3D Tic-Tac-Toe with both a multiplayer and AI mode
- Getting a working AI, that makes logical moves, and is difficult to beat


## What's next for GitGud
We'll see :)