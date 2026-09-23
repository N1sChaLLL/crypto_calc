import math
import time
import random
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


# ---------- Number theory implementations ----------

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


def euclidean_steps(a, b):
    a = abs(a)
    b = abs(b)

    if a == 0 and b == 0:
        return ["gcd(0, 0) is undefined."]

    steps = []

    while b != 0:
        q = a // b
        r = a % b
        steps.append(f"{a} = {b} × {q} + {r}")
        a, b = b, r

    steps.append(f"GCD = {a}")
    return steps


def extended_gcd(a, b):
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r != 0:
        q = old_r // r

        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y

    if old_r < 0:
        old_r = -old_r
        old_x = -old_x
        old_y = -old_y

    return old_r, old_x, old_y


def modular_inverse(a, m):
    if m <= 0:
        raise ValueError("Modulus must be positive.")

    g, x, _ = extended_gcd(a, m)

    if g != 1:
        raise ValueError("Modular inverse does not exist because gcd(a, m) != 1.")

    return x % m


def modular_addition(a, b, m):
    if m <= 0:
        raise ValueError("Modulus must be positive.")

    return (a + b) % m


def modular_multiplication(a, b, m):
    if m <= 0:
        raise ValueError("Modulus must be positive.")

    return (a * b) % m


def modular_power(a, e, m):
    """Modular exponentiation using repeated squaring."""

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


# ---------- Calculator ----------

