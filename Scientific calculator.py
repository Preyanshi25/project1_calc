import tkinter as tk

import math
 
# Dark contrast color palette

BG_COLOR = "#2E2E2E"

DISPLAY_BG = "#424242"

BUTTON_BG = "#616161"

SPECIAL_BUTTON_BG = "#FF5722"

EQUALS_BUTTON_BG = "#4CAF50"

TEXT_COLOR = "#FFFFFF"

RESULT_COLOR = "#FFEB3B"
 
LARGE_FONT_STYLE = ("Segoe UI", 38, "bold")

DEFAULT_FONT_STYLE = ("Segoe UI", 20)
 
 
class Calculator:

    def __init__(self):

        self.window = tk.Tk()

        self.window.title("Scientific Calculator")

        self.window.geometry("400x700")

        self.window.resizable(False, False)

        self.window.config(bg=BG_COLOR)
 
        self.total_expression = ""

        self.current_expression = ""

        self.memory = 0
 
        self.display_frame = self.create_display_frame()

        self.buttons_frame = self.create_buttons_frame()

        self.total_label, self.label = self.create_display_labels()
 
        self.create_all_buttons()

        self.bind_keys()
 
        for i in range(10):

            self.buttons_frame.rowconfigure(i, weight=1)

        for j in range(4):

            self.buttons_frame.columnconfigure(j, weight=1)
 
        self.update_label()

        self.update_total_label()
 
    def create_display_frame(self):

        frame = tk.Frame(self.window, height=200, bg=DISPLAY_BG)

        frame.pack(expand=True, fill="both")

        return frame
 
    def create_display_labels(self):

        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E,

                               bg=DISPLAY_BG, fg=TEXT_COLOR, padx=24, font=DEFAULT_FONT_STYLE)

        total_label.pack(expand=True, fill="both")
 
        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E,

                         bg=DISPLAY_BG, fg=RESULT_COLOR, padx=24, font=LARGE_FONT_STYLE)

        label.pack(expand=True, fill="both")

        return total_label, label
 
    def create_buttons_frame(self):

        frame = tk.Frame(self.window, bg=BG_COLOR)

        frame.pack(expand=True, fill="both")

        return frame
 
    def create_all_buttons(self):

        buttons = [

            ('C', '', 'DEL', '%'),

            ('7', '8', '9', '/'),

            ('4', '5', '6', '*'),

            ('1', '2', '3', '-'),

            ('0', '.', '(', ')'),

            ('pi', 'e', 'sqrt', 'log'),

            ('exp', 'fact', 'sin', 'cos'),

            ('tan', '!', 'MC', 'MR'),

            ('M+', 'M-', '=', '')

        ]
 
        for i, row in enumerate(buttons):

            for j, btn in enumerate(row):

                if not btn:

                    continue

                colspan = 2 if (btn == '=' and j == 2) or (btn == 'C' and j == 0) else 1

                self.create_button(btn, i, j, colspan)
 
    def create_button(self, label, row, column, colspan=1):

        def action():

            if label == 'C':

                self.clear()

            elif label == 'DEL':

                self.delete()

            elif label == '=':

                self.evaluate()

            elif label == 'MC':

                self.memory = 0

            elif label == 'MR':

                self.memory_recall()

            elif label == 'M+':

                self.memory_add()

            elif label == 'M-':

                self.memory_subtract()

            elif label == 'pi':

                self.add_to_expression(str(math.pi))

            elif label == 'e':

                self.add_to_expression(str(math.e))

            elif label == 'sqrt':

                self.add_to_expression('math.sqrt(')

            elif label == 'log':

                self.add_to_expression('math.log(')

            elif label == 'exp':

                self.add_to_expression('math.exp(')

            elif label == 'fact':

                self.add_to_expression('math.factorial(')

            elif label == 'sin':

                self.add_to_expression('math.sin(')

            elif label == 'cos':

                self.add_to_expression('math.cos(')

            elif label == 'tan':

                self.add_to_expression('math.tan(')

            elif label == '!':

                self.current_expression += '!'

                self.update_label()

            elif label == '%':

                self.current_expression += '/100'

                self.update_label()

            else:

                self.add_to_expression(label)
 
        bg = EQUALS_BUTTON_BG if label == '=' else SPECIAL_BUTTON_BG if label in ['C', 'DEL', '%'] else BUTTON_BG

        fg = TEXT_COLOR
 
        tk.Button(self.buttons_frame, text=label, bg=bg, fg=fg,

                  font=DEFAULT_FONT_STYLE, borderwidth=0, command=action

                  ).grid(row=row, column=column, columnspan=colspan, sticky=tk.NSEW, padx=2, pady=2)
 
    def add_to_expression(self, value):

        self.current_expression += str(value)

        self.update_label()
 
    def clear(self):

        self.current_expression = ""

        self.total_expression = ""

        self.update_label()

        self.update_total_label()
 
    def delete(self):

        self.current_expression = self.current_expression[:-1]

        self.update_label()
 
    def memory_recall(self):

        self.current_expression = str(self.memory)

        self.update_label()
 
    def memory_add(self):

        try:

            self.memory += float(eval(self.current_expression))

        except:

            self.current_expression = "Error"

        self.update_label()
 
    def memory_subtract(self):

        try:

            self.memory -= float(eval(self.current_expression))

        except:

            self.current_expression = "Error"

        self.update_label()
 
    def evaluate(self):

        expression = self.current_expression.replace('÷', '/').replace('×', '*').replace('−', '-')
 
        try:

            while '!' in expression:

                index = expression.index('!')

                i = index - 1

                while i >= 0 and (expression[i].isdigit() or expression[i] == '.'):

                    i -= 1

                num = expression[i+1:index]

                fact = str(math.factorial(int(num)))

                expression = expression[:i+1] + fact + expression[index+1:]
 
            result = str(eval(expression))

            self.current_expression = result

            self.total_expression = ""

        except:

            self.current_expression = "Error"

        self.update_label()

        self.update_total_label()
 
    def bind_keys(self):

        self.window.bind("<Return>", lambda event: self.evaluate())

        self.window.bind("<BackSpace>", lambda event: self.delete())

        self.window.bind("<Escape>", lambda event: self.clear())

        self.window.bind("<Key>", self.handle_key_press)
 
    def handle_key_press(self, event):

        key = event.char.lower()  # Convert to lowercase for easier matching
 
        if key.isdigit():

            self.add_to_expression(key)

        elif key in ['+', '-', '*', '/', '%']:

            self.add_to_expression(key)

        elif key in ['.', '(', ')']:

            self.add_to_expression(key)

        elif key == 'p':  # pi

            self.add_to_expression(str(math.pi))

        elif key == 'e':  # e constant

            self.add_to_expression(str(math.e))

        elif key == 'r':  # sqrt

            self.add_to_expression('math.sqrt(')

        elif key == 'l':  # log

            self.add_to_expression('math.log(')

        elif key == 'x':  # exp

            self.add_to_expression('math.exp(')

        elif key == 'f':  # factorial

            self.add_to_expression('math.factorial(')

        elif key == 's':  # sin

            self.add_to_expression('math.sin(')

        elif key == 't':  # tan

            self.add_to_expression('math.tan(')

        elif key == 'c':  # clear

            self.clear()

        elif key == '!':

            self.add_to_expression('!')

        elif key == '=':

            self.evaluate()
 
    def update_total_label(self):

        self.total_label.config(text=self.total_expression)
 
    def update_label(self):

        self.label.config(text=self.current_expression[:15])
 
    def run(self):

        self.window.mainloop()
 
 
if __name__ == "__main__":

    calc = Calculator()

    calc.run()