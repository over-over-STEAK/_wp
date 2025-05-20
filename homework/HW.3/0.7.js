class Vector {
    constructor(components) {
      this.components = components;
    }
  
    add(other) {
      if (this.components.length !== other.components.length) {
        throw new Error("Vectors must have same dimensions");
      }
      return new Vector(
        this.components.map((val, i) => val + other.components[i])
      );
    }
  
    subtract(other) {
      if (this.components.length !== other.components.length) {
        throw new Error("Vectors must have same dimensions");
      }
      return new Vector(
        this.components.map((val, i) => val - other.components[i])
      );
    }
  
    dot(other) {
      if (this.components.length !== other.components.length) {
        throw new Error("Vectors must have same dimensions");
      }
      return this.components.reduce(
        (sum, val, i) => sum + val * other.components[i],
        0
      );
    }
  }
  
  
  
