from tkinter import *

class Input:
    @staticmethod
    def label(root, row=0, column=0, pady=5, padx=0, columnspan=1, text="Put Text Here", font=("Courier", 10)):
        label = Label(root, text=text)
        label.config(font=font)
        label.grid(row=row, column=column, pady=pady, padx=padx, columnspan=columnspan)
        return label

    @staticmethod
    def entry(root, row=0, column=0, pady=5, padx=0, columnspan=1, command=None, width=10, insert="Insert Value Here"):
        entry = Entry(root, width=width)
        entry.grid(row=row, column=column, pady=pady, padx=padx, columnspan=columnspan, command=command)
        entry.insert(0, insert)
        return entry


if __name__ == '__main__':
    pass