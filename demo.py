lst = [1, 2, 3, 4,5,6,7]
class person:
    def __init__(self,name):
        self.name=name
        self.hobbies=[]

    def change(self,h):
        self.hobbies=h

    def add_h(self,h):
        self.hobbies.append(h)




noha =person('noha')
noha.add_h(1)
noha.add_h(2)
noha.add_h(3)
noha.add_h(5)
noha.add_h(6)
noha.add_h(7)
noha.add_h(8)
def change_lst(noha):
    lo = [10, 12, 13, 14, 15, 16, 17]
    noha.change(lo)


for i, l in enumerate(noha.hobbies):
    if i == 2:
        l = 200
        print(i, l)
    else:
        print(i, l)


