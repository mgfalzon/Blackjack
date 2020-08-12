from os import system, name

class Display:

    def __init__(self):
        self._s = ''
        self._args = []

    def render(self, s=None, *args):
        Display.clear()
        if s is not None:
            self._s = s
            self._args = args
        print(self._s.format(*self._args))

    def multiAppend(*strings):
        output = ''

        # split lines
        strings = list(map(lambda item : item.split('\n'), strings))
        # get length first line
        length = len(strings[0])
        # restrict strings same size
        strings = list(map(lambda item : item[:length], strings))

        for i in range(length):
            line = ''
            for s in strings: line += s[i]
            output += line + '\n'

        return output

    def clear():
        _ = system('cls' if name =='nt' else 'clear')

class Child(Display):
    def __init__(self):
        super().__init__()
