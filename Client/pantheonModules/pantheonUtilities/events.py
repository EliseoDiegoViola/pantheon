class EventHook(object):

    def __init__(self):
        self.__muted = False
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        if self.__muted: return
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for handler in self.__handlers:
            if handler.im_self == inObject:
                self -= handler

    def muteCalls(self,state):
        self.__muted = state