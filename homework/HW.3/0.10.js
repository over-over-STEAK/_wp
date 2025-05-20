class EventEmitter {
    constructor() {
        this.events = {};
    }

    on(eventName, listener) {
        if (!this.events[eventName]) {
            this.events[eventName] = [];
        }
        this.events[eventName].push(listener);
    }

    off(eventName, listener) {
        if (!this.events[eventName]) return;
        const idx = this.events[eventName].indexOf(listener);
        if (idx >= 0) {
            this.events[eventName].splice(idx, 1);
        }
    }

    emit(eventName, ...args) {
        if (!this.events[eventName]) return;
        this.events[eventName].forEach(listener => listener(...args));
    }
}
