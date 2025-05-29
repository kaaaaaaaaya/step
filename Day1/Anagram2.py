import string
def is_include(test, dictionary):
    return all(test.get(key, False) >= count for key, count in dictionary.items())

def word_match(word,dictionary):
    for i in range(len(dictionary)):
        if is_include(word, dictionary[i][0][0]):
            result = (dictionary[i][1], dictionary[i][0][1]) #結果 点数
            return result
    
def count_binary_search_all(word,WORD_SCORES):
    word_count = {ch : 0 for ch in string.ascii_lowercase}
    scores = 0
    for i in range(len(word)):
        word_count[word[i]] += 1
        scores += WORD_SCORES[word[i]]
    return (word_count, scores)

def search_anagrams(test_word_count,dictionary_word_count):
    ans = []
    for word in test_word_count:
        ans.append(word_match(word[0], dictionary_word_count))
    return ans

def max_score(ans):
    max = 0
    result = []
    for i in range(len(ans)):
        if max < ans[i][1]:
            max = ans[i][1]
            result = ans[i][0]
    return (max,result)

with open("words.txt", mode='r') as f1, open("large.txt", mode="r") as f2, open("large_answer.txt", mode="w") as a:
    dictionary_word = []
    for line_1 in f1:
        dictionary_word.append(line_1.strip())

    test_word = []
    for line_2 in f2:
        test_word.append(line_2.strip())

    test_word_count = []
    dictionary_word_count = []
    
    SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    WORD_SCORES = {ch: i for ch, i in zip(string.ascii_lowercase, SCORES)}
    for i in range(len(test_word)):
        test_word_count.append(count_binary_search_all(test_word[i],WORD_SCORES))

    for i in range(len(dictionary_word)):
        dictionary_word_count.append((count_binary_search_all(dictionary_word[i],WORD_SCORES),dictionary_word[i]))

    dictionary_word_count.sort(key=lambda x: x[0][1], reverse=True)

    ans = search_anagrams(test_word_count, dictionary_word_count)
    answer = []
    for i in range(len(test_word)):
        print(f"最高点： {ans[i][1]} → ワード: {test_word[i]}、アナグラム： {ans[i][0]}")
        answer.append(ans[i][0] + "\n")

    a.writelines(answer)