NUMBER CALCULATOR
=================

A simple Python/Tkinter calculator for two integers, including 512-bit inputs.

Features
--------
1. Check whether a divides b and whether b divides a.
2. Find the GCD using Euclid's algorithm.
3. Find x and y using the Extended Euclidean Algorithm:
   a*x + b*y = gcd(a,b).

Click "Generate 512-bit numbers" to fill both inputs, or enter numbers yourself.
Small and negative integers are accepted. All three algorithms are implemented
manually using loops, conditions and arithmetic operators. No math.gcd, abs,
pow, or other built-in mathematical helpers are used.
Extended Euclid is checked with a*x + b*y and our own Euclidean GCD function.
Standard Python functions handle input/output; random generates sample inputs
and Tkinter provides the GUI.
All the application code is in calculator.py.

Requirements
------------
Python 3.9 or newer with Tkinter. On macOS, use Tk 8.6 or newer.
No pip packages, internet connection, or API keys are needed to run the app.
Python itself is not included in this ZIP.

Run
---
Windows: double-click "Start Windows.bat".
Mac: double-click "Start Mac.command".
Or open a terminal in this folder and run: python calculator.py

If Tkinter is missing on a Mac with Homebrew:
    brew install python-tk@3.12

Example
-------
a = 240, b = 46
GCD = 2
x = -9, y = 47
240*(-9) + 46*47 = 2

This simplified version covers divisibility, GCD and Extended Euclid.
The PDF's additional modular-arithmetic and timing tasks are not included here.
