class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def is_balanced(in_str):
    if len(in_str) == 0:
        return
    s = Stack()
    op_brackets = ['(', '[', '{']
    cl_brackets = [')', ']', '}']
    for i in in_str:
        if i in op_brackets:
            s.push(i)
        elif i in cl_brackets:
            if s.is_empty():
                return False
            if cl_brackets.index(i) != op_brackets.index(s.pop()):
                return False
    return s.is_empty()


if __name__ == "__main__":
    print('Введите строку из скобок:')
    string = input()
    if is_balanced(string) is True:
        print('Строка скобок сбалансирована')
    elif is_balanced(string) is None:
        print('Строка скобок пуста')
    else:
        print('Строка скобок не сбалансирована')
