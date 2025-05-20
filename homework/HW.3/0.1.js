function countLetters(str) {
  const letterMap = new Map();
  for (const char of str) {
    if (/^[a-zA-Z]$/.test(char)) {
      letterMap.set(char, (letterMap.get(char) || 0) + 1);
    }
  }
  return letterMap;
}
