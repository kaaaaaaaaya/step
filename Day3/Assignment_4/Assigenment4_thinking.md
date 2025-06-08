# Assignment3 の考え方
## 課題内容
abs(), int(), round() に対応しよう
例: abs(-2.2) => 2.2 （絶対値）
    int(1.55) => 1（小数を切捨てる）
    round(1.55) => 2（四捨五入）


## 考え方
[Assignment3](https://github.com/kaaaaaaaaya/step/blob/main/Day3/Assignment_3/assignment3.py)で実装した
括弧の再帰構造を利用して、括弧の前に「abs」、「int」、「round」があれば、
それぞれabs = True 、int = True、round = Trueとし、同じ再起構造を呼び出す。

### 仕様
- abs()
    - 括弧内の式の絶対値を返す
- int()
    - 括弧内の式の小数点以下を切り捨てたものを返す
- round()
    - 括弧内の式を四捨五入したものを返す

### 実装したテストコード
- abs
    - 括弧内が正
        - test("abs(2-1)")
        - test("abs(2.8-1)")
        - test("abs(2.2-1)")
    - 括弧内が負
        - test("abs(1-2)")
        - test("abs(1.2-2)")
        - test("abs(1.6-2)")
    括弧内が0
        - test("abs(2-2)")
- int
    - 括弧内が正
        - test("int(2-1)")
        - test("int(2.1-1)")
        - test("int(2.6+2)") 
    - 括弧内が負
        - test("int(1-2)")
        - test("int(1-2.8)") 
        - test("int(1-2.2)") 
    - 括弧内が0
        - test("int(2-2)")
- round
    - 括弧内が正
        - test("round(2-1)")
        - test("round(3.2-1)")
        - test("round(5.6+2)") 
    - 括弧内が負
        - test("round(1-2)")
        - test("round(1-7.2)") 
        - test("round(1-2.3)") 
    - 括弧内が0
        - test("round(2-2)")
- 混合
    - test("abs(1.2)+abs(round(-1+4))")
    - test("int(1.2-0.7)+round(abs(-1*8.9))")
    - test("abs(int(round(-1.55)+abs(int(-2.3+4))))")