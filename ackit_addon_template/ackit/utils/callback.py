from collections import defaultdict


class CallbackList:
    def __init__(self):
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def remove_callback(self, callback):
        self.callbacks.remove(callback)

    def clear_callbacks(self):
        self.callbacks.clear()

    def call_callbacks(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)
    
    def __bool__(self):
        return len(self.callbacks) > 0


class CallbackDict:
    def __init__(self):
        self.callbacks = defaultdict(CallbackList)

    def add_callback(self, callback_id, callback):
        self.callbacks[callback_id].add_callback(callback)

    def remove_callback(self, callback_id, callback):
        self.callbacks[callback_id].remove_callback(callback)

    def clear_callbacks(self):
        self.callbacks.clear()

    def call_callbacks(self, callback_id, *args, **kwargs):
        self.callbacks[callback_id].call_callbacks(*args, **kwargs)

    def __bool__(self):
        return any(self.callbacks.values())
