from tkinter import *
from tkinter import ttk


class Dropdown:
    def __init__(self, frame, options, row=0, column=0, sticky=W, columnspan=2):
        self.frame = frame
        self.options = options

        self.myCombo = ttk.Combobox(self.frame, value=self.options, width=38)
        self.myCombo.set(self.get_port(0))
        self.myCombo.bind("<<ComboboxSelected>>", self.combo_click)
        self.myCombo.grid(row=row, column=column, sticky=sticky, columnspan=columnspan)

    def get_port(self, num):
        if len(self.options) == 0:
            return self.options
        else:
            return self.options[num].split(" ")[0]

    def combo_click(self, event):
        self.myCombo.set(self.myCombo.get().split(" ")[0])

    def reset_values(self, new_values):
        self.myCombo['values'] = new_values

    def set_value(self, new_value):
        self.myCombo.set(new_value)


if __name__ == '__main__':
    root = Tk()
    root.geometry("400x400")
    options = ["Monday asdlkfj", "Friday asdfadf", "Saturday asdfadf"]
    Dropdown(root, options, row=0, column=0)
    Dropdown(root, options, row=1, column=0)
    root.mainloop()
