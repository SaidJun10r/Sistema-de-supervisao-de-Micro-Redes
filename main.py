import customtkinter 

customtkinter.set_appearance_mode('dark') # Aparencia da janela
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('500x350')

def login():
    print('Test')

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill='both', expand=True)

label = customtkinter.CTkLabel(master=frame, text='Sistema de Login')
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text='Usuario')
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text='Senha', show='*')
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text='Login', command=login)
button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text='Lembarar de mim')
checkbox.pack(pady=12, padx=10)

root.mainloop()