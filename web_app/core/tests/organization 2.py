import random


def random_organization_id() -> str:
    # Щепотка цифр
    str1 = '0123456789012345678901234567890123456789'

    # Преобразуем получившуюся строку в список
    ls1 = list(str1)

    # Тщательно перемешиваем список
    random.shuffle(ls1)
    # Извлекаем из списка 10 произвольных значений
    random_id1 = ''.join([random.choice(ls1) for x in range(10)])

    # Тщательно перемешиваем список
    random.shuffle(ls1)
    # Извлекаем из списка 12 произвольных значений
    random_id2 = ''.join([random.choice(ls1) for x in range(12)])

    ids = [random_id1, random_id2]
    random.shuffle(ids)
    return ids[0]


if __name__ == '__main__':
    print(random_organization_id())
