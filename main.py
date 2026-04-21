import code49 as c49

import os
import time


# Decoder
def decode(code: list) -> str:
    """
    args:
        code: Code49条码读取出的pattern，条码每行的数据为列表中的一个元素，每行数据前后需要有起始符的11与终止符的4

    return:
        解码完的结果
    """

    global success
    success = True

    code_value = []  # 存储条码的值
    for i, row in enumerate(code):
        # Extract pattern, remove head '11' and tail '4'
        if len(row) != 35:
            print(f"\033[1;41m[ERROR]\033[0m: Row{i + 1} length incorrect")
            success = False

        ptrn = row
        if row[:2] == '11':
            ptrn = ptrn[2:]
        if row[-1:] == '4':
            ptrn = ptrn[:-1]

        # For each symbol
        row_value = []  # 存储每行的值
        for j in range(4):
            # Get value
            value = None
            try:
                if c49.ROW_PARITY[i][j] == '0' or len(code) == i + 1:
                    value = c49.EVEN_PARITY_PATTERNS.index(ptrn[j << 3:(j + 1) << 3])
                else:
                    value = c49.ODD_PARITY_PATTERNS.index(ptrn[j << 3:(j + 1) << 3])
            except ValueError as err:
                print(f"\033[1;41m[ERROR]\033[0m: Row{i + 1} Word{j + 1} {err} Please Check pattern!")
                value = 'N/A'
                success = False

            row_value.append(value)
        code_value.append(row_value)

    code_character_value = []  # 存储条码字符值
    print("\nValue:")
    for i, row_value in enumerate(code_value):
        print(f"Row{i + 1}: {row_value}")

        row_character_value = []  # 存储每行的字符值
        for value in row_value:
            if value != 'N/A':
                c1, c2 = value // 49, value % 49
                row_character_value.append(c1)
                row_character_value.append(c2)
            else:
                row_character_value.append('N/A')
                row_character_value.append('N/A')

        code_character_value.append(row_character_value)

    # 检查每行校验字符
    i = 0
    print("\nCharacter Value:")
    for row_character_value in code_character_value:
        row_sum = 0
        for character_value in row_character_value[:-1]:
            if character_value != 'N/A':
                row_sum += character_value

        if row_sum % 49 == row_character_value[-1]:
            print(f"Row{i + 1}: {row_character_value} \033[1;32mCorrect!\033[0m")
        else:
            print(f"Row{i + 1}: {row_character_value} \033[1;30;41m[ERROR]\033[0m")
            success = False
        i += 1

    # 检查校验词
    row_len = len(code)
    try:
        symbol_check_character1 = 38 * code_character_value[-1][6]
        symbol_check_character2 = 16 * code_character_value[-1][6] + c49.Y_WEIGHTS[(row_len - 1) * 4] * code_value[-1][0]
        symbol_check_character3 = 20 * code_character_value[-1][6] + c49.X_WEIGHTS[(row_len - 1) * 4] * code_value[-1][0] + c49.X_WEIGHTS[(row_len - 1) * 4 + 1] * code_value[-1][1]
        for i in range(row_len - 1):
            for j in range(4):
                symbol_check_character1 += c49.Z_WEIGHTS[i * 4 + j] * code_value[i][j]
                symbol_check_character2 += c49.Y_WEIGHTS[i * 4 + j] * code_value[i][j]
                symbol_check_character3 += c49.X_WEIGHTS[i * 4 + j] * code_value[i][j]
        symbol_check_character1 = symbol_check_character1 % 2401
        symbol_check_character2 = symbol_check_character2 % 2401
        symbol_check_character3 = symbol_check_character3 % 2401

        if row_len <= 6:  # 行数小于等于6时有两个校验词
            if symbol_check_character2 == code_value[-1][1] and symbol_check_character3 == code_value[-1][2]:
                print("\nTotal Code Check: \033[1;32mCorrect!\033[0m")
            else:
                success = False
                print("\nTotal Code Check: \033[1;41m[ERROR]\033[0m")
        elif row_len == 7 or row_len == 8:  # 行数为7或8时有三个校验词
            if symbol_check_character2 == code_value[-1][1] and symbol_check_character3 == code_value[-1][2] and symbol_check_character1 == code_value[-1][0]:
                print("\nTotal Code Check: \033[1;32mCorrect!\033[0m")
            else:
                success = False
                print("\nTotal Code Check: \033[1;41m[ERROR]\033[0m")
    except Exception:
        success = False
        print("\nTotal Code Check: \033[1;41m[ERROR]\033[0m")

    # 将字符值解码为字符
    code_character = []  # 存储字符
    for i, row_character_value in enumerate(code_character_value):

        # 计算最后一行的模式数字
        if i + 1 == row_len:
            if row_character_value[-2] != 'N/A':
                starting_mode = row_character_value[-2] - 7 * (row_len - 2)
                if starting_mode < 0 or starting_mode > 6:
                    starting_mode = 'N/A'
            else:
                starting_mode = 'N/A'

        # 将每行的前7个字符值解码为字符
        # 忽略每行的最后一个字符（校验字符）
        for j, character_value in enumerate(row_character_value):
            if j != 7:
                if character_value != 'N/A':
                    code_character.append(c49.CHAR_MAP[character_value])
                else:
                    code_character.append('N/A')

    # 处理起始模式
    print(f"\nMode:{starting_mode}")
    match starting_mode:
        case 0:
            pass
        case 4:
            code_character.insert(0, 'S1')
        case 5:
            code_character.insert(0, 'S2')
        case _:
            print("\033[0;31mdecode as mode 0\033[0m")
            success = False

    # 删除校验词与模式字符
    if row_len <= 6:  # 行数小于等于6时有两个校验词
        code_character[-5:] = []
    elif row_len == 7 or row_len == 8:  # 行数为7或8时有三个校验词
        code_character[-7:] = []
    print("\nCode Character(Without Check Characters):")
    print(code_character)

    # 将字符解码为ASCII字符
    # buffer为char的前一个字符
    mode = 0
    buffer = None
    output = ''
    for i, char in enumerate(code_character):
        if char != 'N/A':
            if char == '<NS>':
                if len(code_character) == i + 1:  # <NS>后面没东西了（后面是校验词） 结束
                    break
                else:
                    if code_character[i + 1] == '<NS>':  # <NS>后面是<NS>
                        pass
                    else:  # <NS>后面有东西 切换字母数字/数字模式
                        if mode == 0:
                            mode = 1
                        elif mode == 1:
                            mode = 0
                    continue

            match mode:
                case 0:  # 字母数字模式
                    if buffer == 'S2' or buffer == 'S1':  # 前一个字符为S1/S2 相加后解码
                        output += chr(c49.ASCII_CHAR_MAP.index(buffer + char))

                    else:  # 前一个字符不是S1/S2 判断当前字符
                        if char == 'S2' or char == 'S1':  # 当前字符是S1/S2 直接进行下一个循环
                            pass
                        else:
                            output += chr(c49.ASCII_CHAR_MAP.index(char))
                case 1:  # 数字模式(还没写)
                    pass

            buffer = char
        else:
            buffer = ''
            output += '[N/A]'
            success = False

    return output


