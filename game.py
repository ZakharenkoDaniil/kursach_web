def check_word(expected, actual):
    if expected == actual:
        return 'Угадано'
    positions_match = 0
    symbols_match = 0
    symbols = {}
    for sym in expected:
        num = symbols.get(sym)
        if num is None:
            symbols.update({sym: 1})
        else:
            symbols.update({sym: num + 1})
    for sym in actual:
        num = symbols.get(sym)
        if num is not None:
            symbols_match += num
    min_len = min(len(expected), len(actual))
    actual = actual[:min_len]
    expected = expected[:min_len]
    for exp, act in zip(expected, actual):
        if exp == act:
            positions_match += 1
    print(expected, actual)
    result = "Угадано символов: {}\nУгадано позиций: {}".format(symbols_match, positions_match)
    return result
