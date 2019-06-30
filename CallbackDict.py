from inspect import iscoroutine

class CallbackDict(dict):
    """
    A simple dict extension that uses a (possibly async) callback to fetch missing items
    Note that .get is used because you cannot have an async __getitem__ (and hence __missing__)
    """
    def __init__(self, callback):
        super(CallbackDict, self).__init__()
        self._cbk = callback
        self.get = self._get_async if iscoroutine(callback) else self._get

    def get(self, k):
        """Get an item from the dictionary. Uses predefined callback if the key is not found"""
        pass

    async def _get_async(self, k):
        v = super().get(k)
        if not v:
            v = await self._cbk(k)
            self[k] = v
        return v

    def _get(self, k):
        v = super().get(k)
        if not v:
            v = self._cbk(k)
            self[k] = v
        return v
