from tkinter import *
from datetime import datetime
from tkinter import colorchooser


class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Kalkulator")
        self.current_bg = 'white'

        self.display = Entry(master, width=25, font=('Arial', 16), justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.buttons = [
            {'text': '7', 'row': 1, 'column': 0},
            {'text': '8', 'row': 1, 'column': 1},
            {'text': '9', 'row': 1, 'column': 2},
            {'text': '+', 'row': 1, 'column': 3},
            {'text': '4', 'row': 2, 'column': 0},
            {'text': '5', 'row': 2, 'column': 1},
            {'text': '6', 'row': 2, 'column': 2},
            {'text': '-', 'row': 2, 'column': 3},
            {'text': '1', 'row': 3, 'column': 0},
            {'text': '2', 'row': 3, 'column': 1},
            {'text': '3', 'row': 3, 'column': 2},
            {'text': '*', 'row': 3, 'column': 3},
            {'text': '0', 'row': 4, 'column': 0},
            {'text': '.', 'row': 4, 'column': 1},
            {'text': '/', 'row': 4, 'column': 3},
            {'text': 'C', 'row': 4, 'column': 2},
            {'text': '=', 'row': 5, 'column': 3},
            {'text': 'Zmień kolor', 'row': 5, 'column': 0, 'columnspan': 2}
        ]

        for button in self.buttons:
            if 'columnspan' in button:
                btn = Button(master, text=button['text'], width=10, height=2, font=('Arial', 16),
                             command=self.change_bg)
            else:
                btn = Button(master, text=button['text'], width=5, height=2, font=('Arial', 16),
                             command=lambda text=button['text']: self.button_click(text))
            btn.grid(row=button['row'], column=button['column'], padx=5, pady=5, columnspan=button.get('columnspan', 1))

        self.clock = Label(master, text=datetime.now().strftime('%H:%M:%S'), font=('Arial', 20))
        self.clock.grid(row=6, column=0, columnspan=4, pady=10)
        self.master.bind('<Key>', self.key_press)
        self.update_clock()

    def change_bg(self):
        color = colorchooser.askcolor()[1]
        self.master.config(bg=color)

    def button_click(self, text):
        if text == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, END)
                self.display.insert(0, str(result))
            except:
                self.display.delete(0, END)
                self.display.insert(0, 'Błąd')
        elif text == 'C':
            self.display.delete(0, END)
        else:
            self.display.insert(END, text)

    def update_clock(self):
        self.clock.config(text=datetime.now().strftime('%H:%M:%S'))
        self.master.after(1000, self.update_clock)

    def key_press(self, event):
        key = event.char
        if key == '\r':
            try:
                result = eval(self.display.get())
                self.display.delete(0, END)
                self.display.insert(0, str(result))
            except:
                self.display.delete(0, END)
                self.display.insert(0, 'Błąd')
        elif key == '\x08':  # Backspace key
            self.display.delete(len(self.display.get()) - 1, END)
        elif key.isdigit() or key in ['+', '-', '*', '/', '.', '(', ')']:
            self.display.insert(END, key)


root = Tk()
calculator = Calculator(root)
root.mainloop()
