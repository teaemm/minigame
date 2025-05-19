import random

def knb():
    return random.randint(1, 3)
    if knb == 1:
        answerknb = "Камень"
    elif knb == 2:
        answerknb = "Ножницы"
    elif knb == 3:
        answerknb = "Бумага"
    print("Выпало: ", answerknb)