class Calculator:
    def __init__(self, root):
        self.root = root

        root.title("Modular Arithmetic Calculator")
        root.geometry("900x700")
        root.minsize(780, 600)

        frame = ttk.Frame(root, padding=18)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Modular Arithmetic Calculator",
            font=("Arial", 18, "bold")
        ).pack(anchor="w")

        ttk.Label(
            frame,
            text="Divisibility, GCD, Euclidean Algorithm, Extended Euclid and Modular Arithmetic"
        ).pack(anchor="w", pady=(4, 14))

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="First number (a):").grid(
            row=0, column=0, sticky="w", padx=(0, 8)
        )
        self.number_a = ttk.Entry(input_frame, width=35)
        self.number_a.grid(row=1, column=0, sticky="ew", padx=(0, 8))

        ttk.Label(input_frame, text="Second number (b):").grid(
            row=0, column=1, sticky="w", padx=8
        )
        self.number_b = ttk.Entry(input_frame, width=35)
        self.number_b.grid(row=1, column=1, sticky="ew", padx=8)

        ttk.Label(input_frame, text="Modulus (m):").grid(
            row=0, column=2, sticky="w", padx=8
        )
        self.modulus = ttk.Entry(input_frame, width=25)
        self.modulus.grid(row=1, column=2, sticky="ew", padx=8)

        ttk.Label(input_frame, text="Exponent (e):").grid(
            row=0, column=3, sticky="w", padx=(8, 0)
        )
        self.exponent = ttk.Entry(input_frame, width=25)
        self.exponent.grid(row=1, column=3, sticky="ew", padx=(8, 0))

        for i in range(4):
            input_frame.columnconfigure(i, weight=1)

        ttk.Label(
            frame,
            text="a and b are used for number-theory operations. m is used for modular operations. e is used for repeated squaring."
        ).pack(anchor="w", pady=(8, 14))

        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=(0, 12))

        operations = [
            ("Divisibility", "divisibility"),
            ("GCD", "gcd"),
            ("Euclidean Algorithm", "euclidean"),
            ("Extended Euclid", "extended"),
            ("Modular Inverse", "inverse"),
            ("Modular Addition", "addition"),
            ("Modular Multiplication", "multiplication"),
            ("Square-and-Multiply", "power"),
            ("Time Comparison", "timing"),
            ("Verify All", "verify"),
        ]

        for index, (label, operation) in enumerate(operations):
            ttk.Button(
                buttons,
                text=label,
                command=lambda op=operation: self.calculate(op)
            ).grid(
                row=index // 5,
                column=index % 5,
                padx=4,
                pady=4,
                sticky="ew"
            )

        for i in range(5):
            buttons.columnconfigure(i, weight=1)

        ttk.Button(
            frame,
            text="Clear",
            command=self.clear
        ).pack(anchor="e", pady=(0, 8))

        ttk.Label(frame, text="Result:").pack(anchor="w")

        self.result = ScrolledText(
            frame,
            height=18,
            wrap="word",
            font=("Courier New", 10),
            state="disabled"
        )
        self.result.pack(fill="both", expand=True, pady=(4, 0))

        self.show("Enter values and select an operation.")

    def show(self, text):
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("1.0", text)
        self.result.configure(state="disabled")

    def clear(self):
        self.number_a.delete(0, "end")
        self.number_b.delete(0, "end")
        self.modulus.delete(0, "end")
        self.exponent.delete(0, "end")
        self.show("")

    def read_int(self, entry, name):
        text = entry.get().strip()

        if text == "":
            raise ValueError(f"Please enter {name}.")

        try:
            return int(text)
        except ValueError:
            raise ValueError(f"{name} must be an integer.")

    def get_ab(self):
        a = self.read_int(self.number_a, "a")
        b = self.read_int(self.number_b, "b")
        return a, b

    def get_modulus(self):
        return self.read_int(self.modulus, "the modulus m")

    def get_exponent(self):
        return self.read_int(self.exponent, "the exponent e")

    # ---------- Verification ----------

    def verify_all(self):
        """
        Verify our implementations against trusted Python operations.

        References:
        - math.gcd()
        - Python %
        - Python + and *
        - pow(a, e, m)
        - pow(a, -1, m)
        """

        tests = 100
        results = []

        # Divisibility
        passed = 0
        for _ in range(tests):
            a = random.randint(-1000000, 1000000)
            b = random.randint(-1000000, 1000000)

            if a == 0:
                reference = b == 0
            else:
                reference = (b % a == 0)

            if divides(a, b) == reference:
                passed += 1

        results.append(("Divisibility", passed, tests))

        # GCD
        passed = 0
        for _ in range(tests):
            a = random.randint(-1000000, 1000000)
            b = random.randint(-1000000, 1000000)

            if gcd(a, b) == math.gcd(a, b):
                passed += 1

        results.append(("GCD vs math.gcd()", passed, tests))

        # Euclidean Algorithm
        passed = 0
        for _ in range(tests):
            a = random.randint(1, 1000000)
            b = random.randint(1, 1000000)

            steps = euclidean_steps(a, b)
            reference = math.gcd(a, b)
            final_gcd = int(steps[-1].split("=")[-1].strip())

            if final_gcd == reference:
                passed += 1

        results.append(("Euclidean Algorithm", passed, tests))

        # Extended Euclid
        passed = 0
        for _ in range(tests):
            a = random.randint(-1000000, 1000000)
            b = random.randint(-1000000, 1000000)

            if a == 0 and b == 0:
                b = 1

            g, x, y = extended_gcd(a, b)

            if (
                g == math.gcd(a, b)
                and a * x + b * y == g
            ):
                passed += 1

        results.append(("Extended Euclid", passed, tests))

        # Modular addition
        passed = 0
        for _ in range(tests):
            a = random.randint(-1000000, 1000000)
            b = random.randint(-1000000, 1000000)
            m = random.randint(1, 1000000)

            mine = modular_addition(a, b, m)
            reference = (a + b) % m

            if mine == reference:
                passed += 1

        results.append(("Modular Addition", passed, tests))

        # Modular multiplication
        passed = 0
        for _ in range(tests):
            a = random.randint(-1000000, 1000000)
            b = random.randint(-1000000, 1000000)
            m = random.randint(1, 1000000)

            mine = modular_multiplication(a, b, m)
            reference = (a * b) % m

            if mine == reference:
                passed += 1

        results.append(("Modular Multiplication", passed, tests))

        # Repeated squaring
        passed = 0
        for _ in range(tests):
            a = random.randint(-1000000, 1000000)
            e = random.randint(0, 100000)
            m = random.randint(1, 1000000)

            mine = modular_power(a, e, m)
            reference = pow(a, e, m)

            if mine == reference:
                passed += 1

        results.append(("Square-and-Multiply vs pow()", passed, tests))

        # Modular inverse
        passed = 0
        attempted = 0

        for _ in range(tests):
            m = random.randint(2, 100000)
            a = random.randint(1, m - 1)

            if math.gcd(a, m) != 1:
                continue

            attempted += 1

            mine = modular_inverse(a, m)
            reference = pow(a, -1, m)

            if mine == reference:
                passed += 1

        results.append(("Modular Inverse vs pow()", passed, attempted))

        lines = [
            "VERIFICATION AGAINST PYTHON STANDARD LIBRARY",
            "=" * 62,
            "",
            "Trusted references:",
            "  math.gcd()                  -> GCD",
            "  Python %                    -> divisibility",
            "  Python + and *              -> modular arithmetic",
            "  pow(a, e, m)                -> modular exponentiation",
            "  pow(a, -1, m)               -> modular inverse",
            "",
            f"Random test cases: {tests}",
            "",
        ]

        overall = True

        for name, passed, total in results:
            status = "PASS" if passed == total else "FAIL"
            if passed != total:
                overall = False

            lines.append(f"{name:<38} {passed}/{total}  {status}")

        lines.extend([
            "",
            "=" * 62,
            "OVERALL RESULT: " + ("PASS" if overall else "FAIL"),
            "",
            "Your algorithms are being tested independently.",
            "The standard library is used only as a reference."
        ])

        self.show("\n".join(lines))

    # ---------- Timing ----------

    def time_comparison(self):
        a = self.read_int(self.number_a, "a")
        e = self.get_exponent()
        m = self.get_modulus()

        if e < 0:
            raise ValueError("Exponent must be non-negative.")

        if m <= 0:
            raise ValueError("Modulus must be positive.")

        # We time repeated-squaring against Python's built-in pow().
        # Both compute the same modular exponentiation.
        repetitions = 1000

        start = time.perf_counter()

        for _ in range(repetitions):
            my_result = modular_power(a, e, m)

        my_time = time.perf_counter() - start

        start = time.perf_counter()

        for _ in range(repetitions):
            library_result = pow(a, e, m)

        library_time = time.perf_counter() - start

        lines = [
            "MODULAR EXPONENTIATION TIME COMPARISON",
            "=" * 60,
            "",
            f"a = {a}",
            f"e = {e}",
            f"m = {m}",
            f"Repetitions = {repetitions}",
            "",
            f"Your repeated-squaring result: {my_result}",
            f"Python pow() result:            {library_result}",
            f"Results match:                  {my_result == library_result}",
            "",
            f"Your method total time:          {my_time:.9f} seconds",
            f"Python pow() total time:         {library_time:.9f} seconds",
            "",
            f"Your method average:             {my_time / repetitions:.12f} seconds",
            f"Python pow() average:            {library_time / repetitions:.12f} seconds",
            "",
            "Note:",
            "Timing depends on your computer and Python version.",
            "Run several times for a more reliable comparison."
        ]

        self.show("\n".join(lines))

    # ---------- Operations ----------

    def calculate(self, operation):
        try:
            if operation == "verify":
                self.verify_all()
                return

            if operation == "timing":
                self.time_comparison()
                return

            if operation == "divisibility":
                a, b = self.get_ab()

                lines = [
                    f"a = {a}",
                    f"b = {b}",
                    "",
                    f"a divides b: {'YES' if divides(a, b) else 'NO'}",
                    f"b divides a: {'YES' if divides(b, a) else 'NO'}"
                ]

                self.show("\n".join(lines))
                return

            if operation == "gcd":
                a, b = self.get_ab()
                answer = gcd(a, b)

                self.show(
                    f"gcd({a}, {b}) = {answer}"
                )
                return

            if operation == "euclidean":
                a, b = self.get_ab()
                steps = euclidean_steps(a, b)

                self.show(
                    "EUCLIDEAN ALGORITHM\n"
                    + "=" * 45
                    + "\n\n"
                    + "\n".join(steps)
                )
                return

            if operation == "extended":
                a, b = self.get_ab()
                g, x, y = extended_gcd(a, b)

                check = a * x + b * y

                text = (
                    f"a = {a}\n"
                    f"b = {b}\n\n"
                    f"GCD = {g}\n\n"
                    f"x = {x}\n"
                    f"y = {y}\n\n"
                    f"Bezout identity:\n"
                    f"a*x + b*y = {check}\n\n"
                    f"Check: {check == g}"
                )

                self.show(text)
                return

            if operation == "inverse":
                a, _ = self.get_ab()
                m = self.get_modulus()

                inverse = modular_inverse(a, m)

                self.show(
                    f"a = {a}\n"
                    f"m = {m}\n\n"
                    f"Modular inverse = {inverse}\n\n"
                    f"Check: ({a} × {inverse}) mod {m} = "
                    f"{(a * inverse) % m}"
                )
                return

            if operation == "addition":
                a, b = self.get_ab()
                m = self.get_modulus()
                answer = modular_addition(a, b, m)

                self.show(
                    f"({a} + {b}) mod {m} = {answer}"
                )
                return

            if operation == "multiplication":
                a, b = self.get_ab()
                m = self.get_modulus()
                answer = modular_multiplication(a, b, m)

                self.show(
                    f"({a} × {b}) mod {m} = {answer}"
                )
                return

            if operation == "power":
                a = self.read_int(self.number_a, "a")
                e = self.get_exponent()
                m = self.get_modulus()

                answer = modular_power(a, e, m)

                self.show(
                    "MODULAR EXPONENTIATION USING REPEATED SQUARING\n"
                    + "=" * 55
                    + "\n\n"
                    f"({a}^{e}) mod {m} = {answer}\n\n"
                    "Method:\n"
                    "1. If the exponent is odd, multiply result by base.\n"
                    "2. Square the base modulo m.\n"
                    "3. Divide the exponent by 2.\n"
                    "4. Repeat until exponent becomes 0."
                )
                return

        except ValueError as error:
            self.show("Error: " + str(error))


if __name__ == "__main__":
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
