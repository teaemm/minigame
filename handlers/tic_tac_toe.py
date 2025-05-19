from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import choice
from states import TicTacToeState

router = Router()

# Игровое поле
EMPTY_BOARD = [["⬜"] * 3 for _ in range(3)]

# Хранилище для игры
games = {}

def render_board_inline(board, user_id):
    """Создает Inline-клавиатуру для игрового поля."""
    keyboard = []
    for i, row in enumerate(board):
        buttons = [
            InlineKeyboardButton(
                text=cell,
                callback_data=f"move:{user_id}:{i}:{j}" if cell == "⬜" else "disabled"
            )
            for j, cell in enumerate(row)
        ]
        keyboard.append(buttons)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.message(F.text == "❌ Крестики-нолики")
async def start_tic_tac_toe(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    games[user_id] = {"board": [row[:] for row in EMPTY_BOARD], "turn": "❌"}
    await state.set_state(TicTacToeState.playing)
    await message.answer(
        "Игра началась! Вы играете за ❌. Ваш ход:",
        reply_markup=render_board_inline(games[user_id]["board"], user_id)
    )

@router.callback_query(F.data.startswith("move"))
async def handle_move(callback: types.CallbackQuery, state: FSMContext):
    _, user_id, row, col = callback.data.split(":")
    user_id = int(user_id)
    row, col = int(row), int(col)

    game = games.get(user_id)
    if not game:
        await callback.answer("Игра не найдена. Начните новую игру с помощью /start.")
        return

    if game["turn"] != "❌":
        await callback.answer("Сейчас не ваш ход!")
        return

    # Сделать ход игрока
    game["board"][row][col] = "❌"
    game["turn"] = "⭕"

    # Проверить победителя после хода игрока
    winner = check_winner(game["board"])
    if winner:
        await callback.message.edit_text(
            f"Игра окончена! Победитель: {winner}\n\n" + render_board_text(game["board"])
        )
        games.pop(user_id, None)
        await state.clear()
        return

    # Проверить ничью
    if all(cell != "⬜" for row in game["board"] for cell in row):
        await callback.message.edit_text(
            "Игра окончена! Ничья.\n\n" + render_board_text(game["board"])
        )
        games.pop(user_id, None)
        await state.clear()
        return

    # Ход бота
    await bot_move(callback, user_id, state)

def render_board_text(board):
    """Создает текстовое представление игрового поля."""
    return "\n".join(["".join(row) for row in board])

async def bot_move(callback: types.CallbackQuery, user_id: int, state: FSMContext):
    game = games[user_id]

    # Найти все свободные клетки
    free_cells = [(i, j) for i, row in enumerate(game["board"]) for j, cell in enumerate(row) if cell == "⬜"]
    if not free_cells:
        return

    # Сделать случайный ход
    row, col = choice(free_cells)
    game["board"][row][col] = "⭕"
    game["turn"] = "❌"

    # Проверить победителя после хода бота
    winner = check_winner(game["board"])
    if winner:
        await callback.message.edit_text(
            f"Игра окончена! Победитель: {winner}\n\n" + render_board_text(game["board"])
        )
        games.pop(user_id, None)
        await state.clear()
        return

    # Проверить ничью
    if all(cell != "⬜" for row in game["board"] for cell in row):
        await callback.message.edit_text(
            "Игра окончена! Ничья.\n\n" + render_board_text(game["board"])
        )
        games.pop(user_id, None)
        await state.clear()
        return

    # Продолжить игру
    await callback.message.edit_text(
        "Ваш ход:",
        reply_markup=render_board_inline(game["board"], user_id)
    )

def check_winner(board):
    # Проверка строк, столбцов и диагоналей
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "⬜":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "⬜":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != "⬜":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "⬜":
        return board[0][2]
    return None