def choose_example() -> list:
    os.system("cls")
    print("选择示例条码\n"
          "\033[96m1.二阶段条码\n2.三阶段条码\n\033[0m")
    cmd = input("\033[92m> \033[0m")
    try:
        cmd = int(cmd)
    except Exception as err:
        print(f"输入错误:{err}")

    match cmd:
        case 1:
            # 二阶段Code49
            code = [
                '11143121314115211131114321124131314',
                '11221611211411251111225122311314214',
                '11123232212411212332131231332321114',
                '11251311211242114112215212413213114',
                '11123121511212521211113243422213114',
                '11224211311211313421211153141112154'
            ]
        case 2:
            # 三阶段Code49
            code = [
                '11134121223121221412111433421123214',
                '11212252111231233112152122311314214',
                '11112411421115123211311315411311414'
            ]
        case _:
            raise ValueError("输入错误")

    print(f"示例Code49条码{cmd}：\n\033[96mcode\033[0m = \033[93m[\033[0m")
    for r in code:
        print(f"    '{r}',")
    print("\033[93m]\033[0m")
    _ = input("按Enter进行解码")
    return code


def main_menu() -> None:
    """打印主菜单"""
    print("Code49 Decoder")
    print("=" * 20)
    print("""\033[96m选择输入方式
1.从txt文件输入
2.查看示例
0.退出程序\033[0m
输入数字后按Enter
使用方法见 https://github.com/Leo-455/code49-decoder""")


def read_from_txt():
    """从 txt 文件中读取code"""
    os.system("cls")
    print("请输入txt文件路径\n若在同一目录下，可输入文件名")
    path = input("\033[92m> \033[0m")
    if not path.lower().endswith(".txt"):
        path += ".txt"

    try:
        with open(path, 'r', encoding="utf-8") as file:
            code = [x.strip().replace("_", "") for x in file.readlines() if x.strip()]
    except Exception as err:
        print(f"txt读取失败：{err}")
        return None

    print(f"读取Code49条码{path}：\n\033[96mcode\033[0m = \033[93m[\033[0m")
    for r in code:
        print(f"    '{r}',")
    print("\033[93m]\033[0m")
    _ = input("按Enter进行解码")

    return code


def save_result(result: str) -> None:
    """
    将解码结果保存到文件中

    Args:
        result: 要保存的结果
    """
    t = time.strftime("%Y-%m-%d %H-%M", time.localtime())
    default_path = f"result_{t}.txt"

    print(f"请输入文件名，留空使用默认文件名{default_path}")
    path = input("\033[92m> \033[0m")

    if path == '':
        path = default_path
    if not path.lower().endswith(".txt"):
        path += ".txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"\033[92m{path} 保存成功\033[0m")


def main() -> None:
    global success
    while True:
        try:
            os.system("cls")
            text = ""
            success = None

            main_menu()
            cmd = input("\033[92m> \033[0m")

            try:
                cmd = int(cmd)
            except ValueError:
                _ = input("请输入数字\n按Enter继续")
                continue

            match cmd:
                case 0:
                    break

                case 1:
                    code = read_from_txt()
                    if code:
                        text = decode(code)

                case 2:
                    code = choose_example()
                    if code:
                        text = decode(code)

                case _:
                    _ = input("输入错误\n按Enter继续")
                    continue

            if success is True:
                print("\ndecode \033[1;32mSUCCESS!\033[0m")
                print("Result:")
                print(text)
            elif success is False:
                print("\033[0;31m\nERROR occurred during decode The result might be wrong.\033[0m")
                print("Result:")
                print(text)
            elif success is None:
                _ = input("按Enter继续")
                continue

            print("\n是否保存结果？[y/n]")
            cmd = input("\033[92m> \033[0m")
            match cmd.lower():
                case "y":
                    save_result(text)
                case "n":
                    pass
                case _:
                    continue

            _ = input("按Enter继续")
        except Exception as err:
            print(err)
            _ = input("按Enter继续")


# Main entry
if __name__ == '__main__':
    main()
