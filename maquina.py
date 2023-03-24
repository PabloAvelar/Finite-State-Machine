class Maquina:
    def __init__(self) -> None:
        inicial = "q0"
        self.s = "q0"

    def f(self, i):
        m = { #0 = maquina
            "q0": "q1",
            "q1": "q2",
            "q2": "q2",
            "q3": "q0"
        }

        u = { #1 = usuario
            "q0": "q2",
            "q1": "q1",
            "q2": "q1",
            "q3": "q0"
        }

        full = {
            "q0": "q0",
            "q1": "q3",
            "q2": "q3",
            "q3": "q3"
        }

        e = {
            "q0": "q0",
            "q1": "q1",
            "q2": "q2",
            "q3": "q0"
        }

        if i == '0':
            if self.s in m:
                self.s = m[self.s]
        
        if i == '1':
            if self.s in u:
                self.s = u[self.s]

        if i == "full":
            if self.s in full:
                self.s = full[self.s]

        if i == 'e':
            if self.s in e:
                self.s = e[self.s]
        print("*****************")
        print("NUEVO ESTADO: {}".format(self.s))

    def g(self, i):
        o = ""
        m = { #0
            "q0": "m",
            "q1": "X",
            "q2": "*",
            "q3": "m"
        }

        u = { #1
            "q0": "u",
            "q1": "*",
            "q2": "O",
            "q3": "u"
        }

        full = {
            "q0": "*",
            "q1": "*",
            "q2": "*",
            "q3": "*"
        }

        e = {
            "q0": "*",
            "q1": "*",
            "q2": "*",
            "q3": "e"
        }

        if i == '0':
            if self.s in m:
                o = m[self.s]
        
        if i == '1':
            if self.s in u:
                o = u[self.s]

        if i == "full":
            if self.s in full:
                o = full[self.s]

        if i == 'e':
            if self.s in e:
                o = e[self.s]
            
        
        
        print("O: ", o)
        return o
