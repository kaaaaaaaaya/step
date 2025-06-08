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

def subcall(line, index, tokens):
    index += 1
    sub_tokens, index = tokenize(line, index)
    answer = evaluate(sub_tokens)
    ### 修正したい
    if answer < 0:
        (token, index) = ({'type': 'MINUS'}, index)
        tokens.append(token)
        return ({'type': 'NUMBER', 'number': answer * -1}, index)
    else:
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
    #S -> ((S))
    test("(1+2)")
    test("(1.0+(2.1-3))")
    test("((8*2)+1)")
    test("((1+2)*3)") #和が先
    test("(4/(-3+1))") #差が先
    #S -> (S)(S)
    test("(8*3)+(1/1)") 
    test("(1+3)*(3-7)") 
    test("(4/2)-(2+1)")
    #S -> (S)S
    test("10*(1+1)") 
    test("(7-3)/2") 
    #複雑な計算
    test("-1+3*4*-1-15/5") 
    test("(1-2)+3*4*(5-6)-(7+8)/5")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens, _ = tokenize(line,index = 0) #←括弧のない時はindexを返す必要がないのでsubcallを追加してみたのですがうまくいきませんでした。
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)