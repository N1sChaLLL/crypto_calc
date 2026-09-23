import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


def divides(a, b):
    if a == 0:
        return b == 0
    return b % a == 0


def gcd(a, b):
    a = abs(a)
    b = abs(b)

    while b != 0:
        a, b = b, a % b

    return a


def extended_gcd(a, b):
    old_r, r = abs(a), abs(b)
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    if a < 0:
        old_x = -old_x
    if b < 0:
        old_y = -old_y

    return old_r, old_x, old_y


def modular_inverse(a, m):
    if m <= 0:
        raise ValueError("Modulus must be positive.")

    g, x, _ = extended_gcd(a, m)

    if g != 1:
        raise ValueError(
            "Modular inverse does not exist because gcd(a, m) != 1."
        )

    return x % m


def modular_add(a, b, m):
    if m <= 0:
        raise ValueError("Modulus must be positive.")
    return (a + b) % m


def modular_multiply(a, b, m):
    if m <= 0:
        raise ValueError("Modulus must be positive.")
    return (a * b) % m


def modular_power_naive(a, e, m):
    if m <= 0:
        raise ValueError("Modulus must be positive.")
    if e < 0:
        raise ValueError("Exponent must be non-negative.")

    result = 1 % m

    for _ in range(e):
        result = (result * a) % m

    return result


def modular_power_repeated_squaring(a, e, m):
    if m <= 0:
        raise ValueError("Modulus must be positive.")
    if e < 0:
        raise ValueError("Exponent must be non-negative.")

    result = 1 % m
    base = a % m

    while e > 0:
        if e % 2 == 1:
            result = (result * base) % m

        base = (base * base) % m
        e //= 2

    return result




