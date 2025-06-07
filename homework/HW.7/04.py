from typing import List

def get_stars(n: int) -> List[str]:
    """回傳一個星星階梯的字串清單（不直接印出）。"""
    return ['*' * i for i in range(1, n + 1)]

# 若需要印出：
for line in get_stars(3):
    print(line)
