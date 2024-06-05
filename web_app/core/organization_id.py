import sys
from functools import reduce


def is_inn_valid(id: str) -> bool:
    def __get_control_sum(inn: list[int], k: list[int]) -> int:
        return reduce(lambda accum, element: accum + element[0] * element[1], zip(k, inn), 0) % 11 % 10

    if not isinstance(id, str): return False
    inn = [int(x) for x in id]
    weight = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    match len(inn):
        case 10:
            k = weight[2:11]
        case 12:
            control_sum = __get_control_sum(inn, weight[1:11])
            if control_sum != inn[-2]:
                return False
            k = weight
        case _: return False
    control_sum = __get_control_sum(inn, k)
    return control_sum == inn[-1]


if __name__ == '__main__':
    print(is_inn_valid("123456789431"))
    print(is_inn_valid("1234567894"))
    print(is_inn_valid("1234567894310"))
    print(is_inn_valid("12345678"))
    print(is_inn_valid(12345678))


