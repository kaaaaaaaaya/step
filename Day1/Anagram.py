def binary_search(word,dictionary, left, right):
    result = []
    if left > right:
        return []
    mid = (left + right)//2
    if word == dictionary[mid][0]:
        i = mid
        while word == dictionary[i][0] and i >= 0:
            i -= 1
        i += 1
        while i < len(dictionary) and dictionary[i][0] == word:
            result.append(dictionary[i][1])
            i += 1
        return result
    elif word < dictionary[mid][0]:
        right = mid - 1
        return binary_search(word,dictionary, left, right)
    else:
        left = mid + 1
        return binary_search(word,dictionary, left, right)

def search_anagrams(test_word,dictionary_word):
    ans = []
    n = len(dictionary_word)
    for word in test_word:
        ans.append(binary_search(word, dictionary_word, 0, n))
    return ans

with open("words.txt", mode='r') as f1, open("test.txt", mode="r") as f2:
    dictionary_word = []
    for line_1 in f1:
        dictionary_word.append(line_1.strip())

    test_word = []
    for line_2 in f2:
        test_word.append(line_2.strip())

    n = len(test_word)
    for i in range(n):
        test_word[i] = "".join(sorted(test_word[i]))

    n = len(dictionary_word)
    for i in range(n):
        dictionary_word[i] = ("".join(sorted(dictionary_word[i])),dictionary_word[i])
    dictionary_word.sort()

    ans = search_anagrams(test_word, dictionary_word)

    for i in range(len(test_word)):
        print(f"{test_word[i]}: {ans[i]}")