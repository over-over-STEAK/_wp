class Animal {
    constructor(name) {
      this.name = name;
    }
    speak() {}
  }
  
  class Dog extends Animal {
    speak() {
      return `Woof! I am ${this.name}`;
    }
  }
  
