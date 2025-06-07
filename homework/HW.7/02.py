from typing import List, Optional

def average(nums: List[float]) -> Optional[float]:
    if not nums:
        return None
    return round(sum(nums) / len(nums), 1)

print(average([1, 2, 3, 4, 5, 6]))     # 3.5
print(average([-3, 5, -2]))            # 0.0
print(average([]))                    # None
