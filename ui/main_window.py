from tkinter import *

class Checkbar(Frame):
     def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)
        def state(self):
            return map((lambda var: var.get()), self.vars)

if __name__ == '__main__':
    root = Tk()
    root.title('*Name*')
    #root.geometry('450x300')
   
    label_del = Label(root, text='Выберите фирму доставки').pack(side=TOP, fill=X)

    delivery = Checkbar(root, ['Boxberry', 'CDEK'])
    delivery.pack(side=TOP,  fill=X)
    delivery.config(relief=GROOVE, bd=2)

    label_city = Label(root, text='Выберите зону доставки').pack(side=TOP, fill=X)

    city_zone = Checkbar(root, ['1', '2', '3', 'Один город'])
    city_zone.pack(side=TOP,  fill=X)
    city_zone.config(relief=GROOVE, bd=2)


    def allstates(): 
        print(list(delivery.state()))
        print(list(city_zone.state()))

    Button(root, text='Выйти', command=root.quit).pack(side=RIGHT)
    Button(root, text='Загрузить', command=allstates).pack(side=RIGHT)

    root.resizable(width=False, height=False)
    root.mainloop()