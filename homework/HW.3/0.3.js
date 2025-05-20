function sumArraySafe(arr) {
    return arr
      .flat(Infinity)
      .filter(num => typeof num === 'number') 
      .reduce((sum, num) => sum + num, 0); 
  }
  
