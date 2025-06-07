def char_frequency(s):
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq

print(char_frequency("hello world!"))
print(char_frequency("abcde"))
print(char_frequency(""))
