#!/bin/zsh
cd -- "${0:A:h}"
for python_path in /opt/homebrew/bin/python3.12 /usr/local/bin/python3.12 python3; do
    if "$python_path" -c 'import tkinter; assert tkinter.TkVersion >= 8.6' >/dev/null 2>&1; then
        exec "$python_path" calculator.py
    fi
done
print 'Python with Tkinter is required.'
print 'On a Mac with Homebrew, run: brew install python-tk@3.12'
read '?Press Return to close.'
