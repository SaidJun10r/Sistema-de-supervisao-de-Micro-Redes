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

import tkinter
window=tkinter.Tk()
window.geometry("700x400")

def vervalor():
    print(selection)


selection=0
option_Menu = tkinter.StringVar(window)
options = ("a","b","c")
menu = tkinter.OptionMenu(window,option_Menu,*options, command=vervalor())
menu.grid(row=2,column=2)
option_Menu.set(2)
selection=option_Menu.get()

tkinter.mainloop()