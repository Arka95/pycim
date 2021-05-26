# Node of a doubly linked list
# Note: this is not thread safe
class Node:
    def __init__(self, data=None, next=None, prev=None):
        self.next = next
        self.prev = prev
        self.data = data


class Deque:
    # TODO: add capacity
    def __init__(self, list=None):
        self.__len = 0
        self.__front = self.__back = None
        if list:
            self.append_from_list(list)

    def front(self):
        # earliest node.data is returned
        return self.__front.data if self.__front else None

    def back(self):
        # latest node.data is returned
        return self.__back.data if self.__back else None

    def size(self):
        return self.__len

    def append(self, data):
        node = Node(data)

        if self.__front == None and self.__back == None:
            self.__front = node
            self.__back = self.__front
        else:
            self.__back.next = node
            node.prev = self.__back
            self.__back = node
        self.__len = self.__len+1
        return node

    def remove(self, node):
        """
        node: pointer to the node you want to delete (*Node)
        """
        if node.prev == None:
        # address of node is front of list
            self.__front = node.next
            node.next.prev = None

        if node.next == None:
        # address of node is back of list
            if node.prev == None:
                self.__back = self.__front
            else:
                self.__back = node.prev

        # any other case
        node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        node = None
        self.__len = self.__len -1 if self.__len >0 else 0
        return self.__back

    def pop(self):
        if self.__back==None: # no node
            return None

        data = self.__back.data

        if not(self.__front ==  self.__back): #not single node
            ptr = self.__back
            self.__back = self.__back.prev
            self.__back.next = ptr = None

        else: #single node
            self.__back = self.__front =None

        self.__len = self.__len -1 if self.__len >0 else 0
        return data

    def move_to_back(self, node):
        data = node.data
        self.remove(node)
        return self.append(data)

    def to_list(self):
        s = []
        ptr = self.__front
        while (ptr != None):
            s.append(ptr.data)
            ptr = ptr.next
        return s

    def append_from_list(self, listing):
        for c in listing:
            self.append(c)

    def __str__(self):
        return str(self.to_list())
