# # Botão
# button = customtkinter.CTkButton(master=app, text="Estudo de Caso 2", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

# # Titulo
# label = customtkinter.CTkLabel(master=app,
#                                text="CTkLabel",
#                                width=120,
#                                height=25,
#                                corner_radius=8)
# label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# # Inserção de texto
# entry = customtkinter.CTkEntry(master=app,
#                                width=120,
#                                height=25,
#                                corner_radius=10)
# entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# text = entry.get()

# # Barra de progresso
# progressbar = customtkinter.CTkProgressBar(master=app,
#                                            width=160,
#                                            height=20,
#                                            border_width=5)
# progressbar.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# progressbar.set(0.05)

# # Frame
# frame = customtkinter.CTkFrame(master=app,
#                                width=200,
#                                height=200,
#                                corner_radius=10)
# frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# # Menu de opções
# optionmenu_1 = customtkinter.CTkOptionMenu(app, dynamic_resizing=False, values=["Value 1", "Value 2", "Value Long Long Long"])
# optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))

import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter

class CSVPlotter:


    def __init__(self, root):
        self.root = root
        root.title("CSV Plotter")

        self.plot_types = ['Line Plot', 'Bar Plot', 'Scatter Plot']
        self.plot_type_var = tk.StringVar(value=self.plot_types[0])
        plot_menu = tk.OptionMenu(self.root, self.plot_type_var, *self.plot_types, command=self.update_plot)
        plot_menu.pack(padx=10, pady=10)

        load_button = tk.Button(self.root, text='Load CSV', command=self.load_csv)
        load_button.pack(padx=10, pady=10)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.widget = self.canvas.get_tk_widget()
        self.widget.pack(padx=10, pady=10)

        self.df = None

    def load_csv(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.df = pd.read_csv(file_path)
            self.update_plot()

    def update_plot(self, event=None):
        if self.df is not None:
            plot_type = self.plot_type_var.get()
            x = self.df.columns[0]
            y = self.df.columns[1]

            self.ax.clear()
            if plot_type == 'Line Plot':
                self.ax.plot(self.df[x], self.df[y], label=f'{y} vs {x}')
            elif plot_type == 'Line Plot':
                self.ax.bar(self.df[x], self.df[y], label=f'{y} vs {x}')
            elif plot_type == 'Line Plot':
                self.ax.scatter(self.df[x], self.df[y], label=f'{y} vs {x}')

            self.ax.set_xlabel(x)
            self.ax.set_ylabel(y)
            self.ax.legend()
            self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = CSVPlotter(root)
    root.mainloop()