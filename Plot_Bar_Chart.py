import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk


def Plot_Bar_Chart(x,y):
    # Create a background window
    root = Tk.Tk()

    # Create a title for background window
    root.title("Nokia_6610")

    # Figsize = figure size in in inches (width, height) , dpi = resolution in dots per inch
    f = Figure(figsize=(8,5), dpi=80)

    # Subplot = number of rows and columns and the number of the plot
    ax = f.add_subplot(111)

    y_location = y

    x_location = x

    # The width of each Bar
    width = .5

    # Draw bar
    ax.bar(x_location, y_location, width)

    # A tk.DrawingArea
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    # Invoke the main event handling loop
    Tk.mainloop()
