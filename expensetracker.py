import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import tkinter.font as tkFont
import json
from datetime import datetime


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("1100x500")
        self.root.configure(bg="#e6f2ff")

        self.expenses = []
        self.categories = ["Rent", "Food", "Entertainment", "Car", "Credit Cards"]
        self.monthly_budget = self.get_initial_budget()

        self.create_widgets()
        self.setup_styles()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TFrame", background="#fadee2")
        self.style.configure("TLabelframe", background="#fadee2", font=("Courier New", 10, "bold"))
        self.style.configure("TLabelframe.Label", background="#fadee2", foreground="white")
        self.style.configure("TLabel", background="#fadee2", font=("Courier New", 10))
        self.style.configure("TButton", background="#f7f0f1", font=("Courier New", 10), padding=6)
        self.style.configure("TEntry", padding=4)

        self.style.configure("Treeview", font=("Courier New", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Courier New", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#cce5ff")])

    def get_initial_budget(self):
        while True:
            budget = simpledialog.askfloat("budget tracker", "enter monthly budget:", minvalue=0.01)
            if budget is not None:
                return budget
            else:
                if messagebox.askyesno("no budget", "no budget entered... or maybe you're broke. quit?"):
                    self.root.quit()
                    return 0

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        input_frame = ttk.LabelFrame(main_frame, text="add expense", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        ttk.Label(input_frame, text="date (YYYY-MM-DD):").grid(row=0, column=0, sticky=tk.W)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="category:").grid(row=1, column=0, sticky=tk.W)
        self.category_combobox = ttk.Combobox(input_frame, values=self.categories)
        self.category_combobox.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="amount:").grid(row=2, column=0, sticky=tk.W)
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=2)
        ttk.Button(input_frame, text="add expense", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=5)

        category_frame = ttk.LabelFrame(main_frame, text="manage categories", padding="10")
        category_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        self.new_category_entry = ttk.Entry(category_frame)
        self.new_category_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(category_frame, text="add category", command=self.add_category).grid(row=0, column=0, sticky=tk.W)

        display_frame = ttk.LabelFrame(main_frame, text="budget manager", padding="10")
        display_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        self.expense_tree = ttk.Treeview(display_frame, columns=('date', 'category', 'amount'), show='headings')
        self.expense_tree.heading('date', text='date')
        self.expense_tree.heading('category', text='category')
        self.expense_tree.heading('amount', text='amount')
        self.expense_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        button_frame = ttk.Frame(display_frame)
        button_frame.grid(row=5, column=0, pady=5, sticky=tk.W)

        ttk.Button(button_frame, text="edit", command=self.edit_expense).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="delete", command=self.delete_expense).grid(row=0, column=1, padx=5)

        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.expense_tree.configure(yscrollcommand=scrollbar.set)

        self.budget_label = ttk.Label(display_frame, text=f"monthly budget: ${self.monthly_budget:.2f}")
        self.budget_label.grid(row=1, column=0, sticky=tk.W, pady=2)

        self.total_expenses_label = ttk.Label(display_frame, text="total expenses: $0.00")
        self.total_expenses_label.grid(row=2, column=0, sticky=tk.W, pady=2)

        self.remaining_budget_label = ttk.Label(display_frame, text=f"remaining budget: ${self.monthly_budget:.2f}")
        self.remaining_budget_label.grid(row=3, column=0, sticky=tk.W, pady=2)

        # Save Button
        ttk.Button(display_frame, text="save data", command=self.save_data).grid(row=4, column=0, pady=10)

        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

    def add_expense(self):
        try:
            date = self.date_entry.get()
            category = self.category_combobox.get()
            amount = float(self.amount_entry.get())

            self.expenses.append({
                'date': date,
                'category': category,
                'amount': amount
            })

            self.update_expense_list()
            self.update_budget_info()
            self.clear_input_fields()
        except ValueError:
            messagebox.showerror("error", "invalid, check your input")

    def add_category(self):
        new_category = self.new_category_entry.get().strip()
        if new_category and new_category not in self.categories:
            self.categories.append(new_category)
            self.category_combobox['values'] = self.categories
            self.new_category_entry.delete(0, tk.END)
            messagebox.showinfo("category added!", f"'{new_category}' has been added to the categories.")
        else:
            messagebox.showerror("error", "invalid or category already exists")

    def update_expense_list(self):
        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)
        for expense in self.expenses:
            self.expense_tree.insert('', 'end', values=(
                expense['date'],
                expense['category'],
                f"${expense['amount']:.2f}"
            ))

    def update_budget_info(self):
        total_expenses = sum(expense['amount'] for expense in self.expenses)
        remaining_budget = self.monthly_budget - total_expenses

        self.total_expenses_label.config(text=f"total rxpenses: ${total_expenses:.2f}")
        self.remaining_budget_label.config(text=f"remaining budget: ${remaining_budget:.2f}")

    def clear_input_fields(self):
        self.date_entry.delete(0, tk.END)
        self.category_combobox.set('')
        self.amount_entry.delete(0, tk.END)

    def delete_expense(self):
        selected_item = self.expense_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "select an expense to delete")
            return

        confirm = messagebox.askyesno("delete confirmation", "confirm deletion?")
        if confirm:
            item_index = self.expense_tree.index(selected_item)
            del self.expenses[item_index]
            self.update_expense_list()
            self.update_budget_info()

    def edit_expense(self):
        selected_item = self.expense_tree.selection()
        if not selected_item:
            messagebox.showwarning("no selection", "select an expense to edit")
            return

        item_index = self.expense_tree.index(selected_item)
        expense = self.expenses[item_index]

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, expense['date'])

        self.category_combobox.set(expense['category'])

        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(expense['amount']))

        del self.expenses[item_index]
        self.update_expense_list()
        self.update_budget_info()


    def save_data(self):
        data = {
            'budget': self.monthly_budget,
            'categories': self.categories,
            'expenses': self.expenses
        }
        current_date = datetime.now().strftime("%Y-%m")
        default_filename = f"expense_data_{current_date}.json"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=default_filename
        )

        if file_path:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("saved!", f"data saved to {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
