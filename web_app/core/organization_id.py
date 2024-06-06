import sys
from functools import reduce


def is_inn_valid(id: str) -> bool:
    def __calculate_control_sum(inn: list[int], k: list[int]) -> int:
        """Возвращает младшую цифру остатка деления на 11 суммы произведений весовых коэффициентов на цифры в ИНН"""
        return reduce(lambda accum, element: accum + element[0] * element[1], zip(k, inn), 0) % 11 % 10

    if not isinstance(id, str):
        return False
    inn_as_list_of_int = [int(x) for x in id]
    weight = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    control_sum = inn_as_list_of_int[-1]
    match len(inn_as_list_of_int):
        case 10: k = weight[2:11]
        case 12:
            control_sum_1 = __calculate_control_sum(inn_as_list_of_int, weight[1:11])
            if control_sum_1 != inn_as_list_of_int[-2]:
                return False
            k = weight
        case _: return False
    return control_sum == __calculate_control_sum(inn_as_list_of_int, k)


if __name__ == '__main__':
    print(is_inn_valid("123456789431"))
    print(is_inn_valid("1234567894"))
    print(is_inn_valid("1234567894310"))
    print(is_inn_valid("12345678"))
    print(is_inn_valid(12345678))


