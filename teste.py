import customtkinter

app = customtkinter.CTk()

inputs = []

def add_input(parent, placeholder):
    input = customtkinter.CTkEntry(master=parent, placeholder_text=placeholder)
    input.pack(padx=8, pady=8)
    inputs.append(input)

for i in range(5):
    add_input(app, f"input {i+1}")

def print_inputs():
    for input in inputs:
        print("value:", input.get())

customtkinter.CTkButton(master=app, text="Print", command=print_inputs).pack(pady=8)

app.mainloop()