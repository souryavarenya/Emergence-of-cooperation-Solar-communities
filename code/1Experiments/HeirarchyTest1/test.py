class boxy(object):
    def __init__(self,initstr):
        print(initstr)
        self.value = False

    def toggle_value(self):
        self.value = not self.value

class casy(object):
    def __init__(self, boxy_obj):
        print("casy")
        self.bxyobj = boxy_obj

    def printy(self):
        print(self.bxyobj.value)

bx1 = boxy("Sou")
cs1 = casy(bx1)
cs1.printy()
bx1.toggle_value()
cs1.printy()

