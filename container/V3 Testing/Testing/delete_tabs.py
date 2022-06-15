from tkinter import *
from tkinter import ttk

def deletetab():
    for item in nb.winfo_children():
        if str(item) == (nb.select()):
            item.destroy()
            return  #Necessary to break or for loop can destroy all the tabs when first tab is deleted

root = Tk()

button = ttk.Button(root,text='Delete Tab', command=deletetab)
button.pack()

nb = ttk.Notebook(root)
nb.pack()

f1 = ttk.Frame(nb)
f2 = ttk.Frame(nb)
f3 = ttk.Frame(nb)
f4 = ttk.Frame(nb)
f5 = ttk.Frame(nb)

nb.add(f1, text='FRAME_1')
nb.add(f2, text='FRAME_2')
nb.add(f3, text='FRAME_3')
nb.add(f4, text='FRAME_4')
nb.add(f5, text='FRAME_5')

root.mainloop()