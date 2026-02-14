import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import pyperclip

class AdvancedPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.lowercase = "abcdefghijklmnopqrstuvwxyz"
        self.uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.digits = "0123456789"
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous = "0O1lI"
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="🔐 Advanced Password Generator",
                         font=("Arial", 18, "bold"))
        title.pack(pady=20)
        length_frame = ttk.LabelFrame(self.root, text="Password Length", padding=10)
        length_frame.pack(pady=10, padx=20, fill="x")
        tk.Label(length_frame, text="Length:").grid(row=0, column=0, sticky="w")
        self.length_var = tk.StringVar(value="16")
        length_spin = tk.Spinbox(length_frame, from_=8, to=128, width=10,
                             textvariable=self.length_var, font=("Arial", 12))
        length_spin.grid(row=0, column=1, padx=10)
        char_frame = ttk.LabelFrame(self.root, text="Character Types", padding=10)
        char_frame.pack(pady=10, padx=20, fill="x")
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        tk.Checkbutton(char_frame, text="Lowercase (a-z)",
                       variable=self.lower_var).grid(row=0, column=0, sticky="w")
        tk.Checkbutton(char_frame, text="Uppercase (A-Z)",
                       variable=self.upper_var).grid(row=1, column=0, sticky="w")
        tk.Checkbutton(char_frame, text="Numbers (0-9)",
                       variable=self.digits_var).grid(row=2, column=0, sticky="w")
        tk.Checkbutton(char_frame, text="Symbols (!@#$...)",
                       variable=self.symbols_var).grid(row=3, column=0, sticky="w")
        self.exclude_ambiguous_var = tk.BooleanVar(value=True)
        tk.Checkbutton(char_frame, text="Exclude ambiguous chars (0,O,1,l,I)",
                       variable=self.exclude_ambiguous_var).grid(row=4, column=0, sticky="w", pady=5)
        display_frame = ttk.LabelFrame(self.root, text="Generated Password", padding=15)
        display_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(display_frame, textvariable=self.password_var,
                                       font=("Consolas", 14), width=40, justify="center",
                                       state="readonly", bg="#f0f0f0")
        self.password_entry.pack(pady=10, fill="x")
        self.strength_var = tk.StringVar(value="No password")
        self.strength_label = tk.Label(display_frame, textvariable=self.strength_var,
                                       font=("Arial", 10, "bold"))
        self.strength_label.pack()
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        self.generate_btn = tk.Button(button_frame, text="Generate Password",
                                      command=self.generate_password,
                                      bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                                      padx=20, pady=5, relief="flat")
        self.generate_btn.pack(side="left", padx=10)
        self.copy_btn = tk.Button(button_frame, text="Copy to Clipboard",
                                  command=self.copy_to_clipboard,
                                  bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                                  padx=20, pady=5, relief="flat", state="disabled")
        self.copy_btn.pack(side="left", padx=10)
        self.generate_password()

    def get_character_set(self):
        charset = ""
        if self.lower_var.get():
            charset += self.lowercase
        if self.upper_var.get():
            charset += self.uppercase
        if self.digits_var.get():
            charset += self.digits
        if self.symbols_var.get():
            charset += self.symbols
        if self.exclude_ambiguous_var.get():
            charset = ''.join(c for c in charset if c not in self.ambiguous)
        return charset

    def ensure_security_rules(self, password, charset_types):
        required_types = []
        if self.lower_var.get():
            required_types.append(self.lowercase)
        if self.upper_var.get():
            required_types.append(self.uppercase)
        if self.digits_var.get():
            required_types.append(self.digits)
        if self.symbols_var.get():
            required_types.append(self.symbols)
        for req_type in required_types:
            if not any(c in req_type for c in password):
                return False
        return True

    def generate_password(self):
        try:
            length = int(self.length_var.get())
            if length < 8:
                messagebox.showwarning("Warning", "Password must be at least 8 characters!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid length!")
            return
        charset = self.get_character_set()
        if not charset:
            messagebox.showwarning("Warning", "Select at least one character type!")
            return
        password = ""
        attempts = 0
        max_attempts = 100
        while attempts < max_attempts:
            password = ''.join(secrets.choice(charset) for _ in range(length))
            if self.ensure_security_rules(password, charset):
                break
            attempts += 1
        if attempts >= max_attempts:
            messagebox.showwarning("Warning",
                                   "Could not generate password meeting all criteria. Using best effort.")
        self.password_var.set(password)
        self.update_strength(password)
        self.copy_btn.config(state="normal")

    def update_strength(self, password):
        length_score = min(len(password) // 8, 4)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        strength = length_score + (1 if has_lower else 0) + (1 if has_upper else 0) + \
                   (1 if has_digit else 0) + (1 if has_symbol else 0)
        strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"]
        colors = ["#ff4444", "#ff8800", "#ffaa00", "#aadd00", "#44ff44", "#00ff00"]
        self.strength_var.set(f"{strength_labels[min(strength, 5)]} ({strength}/6)")
        self.strength_label.config(fg=colors[min(strength, 5)])

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPasswordGenerator(root)
    root.mainloop()