function filterArray(arr, predicate) {
    const filtered = [];
    for (const element of arr) {
      if (predicate(element)) {
        filtered.push(element);
      }
    }
    return filtered;
  }
