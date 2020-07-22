# Minesweeper - Code Challenge

[Code challenge](https://github.com/deviget/minesweeper-API/tree/23ff6b614ee33d5a9104a3ade5f287eee583640b) 
for [Deviget](https://www.deviget.com/).

The project has an API developed in Django, and a UI developed in VueJS. It has
been deployed to Heroku https://ms-deviget.herokuapp.com/.

It uses environment variables for configuration. A full list of available values can
be found in the `.env.example` files.

## Game play!!!

You need to register your email! Do not worry, I will not spam you. In fact, I
will never send you any emails. You can use a fake one, I do not care.

I am not requesting passwords because passwords are tedious, and who cares if
someone else sees your games, they might even finish them for you 🥳.

Once you have registered, you can create a new game (use the beautiful select
box I provide) or you can also continue playing your previous games. Although
you will only be able to retrieve your last 15 games! Any other will be lost
forever! 🙀 (They are still in the database, I just hide them)

And be careful! Timer will not stop! Once you create a game the timer starts
running... 😲

I have provided some easy to remember non configurable game names which you
can use to go back to your previous games. They look something like this:
22eead94-98ce-4de4-97f4-e8e8d5897750. **You are welcome.**

You can create games of up to 100 x 100, but do know that your browser will
complain! I only allow that number so you can see how my (non-)recursive
uncovering implementation does not die due to stack overflow!

### Rules!
 - Click on a flag to, well, flag the cell.
 - Click on a flagged cell to unflag it.
 - Click on the check-mark to uncover a cell.
 - Keep going until you win, or explode.

## Development

### Requirements
- Python 3.8
- Poetry
- Node 14.5
- Yarn

### Django

To run the development server:
```shell
poetry install
poetry shell
# MANUALLY create your own .env file
dotenv python manage.py runsslserver
```

### VueJS

To run the development server:
```shell
cd mineswepper_ui
yarn install
# MANUALLY create your own .env file
yarn serve
```

### Tests

There are some tests for Django, and none for Vue.

#### Why?

Since the data is handled in the backend, tests were implemented there
to ensure that the logic of the game and the data was correctly handled.

Test coverage is incomplete, but my main goal was to show how I write tests.

### API documentation

You can read the API documentation in at two different paths:

- https://ms-deviget.herokuapp.com/swagger/
- https://ms-deviget.herokuapp.com/redoc/

Choose the one that makes you happier!


### Important considerations

#### Game time
Game time is handled using real time count. A timeout is used to trigger a
visual change, but real datetime instances are used to calculate the difference
from the start of the game until it finishes.

#### Multi tab usage
After every move the whole board is refreshed from the server so that if you
are playing the same game in two different tabs, then we always get the most
recent version of the board after each play. Not very efficient, but at least
we do not get outdated games.

#### No GET endpoint for a single game
If you create big games (40 x 40) your payload for 15 games would be around
100kb.

If you create small games (10 x 10) your payload for 15 games would be around
100km.

I think those sizes are acceptable for a Demo app, so I went for a single GET
endpoint were I could bring all the games at once, instead of making a single
request for each one.
