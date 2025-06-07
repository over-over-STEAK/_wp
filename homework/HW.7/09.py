def most_common_verbose(nums):
    if not nums:
        return None, 0

    counts = {}
    for num in nums:
        counts[num] = counts.get(num, 0) + 1

    max_num = max(counts, key=counts.get)
    return max_num, counts[max_num]

# 測試
val, freq = most_common_verbose([1, 2, 2, 3, 3])
print(f"最多的是 {val}，出現 {freq} 次")  # 最多的是 2 或 3，出現 2 次
