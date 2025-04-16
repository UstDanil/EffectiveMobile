class ObjList:
    def __init__(self, data):
        self.__prev = None
        self.__data = data
        self.__next = None

    def set_next(self, obj):
        self.__next = obj

    def set_prev(self, obj):
        self.__prev = obj

    def get_next(self):
        return self.__next

    def get_prev(self):
        return self.__prev

    def set_data(self, data):
        self.__data = obj

    def get_data(self):
        return self.__data


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_obj(self, new_obj):
        if not self.head:
            self.head = new_obj
            self.tail = new_obj
            return

        last_obj = self.tail
        last_obj.set_next(new_obj)
        new_obj.set_prev(last_obj)
        self.tail = new_obj

    def get_data(self):
        obj = self.head
        result = list()
        while obj is not None:
            result.append(obj.get_data())
            obj = obj.get_next()
        return result

    def remove_obj(self):
        last_obj = self.tail
        if not last_obj:
            return

        penultimate_obj = last_obj.get_prev()
        if not penultimate_obj:
            self.head = None
            self.tail = None
            return

        self.tail = penultimate_obj
        last_obj.set_prev(None)
        penultimate_obj.set_next(None)


# if __name__ == '__main__':
#     lst = LinkedList()
#     lst.add_obj(ObjList('data1'))
#     lst.add_obj(ObjList('data2'))
#     lst.add_obj(ObjList('data3'))
#     lst.add_obj(ObjList('data4'))
#     lst.remove_obj()
#     res = lst.get_data()
#     print(res)
