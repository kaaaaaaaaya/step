import string
def is_include(test, dictionary):
    return all(test.get(key, False) >= count for key, count in dictionary.items())

def word_match(word,dictionary):
    result = []
    for i in range(len(dictionary)):
        if is_include(word, dictionary[i][0][0]):
            result.append((dictionary[i][1], dictionary[i][0][1])) #結果 点数
    return result

def count_binary_search(word, left, right):
    alp = list(string.ascii_lowercase)
    if left > right:
        return []
    mid = (left + right)//2
    if word == alp[mid]:
        return alp[mid]
    elif word < alp[mid]:
        right = mid - 1
        return count_binary_search(word, left, right)
    else:
        left = mid + 1
        return count_binary_search(word, left, right)
    
def count_binary_search_all(word):
    word_count = {ch : 0 for ch in string.ascii_lowercase}
    SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    WORD_SCORES = {ch: i for ch, i in zip(string.ascii_lowercase, SCORES)}
    scores = 0
    for i in range(len(word)):
        word_count[count_binary_search(word[i], 0, 25)] += 1
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

with open("words.txt", mode='r') as f1, open("large.txt", mode="r") as f2, open("laege_answer.txt", mode="w") as a:
    dictionary_word = []
    for line_1 in f1:
        dictionary_word.append(line_1.strip())

    test_word = []
    for line_2 in f2:
        test_word.append(line_2.strip())

    test_word_count = []
    dictionary_word_count = []
    for i in range(len(test_word)):
        test_word_count.append(count_binary_search_all(test_word[i]))

    for i in range(len(dictionary_word)):
        dictionary_word_count.append((count_binary_search_all(dictionary_word[i]),dictionary_word[i]))

    ans = search_anagrams(test_word_count, dictionary_word_count)
    answer = []
    for i in range(len(test_word)):
        maxscore = max_score(ans[i])
        print(f"最高点： {maxscore[0]} → ワード: {test_word[i]}、アナグラム： {maxscore[1]}")
        answer.append(maxscore[1] + "\n")

    a.writelines(answer)