"""Simple number calculator using Python and Tkinter."""

import random
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


def divides(a, b):
    if a == 0:
        return b == 0
    return b % a == 0


def gcd(a, b):
    if a < 0:
        a = -a
    if b < 0:
        b = -b
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    r0 = -a if a < 0 else a
    r1 = -b if b < 0 else b
    x0, x1 = 1, 0
    y0, y1 = 0, 1

    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    if a < 0:
        x0 = -x0
    if b < 0:
        y0 = -y0
    return r0, x0, y0


class Calculator:
    def __init__(self, root):
        root.title('Number Calculator')
        root.geometry('740x620')
        root.minsize(680, 560)

        frame = ttk.Frame(root, padding=18)
        frame.pack(fill='both', expand=True)
        ttk.Label(frame, text='Number Calculator', font=('Arial', 18, 'bold')).pack(anchor='w')
        ttk.Label(frame, text='Divisibility, GCD and Extended Euclidean Algorithm').pack(anchor='w', pady=(4, 14))

        ttk.Label(frame, text='First number (a):').pack(anchor='w')
        self.number_a = ScrolledText(frame, height=3, wrap='char', font=('Courier', 11))
        self.number_a.pack(fill='x', pady=(4, 10))

        ttk.Label(frame, text='Second number (b):').pack(anchor='w')
        self.number_b = ScrolledText(frame, height=3, wrap='char', font=('Courier', 11))
        self.number_b.pack(fill='x', pady=(4, 10))

        options = ttk.Frame(frame)
        options.pack(fill='x', pady=(0, 12))
        ttk.Button(options, text='Generate 512-bit numbers', command=self.generate).pack(side='left')
        ttk.Button(options, text='Clear', command=self.clear).pack(side='left', padx=8)
        ttk.Label(options, text='Small numbers are also accepted.').pack(side='left')

        buttons = ttk.Frame(frame)
        buttons.pack(fill='x', pady=(0, 14))
        ttk.Button(buttons, text='Divisibility', command=lambda: self.calculate('divisibility')).pack(side='left')
        ttk.Button(buttons, text='GCD', command=lambda: self.calculate('gcd')).pack(side='left', padx=8)
        ttk.Button(buttons, text='Extended Euclid', command=lambda: self.calculate('extended')).pack(side='left')

        ttk.Label(frame, text='Result:').pack(anchor='w')
        self.result = ScrolledText(frame, height=8, wrap='char', font=('Courier', 11), state='disabled')
        self.result.pack(fill='both', expand=True, pady=(4, 0))
        self.show('Enter two numbers and choose an operation.')

    def show(self, text):
        self.result.configure(state='normal')
        self.result.delete('1.0', 'end')
        self.result.insert('1.0', text)
        self.result.configure(state='disabled')

    def read_numbers(self):
        values = []
        for field in (self.number_a, self.number_b):
            text = ''.join(field.get('1.0', 'end').split())
            digits = text[1:] if text.startswith(('+', '-')) else text
            if len(text) > 1250 or not digits.isascii() or not digits.isdigit():
                raise ValueError('Please enter valid whole numbers in both boxes.')
            value = int(text)
            magnitude = -value if value < 0 else value
            if magnitude >= (1 << 4096):
                raise ValueError('Please use numbers with at most 4096 bits.')
            values.append(value)
        return values

    def generate(self):
        for field in (self.number_a, self.number_b):
            value = random.getrandbits(511) | (1 << 511)
            field.delete('1.0', 'end')
            field.insert('1.0', str(value))
        self.show('Two 512-bit numbers generated. Choose an operation.')

    def clear(self):
        self.number_a.delete('1.0', 'end')
        self.number_b.delete('1.0', 'end')
        self.show('')
        self.number_a.focus_set()

    def calculate(self, operation):
        try:
            a, b = self.read_numbers()
        except ValueError as error:
            self.show(str(error))
            return

        if operation == 'divisibility':
            text = 'a divides b: ' + ('Yes' if divides(a, b) else 'No')
            text += '\nb divides a: ' + ('Yes' if divides(b, a) else 'No')
            if a != 0:
                positive_a = -a if a < 0 else a
                text += '\n\nb remainder |a| = ' + str(b % positive_a)
            if b != 0:
                positive_b = -b if b < 0 else b
                text += '\na remainder |b| = ' + str(a % positive_b)
            if a == 0 or b == 0:
                text += '\n\nZero divides only zero. Division by zero is undefined.'
        elif operation == 'gcd':
            answer = gcd(a, b)
            text = 'GCD = ' + str(answer)
        else:
            g, x, y = extended_gcd(a, b)
            text = 'GCD = %s\n\nx = %s\n\ny = %s' % (g, x, y)
            text += '\n\nCheck: a*x + b*y = ' + str(a*x + b*y)
            text += '\nCorrect: ' + str(a*x + b*y == g == gcd(a, b))

        self.show(text)


if __name__ == '__main__':
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
