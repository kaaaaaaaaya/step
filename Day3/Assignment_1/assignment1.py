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


def tokenize(line):
    tokens = []
    index = 0
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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

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
    if minus == 1:
        index -= 3
        return index
    else:
        index -= 2
        return index

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
                index = calculation_mult_div(tokens, index, 1)
            elif tokens[index - 1]['type'] in {"MULT", "DIV"}:
                index = calculation_mult_div(tokens, index, 0)
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
    tokens = tokenize(line)
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
    test("1+2")
    test("1.0+2.1-3")
    #掛け算
    test("8*3") #1桁*1桁
    test("23*5") #2桁*1桁
    test("395*12") #3桁*2桁

    test("2*-4") #かける数が負の数
    test("-10*20") #かけられる数が負の数

    test("1*2*3")#複数回かける
    test("1*-2*3")#複数回かける(負)

    test("12020*0") #0をかける
    test("0*103") #0にかける

    test("3.14*1.59") #小数
    test("3.1*4.1592") #桁違い
    
    #割り算
    test("8/4") #1桁/1桁
    test("24/6") #2桁/1桁
    test("400/20") #3桁/2桁

    test("9/4") #1桁/1桁
    test("23/6") #2桁/1桁
    test("400/17") #3桁/2桁

    test("1/2") #1桁/1桁
    test("4/9") #1桁/1桁
    test("20/400") #2桁/3桁

    test("12/-2") #割る数が負の数
    test("-15/6") #割られる数が負の数

    test("8/4/2")#複数回割る
    test("-8/4/2")#複数回割る(負)

    test_division_by_zero() #0で割る
    test("0/103") #0を割る
     
    test("5.555/1.23") #小数
    test("5.5/1.2345") #桁違い

    #掛け算と割り算
    test("6/3*2*6/8/2") 
    test("6/3*2+6/8")

    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    print(line)
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)