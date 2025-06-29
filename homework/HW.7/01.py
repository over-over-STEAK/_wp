from typing import List, Optional

def find_max(numbers: List[int]) -> Optional[int]:
    if not numbers:
        return None  
    max_num = numbers[0]
    for num in numbers[1:]:
        if num > max_num:
            max_num = num
    return max_num

print(find_max([10]))              # 輸出: 10
print(find_max([3, 55, 11, 91, -2]))  # 輸出: 91
print(find_max([-180, -5, -37]))   # 輸出: -5
