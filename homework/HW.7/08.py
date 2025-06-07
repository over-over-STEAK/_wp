def is_prime(n: int) -> bool:
    if n <= 1:
        print(f"{n} 不是質數（小於等於 1）")
        return False
    if n == 2:
        print(f"{n} 是質數")
        return True
    if n % 2 == 0:
        print(f"{n} 不是質數（是偶數）")
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            print(f"{n} 不是質數（可被 {i} 整除）")
            return False
    print(f"{n} 是質數")
    return True
