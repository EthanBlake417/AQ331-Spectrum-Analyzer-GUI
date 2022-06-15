from tkinter import *
from tkinter import filedialog as fd
import pandas as pd


class ScrollableTextBox:
    """
    For this scrollable text box to give the information outside this function:
    Please define these globals: global text_area, temps_list, times_list
    Additionally: call parse_text_data before using any of the data to make sure you have the current data.
    For example, before displaying a graph, call parse_text_data. before running a program, call parse_text_data
    """

    def __init__(self, root):
        """
        Sets up the scrollable text box class inside of a frame.
        :param root: From outside program
        """
        self.temps_list = []
        self.times_list = []
        frame_1 = Frame(root, width=400, height=400, bd=1)
        frame_1.place(x=10, y=10)
        frame_2 = Frame(frame_1, width=400, height=400, bd=1)
        frame_2.place(x=0, y=30)
        Button(frame_1, text="Get Data", command=self.get_data_from_csv).place(x=25, y=0)
        Button(frame_1, text="Write Data", command=self.write_data_to_csv).place(x=150, y=0)

        v = Scrollbar(frame_2)
        v.pack(side=RIGHT, fill=Y)

        self.text_area = Text(frame_2, width=46, height=20, wrap=NONE, yscrollcommand=v.set)
        self.text_area.pack(side=TOP, fill=X)
        v.config(command=self.text_area.yview)

        self.put_data([24], [0])

    def parse_text_data(self):
        """
        Parses the data in the text, putting only the numerical values into the Temperatures and Times
        """
        self.temps_list = []
        self.times_list = []
        result = self.text_area.get(1.0, END)
        string = ""
        for char in result:
            if char == ',':
                self.temps_list.append(string)
                string = ""
            elif char == '\n':
                self.times_list.append(string)
                string = ""
            else:
                string = string + char
        self.times_list = self.times_list[1:len(self.temps_list)]   # this is to account for if there are extra new line characters at the end
        self.temps_list = self.temps_list[1:]                       # we slice from line one to remove the labels.

    def get_data_from_csv(self):
        """ Gets the data from the CSV and displays it on the screen """
        filename = fd.askopenfilename(title='Open a file', filetypes=(("csv files", "*.csv"), ("All Files", "*.*")))
        if filename:
            temps = pd.read_csv(filename)['Temperature'].tolist()
            times = pd.read_csv(filename)['Time'].tolist()
            self.temps_list = ["Temperature"]
            self.times_list = ["Time"]
            self.text_area.delete(1.0, END)
            self.text_area.update_idletasks()
            self.text_area.insert(INSERT, f'{self.temps_list[0]},{self.times_list[0]}\n')
            for i in range(len(temps)):
                self.temps_list.append(temps[i])
                self.times_list.append(times[i])
                self.text_area.insert(INSERT, f'{temps[i]},{times[i]}\n')

    def write_data_to_csv(self):
        """ Writes the data to a csv file of your choosing """
        filename = fd.asksaveasfilename(title='Save', filetypes=(("csv files", "*.csv"), ("All Files", "*.*")))
        if filename:
            # it is important to parse the data first before doing anything else.
            self.parse_text_data()
            df = pd.DataFrame()
            df['Temperature'] = self.temps_list
            df['Time'] = self.times_list
            df.to_csv(filename, index=False)

    def get_data(self):
        """ Returns a list of temperatures and a list of Times"""
        self.parse_text_data()
        for i in range(len(self.temps_list)):
            self.temps_list[i] = float(self.temps_list[i])
            self.times_list[i] = float(self.times_list[i])
        return self.temps_list, self.times_list

    def delete_data(self):
        """ Deletes text box data"""
        self.text_area.delete(1.0, END)
        self.text_area.update_idletasks()

    def put_data(self, temps, times):
        """
        args: temps, times
        action: puts in scrollable text box data
        """
        self.temps_list = ["Temperature"]
        self.times_list = ["Time"]
        self.text_area.delete(1.0, END)
        self.text_area.update_idletasks()
        self.text_area.insert(INSERT, f'{self.temps_list[0]},{self.times_list[0]}\n')
        for i in range(len(temps)):
            self.temps_list.append(temps[i])
            self.times_list.append(times[i])
            self.text_area.insert(INSERT, f'{temps[i]},{times[i]}\n')


if __name__ == '__main__':
    """ this is some sample usage"""
    root = Tk()
    root.geometry("800x600")
    root.title("ScrolledText Widget")
    scrollable_text_box = ScrollableTextBox(root)


    def get():
        temps_list, times_list = scrollable_text_box.get_data()
        print(temps_list, times_list)


    Button(root, text="Update Data", command=get).pack()

    root.mainloop()
