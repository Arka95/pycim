"""
This was created due to current limitations of python collections.deque suffering
a node removal time complexity of O(N). moreover unnecessary functions are removed as well
Note: this is not thread safe. Also it does not throw excpetions for empty queue"""

class Node:
    def __init__(self, data=None, next=None, prev=None):
        self.next = next
        self.prev = prev
        self.data = data


class Deque:
    # TODO: make this is a cyclic deque
    def __init__(self, list=None, capacity=None):
        self.__len = 0
        self.__capacity = capacity
        self.__front = self.__back = None
        if list:
            self.append_from_list(list)

    def front(self):
        # earliest node.data is returned in O(1)
        return self.__front.data if self.__front else None

    def back(self):
        # latest node.data is returned in O(1)
        return self.__back.data if self.__back else None

    def size(self):  # O(1)
        return self.__len

    def append(self, data):  # O(1)
        node = Node(data)

        if self.is_full():  # ensures old item popped before new item is inserted
            self.pop_left()

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
        node: pointer to the node you want to delete (*Node) in O(1)
        """
        if not node:
            return

        elif node.next==None and node.prev==None: # it was the only one node of the queue
            self.__back = self.__front = None

        elif node.prev == None:  # address of node is front of list
            self.__front = node.next
            node.next.prev = None

        elif node.next == None:  # address of node is back of list
            self.__back = node.prev
            node.prev.next = None

        else:  # any other case
            node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev

        node = None
        self.__len = self.__len -1 if self.__len >0 else 0
        return self.__back

    def pop_left(self):  # O(1)
        node = self.__front
        data = node.data if node else None
        self.remove(node)
        return data

    def pop(self):  # O(1)
        node = self.__back
        data = node.data if node else None
        self.remove(node)
        return data

    def move_to_back(self, node):  # O(1)
        data = node.data
        self.remove(node)
        return self.append(data)

    def to_list(self):  # O(n)
        s = []
        ptr = self.__front
        while (ptr != None):
            s.append(ptr.data)
            ptr = ptr.next
        return s

    def append_from_list(self, listing):  # O(n)
        for c in listing:
            self.append(c)

    def __str__(self):  # O(n)
        return str(self.to_list())

    def is_empty(self):
        return self.__front == self.__back == None

    def is_full(self):
        return self.size() ==self.__capacity
