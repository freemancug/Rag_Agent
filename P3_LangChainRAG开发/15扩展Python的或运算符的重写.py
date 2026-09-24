

class Test(object):
    def __init__(self, name):
        self.name = name
    def __or__(self, other):
        return MySquence(self, other)
    def __str__(self):
        return self.name

class MySquence(object):
    def __init__(self,*args):
        self.squence = []
        for arg in args:
            self.squence.append(arg)
        
    def __or__(self, other):
        self.squence.append(other)
        return self

    def run(self):
        for item in self.squence:
            print(item)

if __name__ == "__main__":
    a = Test("a")
    b = Test("b")
    c = Test("c")
    e = Test("e")
    f = Test("f")
    g = Test("g")
    d = a | b | c | e | f | g
    d.run()
    print(type(d))
