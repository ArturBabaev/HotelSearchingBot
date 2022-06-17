def ending(num: int) -> str:
    """
    Required ending
    :param num: Quantity
    :type: int
    :return: Ending
    :type: str
    """
    if num % 100 in [0, 10, 11, 12, 13, 14]:
        return 'ей'
    elif num % 10 in [2, 3, 4]:
        return 'я'
    elif num % 10 in [1]:
        return 'ь'
    elif num % 10 in [0, 5, 6, 7, 8, 9]:
        return 'ей'
