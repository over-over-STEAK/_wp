function* fibonacciGenerator() {
    let a = 0, b = 1;
    yield a;
    yield b;
    while (true) {
        const nextVal = a + b;
        yield nextVal;
        a = b;
        b = nextVal;
    }
}

const fib = fibonacciGenerator();
console.log(fib.next().value); // 0
console.log(fib.next().value); // 1
console.log(fib.next().value); // 1
console.log(fib.next().value); // 2
console.log(fib.next().value); // 3
console.log(fib.next().value); // 5
console.log(fib.next().value); // 8
