function deepMerge(obj1, obj2) {
    for (const key in obj2) {
      if (obj2.hasOwnProperty(key)) {
        const val1 = obj1[key];
        const val2 = obj2[key];
        if (
          typeof val1 === 'object' && val1 !== null && !Array.isArray(val1) &&
          typeof val2 === 'object' && val2 !== null && !Array.isArray(val2)
        ) {
          deepMerge(val1, val2); 
        } else {
          obj1[key] = val2;
        }
      }
    }
    return obj1;
  }
  
