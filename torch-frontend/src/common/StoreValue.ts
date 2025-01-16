type EventCallback<T> = (value: T) => void;

export default class StoreValue<T>{
    private __value: T;
    private listeners: EventCallback<T>[] = [];

    constructor(value: T) {

        this.__value = value
    }

    public set value(value: T) {
        this.__value = value;
        this.notifyListeners(value);
    }

    public get value() {
        return this.__value;
    }

    subscribe(callback: EventCallback<T>) {
      this.listeners.push(callback);
      return () => {
        this.listeners = this.listeners.filter((listener) => listener !== callback);
      };
    }

    private notifyListeners(value: T) {
      this.listeners.forEach((callback) => callback(value));
    }
}

//function that will set a key on a map stored in a StoreValue
export function setMapKey<T>(storeValue: StoreValue<Map<string, T>>, key: string, value: T) {
    const map = storeValue.value;
    map.set(key, value);
    storeValue.value = map;
}