class Calculator:
    def __init__(self, root):
        self.root = root

        root.title("Modular Arithmetic Calculator")
        root.geometry("900x760")
        root.minsize(760, 650)

        frame = ttk.Frame(root, padding=18)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Modular Arithmetic Calculator",
            font=("Arial", 18, "bold")
        ).pack(anchor="w")

        ttk.Label(
            frame,
            text=(
                "Divisibility, GCD, Extended Euclid, Modular Inverse, "
                "Modular Arithmetic and Exponentiation"
            )
        ).pack(anchor="w", pady=(4, 14))

        input_frame = ttk.LabelFrame(frame, text="Inputs", padding=10)
        input_frame.pack(fill="x", pady=(0, 12))

        self.number_a = self.make_input(input_frame, "First number (a):", 0)
        self.number_b = self.make_input(input_frame, "Second number (b):", 1)
        self.modulus = self.make_input(input_frame, "Modulus (m):", 2)
        self.exponent = self.make_input(input_frame, "Exponent (e):", 3)

        options = ttk.Frame(frame)
        options.pack(fill="x", pady=(0, 12))

        ttk.Button(
            options,
            text="Generate 512-bit numbers",
            command=self.generate
        ).pack(side="left")

        ttk.Button(
            options,
            text="Clear",
            command=self.clear
        ).pack(side="left", padx=8)

        ttk.Label(
            options,
            text="Small numbers are also accepted."
        ).pack(side="left")

        operations = ttk.LabelFrame(frame, text="Operations", padding=10)
        operations.pack(fill="x", pady=(0, 12))

        buttons = [
            ("Divisibility", "divisibility"),
            ("GCD", "gcd"),
            ("Extended Euclid", "extended"),
            ("Modular Inverse", "inverse"),
            ("Modular Add", "mod_add"),
            ("Modular Multiply", "mod_mul"),
            ("Modular Power", "power"),
            ("Power Timing", "timing"),
        ]

        for index, (label, operation) in enumerate(buttons):
            ttk.Button(
                operations,
                text=label,
                command=lambda op=operation: self.calculate(op)
            ).grid(
                row=index // 3,
                column=index % 3,
                padx=5,
                pady=5,
                sticky="ew"
            )

        for column in range(3):
            operations.columnconfigure(column, weight=1)

        ttk.Label(frame, text="Result:").pack(anchor="w")

        self.result = ScrolledText(
            frame,
            height=16,
            wrap="char",
            font=("Courier", 11),
            state="disabled"
        )
        self.result.pack(fill="both", expand=True, pady=(4, 0))

        self.show(
            "Enter the required values and choose an operation.\n\n"
            "a and b are used by most operations.\n"
            "m is the modulus.\n"
            "e is the exponent for modular exponentiation."
        )

    def make_input(self, parent, label, row):
        ttk.Label(parent, text=label).grid(
            row=row,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=4
        )

        field = ScrolledText(
            parent,
            height=2,
            wrap="char",
            font=("Courier", 11)
        )
        field.grid(
            row=row,
            column=1,
            sticky="ew",
            pady=4
        )

        parent.columnconfigure(1, weight=1)

        return field

    def show(self, text):
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("1.0", text)
        self.result.configure(state="disabled")

    def read_field(self, field, name):
        text = "".join(field.get("1.0", "end").split())

        if not text:
            raise ValueError(f"{name} cannot be empty.")

        digits = text[1:] if text.startswith(("+", "-")) else text

        if (
            not digits
            or not digits.isascii()
            or not digits.isdigit()
        ):
            raise ValueError(f"{name} must be a whole integer.")

        value = int(text)

        if abs(value) >= (1 << 4096):
            raise ValueError(
                f"{name} must contain at most 4096 bits."
            )

        return value

    def read_numbers(self, *needed):
        fields = {
            "a": self.number_a,
            "b": self.number_b,
            "m": self.modulus,
            "e": self.exponent
        }

        return {
            name: self.read_field(fields[name], name)
            for name in needed
        }

    def generate(self):
        for field in (
            self.number_a,
            self.number_b,
            self.modulus,
            self.exponent
        ):
            value = random.getrandbits(512)
            value |= 1 << 511

            field.delete("1.0", "end")
            field.insert("1.0", str(value))

        self.show(
            "512-bit values generated.\n\n"
            "Note: the generated modulus is only a random odd/even "
            "512-bit number. For modular inverse it may not be coprime "
            "with a, so another value may be needed."
        )

    def clear(self):
        for field in (
            self.number_a,
            self.number_b,
            self.modulus,
            self.exponent
        ):
            field.delete("1.0", "end")

        self.show("")
        self.number_a.focus_set()

    def calculate(self, operation):
        try:
            if operation == "divisibility":
                values = self.read_numbers("a", "b")
                a, b = values["a"], values["b"]

                text = "a divides b: "
                text += "Yes" if divides(a, b) else "No"

                text += "\nb divides a: "
                text += "Yes" if divides(b, a) else "No"

                if a != 0:
                    text += f"\nb mod |a| = {b % abs(a)}"

                if b != 0:
                    text += f"\na mod |b| = {a % abs(b)}"

                if a == 0 or b == 0:
                    text += (
                        "\n\nZero divides only zero. "
                        "Division by zero is undefined."
                    )

            elif operation == "gcd":
                values = self.read_numbers("a", "b")
                a, b = values["a"], values["b"]

                answer = gcd(a, b)
                text = f"GCD(a, b) = {answer}"

            elif operation == "extended":
                values = self.read_numbers("a", "b")
                a, b = values["a"], values["b"]

                g, x, y = extended_gcd(a, b)

                text = (
                    f"GCD(a, b) = {g}\n\n"
                    f"x = {x}\n\n"
                    f"y = {y}\n\n"
                    f"Check:\n"
                    f"a*x + b*y = {a * x + b * y}\n\n"
                    f"Correct: {a * x + b * y == g}"
                )


            elif operation == "inverse":
                values = self.read_numbers("a", "m")
                a, m = values["a"], values["m"]

                inverse = modular_inverse(a, m)

                text = (
                    f"Inverse of {a} modulo {m} = {inverse}\n\n"
                    f"Check:\n"
                    f"(a * inverse) mod m = {(a * inverse) % m}"
                )

            elif operation == "mod_add":
                values = self.read_numbers("a", "b", "m")
                a, b, m = values["a"], values["b"], values["m"]

                answer = modular_add(a, b, m)

                text = (
                    f"(a + b) mod m = {answer}\n\n"
                    f"({a} + {b}) mod {m} = {answer}"
                )

            elif operation == "mod_mul":
                values = self.read_numbers("a", "b", "m")
                a, b, m = values["a"], values["b"], values["m"]

                answer = modular_multiply(a, b, m)

                text = (
                    f"(a * b) mod m = {answer}\n\n"
                    f"({a} * {b}) mod {m} = {answer}"
                )

            elif operation == "power":
                values = self.read_numbers("a", "e", "m")
                a, e, m = values["a"], values["e"], values["m"]

                answer = modular_power_repeated_squaring(a, e, m)

                text = (
                    f"a^e mod m = {answer}\n\n"
                    f"{a}^{e} mod {m} = {answer}\n\n"
                    f"Method: repeated squaring / square-and-multiply"
                )

            elif operation == "timing":
                values = self.read_numbers("a", "e", "m")
                a, e, m = values["a"], values["e"], values["m"]

                start = time.perf_counter()

                fast_answer = modular_power_repeated_squaring(a, e, m)

                fast_time = time.perf_counter() - start

                if e <= 1_000_000:
                    start = time.perf_counter()

                    slow_answer = modular_power_naive(a, e, m)

                    naive_time = time.perf_counter() - start

                    same = fast_answer == slow_answer

                    text = (
                        f"Naive result: {slow_answer}\n"
                        f"Square-and-multiply result: {fast_answer}\n\n"
                        f"Results match: {same}\n\n"
                        f"Naive time: {naive_time:.8f} seconds\n"
                        f"Square-and-multiply time: "
                        f"{fast_time:.8f} seconds\n\n"
                        f"Exponent: {e}\n"
                        f"Naive operations: approximately {e}\n"
                        f"Square-and-multiply operations: "
                        f"approximately {e.bit_length()}"
                    )
                else:
                    text = (
                        f"Square-and-multiply result: {fast_answer}\n\n"
                        f"Square-and-multiply time: "
                        f"{fast_time:.8f} seconds\n\n"
                        f"Naive method was skipped because e = {e} "
                        f"is too large for a practical experiment.\n\n"
                        f"Naive operations: approximately {e}\n"
                        f"Square-and-multiply operations: "
                        f"approximately {e.bit_length()}"
                    )

            self.show(text)

        except ValueError as error:
            self.show(str(error))


if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
