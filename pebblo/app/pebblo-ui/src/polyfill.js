Array.prototype.myMap = function (callbackFn) {
  var arr = [];
  for (var i = 0; i < this.length; i++) {
    arr.push(callbackFn(this[i], i, this));
  }
  return arr.join("");
};

(function () {
  var originalAddEventListener = EventTarget.prototype.addEventListener;

  EventTarget.prototype.addEventListener = function (type, listener, options) {
    this._eventListeners = this._eventListeners || {};
    this._eventListeners[type] = this._eventListeners[type] || [];
    this._eventListeners[type].push(listener);
    originalAddEventListener.call(this, type, listener, options);
  };

  // Function to check if an event listener is added
  EventTarget.prototype.hasEventListener = function (type, listener) {
    if (!this._eventListeners || !this._eventListeners[type]) {
      return false;
    }
    return this._eventListeners[type].includes(listener);
  };
})();
