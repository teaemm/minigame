from aiogram.fsm.state import State, StatesGroup

class GuessNumberState(StatesGroup):
    guessing = State()

class GuessKnb(StatesGroup):
    knbguessing = State()

class TicTacToeState(StatesGroup):
    playing = State()
