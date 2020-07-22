# Minesweeper - Code Challenge

[Code challenge](https://github.com/deviget/minesweeper-API/tree/23ff6b614ee33d5a9104a3ade5f287eee583640b) 
for [Deviget](https://www.deviget.com/).

The project has an API developed in Django, and a UI developed in VueJS.

It uses environment variables for configuration. A full list of available values can
be found in the `.env.example` file.

## Requirements
- Python 3.8
- Poetry
- Node 14.5
- Yarn

## Django

To run the development server:
```shell
poetry install
poetry shell
# MANUALLY create your own .env file
dotenv python manage.py runsslserver
```

## VueJS

To run the development server:
```shell
cd mineswepper_ui
yarn install
# MANUALLY create your own .env file
yarn serve
```

# Game play!!!

You need to register your email! Do not worry, I will not spam you. In fact, I
will never send you any email. You can use a fake one, I do not care.

I am not requesting passwords because passwords are tedious, and who cares if
someone else sees your games, they might even finish them for you 🥳.

Once you have registered, you can create a new game (use the beautiful select
box I provide) or you can also continue playing your previous games.

But be careful! Timer will not stop! Once you create a game the timer starts
running... 😲

I have provided some easy to remember non configurable game names which you
can use to go back to your previous games. **You are welcome.**

You can create boards of up to 100 x 100, but do know that your browser will
complain! I only allow that number so you can see how my recursive uncovering
implementation does not die due to stack overflow!

## Rules!
 - Click on a flag to, well, flag the cell.
 - Click on the check-mark to uncover a cell.
 - Keep going until you win, or explode.
