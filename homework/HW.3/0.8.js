function delayedSum(a, b, delay) {
    return new Promise((resolve) => {
        setTimeout(() => resolve(a + b), delay);
    });
}

delayedSum(3, 7, 1000).then(console.log); 
