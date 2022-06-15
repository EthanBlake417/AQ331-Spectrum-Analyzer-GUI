from tkinter import *
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from tkinter import filedialog
from container.UI.Operations.scrollable_text_box_class import ScrollableTextBox


class TkinterPlot:
    """
    For this scrollable text box to give the information outside this function:
    Please define these globals: global text_area, temps_list, times_list
    Additionally: call parse_text_data before using any of the data to make sure you have the current data.
    For example, before displaying a graph, call parse_text_data. before running a program, call parse_text_data
    """

    def __init__(self, root, scrollable_text_box):
        """
        Sets up the scrollable text box class inside of a frame.
        :param root: From outside program
        """
        self.scrollable_text_box = scrollable_text_box
        self.root = root
        frame = Frame(root, width=400, height=400, bd=1)
        frame.place(x=10, y=10)
        Button(frame, text="Plot Data", command=self.plot_data).place(x=150, y=340)

    def plot_data(self):
        try:
            x_axis, y_axis = [], []
            list_of_temps, list_of_times = self.scrollable_text_box.get_data()
            x_axis.append(list_of_times[0])
            for i in range(1, len(list_of_times)):
                x_axis.append(list_of_times[i] + x_axis[i - 1])
            y_axis = list_of_temps
            # the figure that will contain the plot
            fig = Figure(figsize=(4, 3),
                         dpi=100)
            # list of squares
            x = x_axis
            y = y_axis

            # adding the subplot
            plot1 = fig.add_subplot(111)

            # plotting the graph
            plot1.plot(x, y)

            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()

            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().grid(row=0, column=0, columnspan=1)

            # creating the Matplotlib toolbar
            toolbar = NavigationToolbar2Tk(canvas, self.root, pack_toolbar=False)
            toolbar.grid(row=1, column=0, columnspan=1)
            toolbar.update()
            canvas._tkcanvas.grid()
            # side=tk.TOP, fill=tk.BOTH, expand=True
            # placing the toolbar on the Tkinter window
            canvas.get_tk_widget().grid()
        except IndexError:
            print("No Data to Graph!")


if __name__ == '__main__':
    pass
