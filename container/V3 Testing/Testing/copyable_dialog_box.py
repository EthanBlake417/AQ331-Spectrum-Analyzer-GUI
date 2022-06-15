import tkinter as tk
import tkinter.simpledialog


class CustomDialog(tkinter.simpledialog.Dialog):

    def __init__(self, parent, title=None, text=None):
        self.data = text
        tkinter.simpledialog.Dialog.__init__(self, parent, title=title)

    def body(self, parent):
        self.text = tk.Text(self, width=40, height=4)
        self.text.pack(fill="both", expand=True)

        self.text.insert("1.0", self.data)

        return self.text


def show_dialog(root, title: str, text: str):
    """ Opens a dialog box where you can copy and paste the values"""
    CustomDialog(root, title=title, text=text)


if __name__ == '__main__':
    root = tk.Tk()
    # button = tk.Button(root, text="Click me", command=show_dialog)
    # button.pack(padx=20, pady=20)
    show_dialog(root, "hello", "what")
    root.mainloop()
