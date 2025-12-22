import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from backend.models.pantry_system import PantrySystem


class PantryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Pantry Inventory System")
        self.root.geometry("600x520")
        self.system = PantrySystem()
        self.build_main_menu()

    def add_hover_effect(self, widget, normal_bg, hover_bg):
        if widget is None:
            return

        def on_enter(e):
            widget.configure(bg=hover_bg)

        def on_leave(e):
            widget.configure(bg=normal_bg)

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def build_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF7EE")

        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((130, 130), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(img)
        else:
            self.logo_photo = None

        header = tk.Frame(self.root, bg="#FFF7EE")
        header.pack(pady=20)

        if self.logo_photo:
            tk.Label(header, image=self.logo_photo, bg="#FFF7EE").pack(side="left", padx=10)

        tk.Label(
            header,
            text="Food Pantry",
            font=("Segoe UI", 30, "bold"),
            bg="#FFF7EE",
            fg="#FF8C42"
        ).pack(side="left")

        btn_style = {
            "font": ("Segoe UI", 13),
            "bg": "#FF8C42",
            "fg": "white",
            "activebackground": "#e6762f",
            "bd": 0,
            "width": 22,
            "height": 1
        }

        btn1 = tk.Button(self.root, text="Add Donation / Item", command=self.open_add_item_screen, **btn_style)
        btn1.pack(pady=8)
        self.add_hover_effect(btn1, "#FF8C42", "#e6762f")

        btn2 = tk.Button(self.root, text="Add Recipient", command=self.open_add_recipient_screen, **btn_style)
        btn2.pack(pady=8)
        self.add_hover_effect(btn2, "#FF8C42", "#e6762f")

        btn3 = tk.Button(self.root, text="Record Distribution", command=self.open_distribution_screen, **btn_style)
        btn3.pack(pady=8)
        self.add_hover_effect(btn3, "#FF8C42", "#e6762f")

        btn4 = tk.Button(self.root, text="View Inventory", command=self.open_inventory_screen, **btn_style)
        btn4.pack(pady=8)
        self.add_hover_effect(btn4, "#FF8C42", "#e6762f")

        btn5 = tk.Button(self.root, text="View Distribution History", command=self.open_history_screen, **btn_style)
        btn5.pack(pady=8)
        self.add_hover_effect(btn5, "#FF8C42", "#e6762f")

    def open_add_item_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF7EE")
        tk.Label(self.root, text="Add Donation / Item", font=("Segoe UI", 20, "bold"), bg="#FFF7EE", fg="#FF8C42").pack(pady=15)

        form = tk.Frame(self.root, bg="white")
        form.pack(pady=20)

        tk.Label(form, text="Item Name:", bg="white", font=("Segoe UI", 13)).pack()
        name_entry = tk.Entry(form, font=("Segoe UI", 12))
        name_entry.pack(pady=5)

        tk.Label(form, text="Category:", bg="white", font=("Segoe UI", 13)).pack()
        category_entry = tk.Entry(form, font=("Segoe UI", 12))
        category_entry.pack(pady=5)

        tk.Label(form, text="Quantity:", bg="white", font=("Segoe UI", 13)).pack()
        quantity_entry = tk.Entry(form, font=("Segoe UI", 12))
        quantity_entry.pack(pady=5)

        def submit_item():
            name = name_entry.get()
            category = category_entry.get()
            quantity = quantity_entry.get()

            if not name or not category or not quantity.isdigit():
                messagebox.showerror("Error", "Please enter valid item information!")
                return

            self.system.add_item(name, category, int(quantity))
            messagebox.showinfo("Success", f"Added {quantity} units of {name}.")
            self.build_main_menu()

        btn1 = tk.Button(self.root, text="Add Item", bg="#FF8C42", fg="white", width=20, command=submit_item)
        btn1.pack(pady=10)
        self.add_hover_effect(btn1, "#FF8C42", "#e6762f")

        btn2 = tk.Button(self.root, text="Back", bg="#ccc", width=15, command=self.build_main_menu)
        btn2.pack()
        self.add_hover_effect(btn2, "#ccc", "#bbb")

    def open_add_recipient_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF7EE")
        tk.Label(self.root, text="Add Recipient", font=("Segoe UI", 20, "bold"), bg="#FFF7EE", fg="#FF8C42").pack(pady=15)

        form = tk.Frame(self.root, bg="white")
        form.pack(pady=20)

        tk.Label(form, text="Recipient Name:", bg="white", font=("Segoe UI", 13)).pack()
        name_entry = tk.Entry(form, font=("Segoe UI", 12))
        name_entry.pack(pady=5)

        tk.Label(form, text="Household Size:", bg="white", font=("Segoe UI", 13)).pack()
        size_entry = tk.Entry(form, font=("Segoe UI", 12))
        size_entry.pack(pady=5)

        tk.Label(form, text="Notes:", bg="white", font=("Segoe UI", 13)).pack()
        notes_entry = tk.Entry(form, font=("Segoe UI", 12))
        notes_entry.pack(pady=5)

        def submit_recipient():
            name = name_entry.get()
            size = size_entry.get()
            notes = notes_entry.get()

            if not name or not size.isdigit():
                messagebox.showerror("Error", "Please enter valid recipient information!")
                return

            self.system.add_recipient(name, int(size), notes)
            messagebox.showinfo("Success", f"Recipient '{name}' added.")
            self.build_main_menu()

        btn1 = tk.Button(self.root, text="Add Recipient", bg="#FF8C42", fg="white", width=20, command=submit_recipient)
        btn1.pack(pady=10)
        self.add_hover_effect(btn1, "#FF8C42", "#e6762f")

        btn2 = tk.Button(self.root, text="Back", bg="#ccc", width=15, command=self.build_main_menu)
        btn2.pack()
        self.add_hover_effect(btn2, "#ccc", "#bbb")

    def open_inventory_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF7EE")
        tk.Label(self.root, text="Inventory List", font=("Segoe UI", 20, "bold"), bg="#FFF7EE", fg="#FF8C42").pack(pady=15)

        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=10)

        inventory = self.system.get_inventory()

        if not inventory:
            tk.Label(frame, text="No items are in inventory currently.", bg="white", font=("Segoe UI", 13)).pack(pady=10)
        else:
            for item in inventory:
                tk.Label(frame, text=f"{item.name} | {item.category} | {item.quantity} units", bg="white", font=("Segoe UI", 13)).pack(pady=5)

        btn = tk.Button(self.root, text="Back", bg="#ccc", width=15, command=self.build_main_menu)
        btn.pack(pady=15)
        self.add_hover_effect(btn, "#ccc", "#bbb")

    def open_distribution_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF7EE")
        tk.Label(self.root, text="Record Distribution", font=("Segoe UI", 20, "bold"), bg="#FFF7EE", fg="#FF8C42").pack(pady=15)

        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=20)

        tk.Label(frame, text="Recipient:", bg="white", font=("Segoe UI", 13)).pack()
        recipients = [r.name for r in self.system.recipients]

        if not recipients:
            tk.Label(frame, text="No recipients were found.", bg="white", fg="red").pack()
            tk.Button(self.root, text="Back", bg="#ccc", command=self.build_main_menu).pack(pady=10)
            return

        recipient_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=recipient_var, values=recipients, state="readonly").pack(pady=5)

        tk.Label(frame, text="Item:", bg="white", font=("Segoe UI", 13)).pack()
        items = [i.name for i in self.system.items]

        if not items:
            tk.Label(frame, text="No items are currently available.", bg="white", fg="red").pack()
            tk.Button(self.root, text="Back", bg="#ccc", command=self.build_main_menu).pack(pady=10)
            return

        item_var = tk.StringVar()
        ttk.Combobox(frame, textvariable=item_var, values=items, state="readonly").pack(pady=5)

        tk.Label(frame, text="Quantity:", bg="white", font=("Segoe UI", 13)).pack()
        qty_entry = tk.Entry(frame, font=("Segoe UI", 12))
        qty_entry.pack(pady=5)

        def submit_distribution():
            r = recipient_var.get()
            i = item_var.get()
            q = qty_entry.get()

            if not r or not i or not q.isdigit():
                messagebox.showerror("Error", "Please ensure that all fields are filled out correctly.")
                return

            result = self.system.record_distribution(i, r, int(q))

            if result:
                messagebox.showinfo("Success", f"Gave {q} units of {i} to {r}.")
                self.build_main_menu()
            else:
                messagebox.showerror("Error", "Not enough inventory.")

        btn1 = tk.Button(self.root, text="Record Distribution", bg="#FF8C42", fg="white", width=20, command=submit_distribution)
        btn1.pack(pady=10)
        self.add_hover_effect(btn1, "#FF8C42", "#e6762f")

        btn2 = tk.Button(self.root, text="Back", bg="#ccc", width=15, command=self.build_main_menu)
        btn2.pack(pady=10)
        self.add_hover_effect(btn2, "#ccc", "#bbb")

    def open_history_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF7EE")
        tk.Label(self.root, text="Distribution History", font=("Segoe UI", 20, "bold"), bg="#FFF7EE", fg="#FF8C42").pack(pady=15)

        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=10)

        if not self.system.history:
            tk.Label(frame, text="No distribution records yet.", bg="white", font=("Segoe UI", 13)).pack(pady=10)
        else:
            for record in self.system.history:
                tk.Label(frame, text=f"{record['recipient']} received {record['quantity']} of {record['item']}", bg="white", font=("Segoe UI", 13)).pack(pady=5)

        btn1 = tk.Button(self.root, text="Back", bg="#ccc", width=15, command=self.build_main_menu)
        btn1.pack(pady=15)
        self.add_hover_effect(btn1, "#ccc", "#bbb")


if __name__ == "__main__":
    root = tk.Tk()
    app = PantryApp(root)
    root.mainloop()
