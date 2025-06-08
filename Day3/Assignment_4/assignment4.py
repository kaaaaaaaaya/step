#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_mult(line, index):
    token = {'type': 'MULT'}
    return token, index + 1


def read_div(line, index):
    token = {'type': 'DIV'}
    return token, index + 1

def subcall(line, index, tokens, to_abs = False, to_int = False, to_round = False):
    index += 1
    sub_tokens, index = tokenize(line, index)
    answer = evaluate(sub_tokens)
    ### 修正したい
    if answer < 0:
        if to_abs:
            return ({'type': 'NUMBER', 'number': answer * -1}, index)
        else:
            if to_int:
                answer = int(answer)
            elif to_round:
                answer = round(answer)
            (token, index) = ({'type': 'MINUS'}, index)
            tokens.append(token)
            return ({'type': 'NUMBER', 'number': answer * -1}, index)
    else:
        if to_int:
            answer = int(answer)
        elif to_round:
            answer = round(answer)
        return ({'type': 'NUMBER', 'number': answer}, index)
    ###

def tokenize(line,index):
    tokens = []
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_mult(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        elif line[index] == 'a' and line[index + 1] == 'b' and line[index + 2] == 's':
            if line[index + 3] == '(':
                index = index + 3
                (token, index) = subcall(line,index, tokens, to_abs = True)
            else:
                print("syntax error")
        elif line[index] == 'i' and line[index + 1] == 'n' and line[index + 2] == 't':
            if line[index + 3] == '(':
                index = index + 3
                (token, index) = subcall(line,index, tokens, to_int = True)
            else:
                print("syntax error")
        elif line[index] == 'r' and line[index + 1] == 'o' and line[index + 2] == 'u' and line[index + 3] == 'n' and line[index + 4] == 'd':
            if line[index + 5] == '(':
                index = index + 5
                (token, index) = subcall(line,index, tokens, to_round = True)
            else:
                print("syntax error")
        elif line[index] == '(':
            (token, index) = subcall(line,index, tokens)
            print(token)
        elif line[index] == ')':
            index += 1
            return tokens, index
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens, index

def calculation_mult_div(tokens,index,minus):
    positive = 1
    if minus == 1:
        positive = -1
    if tokens[index - 1 - minus]['type'] == 'MULT':
        result = tokens[index - 2 - minus]['number'] * tokens[index]['number'] * positive
    elif tokens[index - 1 - minus]['type'] == 'DIV':
        assert tokens[index]['number'] != 0, 'Cannot be devided by 0'
        result = tokens[index - 2 - minus]['number'] * positive / tokens[index]['number']
    tokens[index - 2 - minus: index + 1] = [{'type': 'NUMBER', 'number': result}]

def calculation_plus_minus(tokens,index,minus, answer):
    positive = 1
    if minus == 1:
        positive = -1
    if tokens[index - 1 - minus]['type'] == 'PLUS':
        answer += tokens[index]['number'] * positive
    elif tokens[index - 1 - minus]['type'] == 'MINUS':
        answer -= tokens[index]['number'] * positive
    return answer

def evaluate(tokens):
    # * / の計算
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MINUS' and tokens[index - 2]['type'] in {"MULT", "DIV"}:
                calculation_mult_div(tokens, index, 1)
            elif tokens[index - 1]['type'] in {"MULT", "DIV"}:
                calculation_mult_div(tokens, index, 0)
        index += 1

    # + - の計算
    index = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    answer = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MINUS' and tokens[index - 2]['type'] in {"PLUS", "MINUS"}:
                answer = calculation_plus_minus(tokens, index, 1, answer)
            elif tokens[index - 1]['type'] in {"PLUS", "MINUS"}:
                answer = calculation_plus_minus(tokens, index, 0, answer)
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens, _ = tokenize(line, index = 0)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def test_division_by_zero():
    try:
        test("12020/0")
        print("FAIL! Expected assertion error for division by zero")
    except AssertionError as e:
        print("PASS! Caught expected assertion error:", e)

def run_test():
    print("==== Test started! ====")
    #abs
    #括弧内が正
    test("abs(2-1)")
    test("abs(2.8-1)")
    test("abs(2.2-1)")
    #括弧内が負
    test("abs(1-2)")
    test("abs(1.2-2)")
    test("abs(1.6-2)")
    #括弧内が0
    test("abs(2-2)")

    #int
    #括弧内が正
    test("int(2-1)")
    test("int(2.1-1)")
    test("int(2.6+2)") 
    #括弧内が負
    test("int(1-2)")
    test("int(1-2.8)") 
    test("int(1-2.2)") 
    #括弧内が0
    test("int(2-2)")

    #round
    #括弧内が正
    test("round(2-1)")
    test("round(3.2-1)")
    test("round(5.6+2)") 
    #括弧内が負
    test("round(1-2)")
    test("round(1-7.2)") 
    test("round(1-2.3)") 
    #括弧内が0
    test("round(2-2)")

    #混合
    test("abs(1.2)+abs(round(-1+4))")
    test("int(1.2-0.7)+round(abs(-1*8.9))")
    test("abs(int(round(-1.55)+abs(int(-2.3+4))))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens, _ = tokenize(line,index = 0) #←括弧のない時はindexを返す必要がないのでsubcallを追加してみたのですがうまくいきませんでした。
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)