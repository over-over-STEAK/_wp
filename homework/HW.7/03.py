from typing import List, Dict

def classify_even_odd(numbers: List[int]) -> Dict[str, List[int]]:
    return {
        'even': [num for num in numbers if num % 2 == 0],
        'odd':  [num for num in numbers if num % 2 != 0]
    }

# 測試
print(classify_even_odd([1, 2, 3, 4, 5, 6]))        # {'even': [2, 4, 6], 'odd': [1, 3, 5]}
print(classify_even_odd([-3, -2, -1, 0, 1, 2, 3]))  # {'even': [-2, 0, 2], 'odd': [-3, -1, 1, 3]}
print(classify_even_odd([]))                       # {'even': [], 'odd': []}
