import code49 as c49


# Decoder
def decode(code: list) -> str:
    """
    args:
        code: Code49条码读取出的pattern，条码每行的数据为列表中的一个元素，每行数据前后需要有起始符的11与终止符的4

    return:
        解码完的结果
    """

    code_value = []  # 存储条码的值
    for i, row in enumerate(code):
        # Extract pattern, remove head '11' and tail '4'
        ptrn = row[2:-1]

        # For each symbol
        row_value = []  # 存储每行的值
        for j in range(4):
            # Get value
            value = None
            if c49.ROW_PARITY[i][j] == '0' or len(code) == i + 1:
                value = c49.EVEN_PARITY_PATTERNS.index(ptrn[j << 3:(j + 1) << 3])
            else:
                value = c49.ODD_PARITY_PATTERNS.index(ptrn[j << 3:(j + 1) << 3])

            row_value.append(value)
        code_value.append(row_value)

    code_character_value = []  # 存储条码字符值
    print("Value:")
    for i, row_value in enumerate(code_value):
        print(f"Row{i + 1}: {row_value}")

        row_character_value = []  # 存储每行的字符值
        for value in row_value:
            c1, c2 = value // 49, value % 49
            row_character_value.append(c1)
            row_character_value.append(c2)

        code_character_value.append(row_character_value)

    # 检查每行校验字符
    i = 0
    print("\nCharacter Value:")
    for row_character_value in code_character_value:
        row_sum = 0
        for character_value in row_character_value[:-1]:
            row_sum += character_value

        if row_sum % 49 == row_character_value[-1]:
            print(f"Row{i + 1}: {row_character_value} Correct!")
        else:
            print(f"Row{i + 1}: {row_character_value} [ERROR]")
        i += 1

    # 将字符值解码为字符
    code_character = []  # 存储字符
    row_len = len(code)
    for i, row_character_value in enumerate(code_character_value):

        # 计算最后一行的模式数字
        if i + 1 == row_len:
            starting_mode = row_character_value[-2] - 7 * (row_len - 2)

        # 将每行的前7个字符值解码为字符
        # 忽略每行的最后一个字符（校验字符）
        for j, character_value in enumerate(row_character_value):
            if j != 7:
                code_character.append(c49.CHAR_MAP[character_value])

    # 模式5需要在最开头加入一个S2
    print(f"\nMode:{starting_mode}")
    match starting_mode:
        case 0:
            pass
        case 5:
            code_character.insert(0, 'S2')

    # 删除校验词与模式字符
    code_character[-5:] = []
    print("\nCode Character(Whitout Check Characters):")
    print(code_character)

    # 将字符解码为ASCII字符
    # buffer为char的前一个字符
    buffer = None
    output = ''
    for char in code_character:

        if buffer == 'S2' or buffer == 'S1':  # 前一个字符为S1/S2 相加后解码
            output += chr(c49.ASCII_CHAR_MAP.index(buffer + char))

        else:  # 前一个字符不是S1/S2 判断当前字符
            if char == 'S2' or char == 'S1':  # 当前字符是S1/S2 直接进行下一个循环
                pass
            elif char == '<NS>':
                break
            else:
                output += chr(c49.ASCII_CHAR_MAP.index(char))

        buffer = char

    return output


# Main entry
if __name__ == '__main__':
    # Test encoder
    # test.test_cases()

    # Decode

    # 二阶段Code49
    code = [
      '11143121314115211131114321124131314',
      '11221611211411251111225122311314214',
      '11123232212411212332131231332321114',
      '11251311211242114112215212413213114',
      '11123121511212521211113243422213114',
      '11224211311211313421211153141112154'
    ]

    # 三阶段Code49
    # code = [
    #   '11134121223121221412111433421123214',
    #   '11212252111231233112152122311314214',
    #   '11112411421115123211311315411311414'
    # ]

    text = decode(code)
    print("\nResult:")
    print(text)
