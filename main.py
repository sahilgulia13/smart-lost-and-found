
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import date

from linked_list import LinkedList
from matching import find_possible_matches
from generate_dataset import generate_records, save_records


BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "lost_found_dataset.csv"

FIELDS = [
    "item_id", "report_type", "item_name", "category",
    "brand", "color", "location", "description",
    "date_reported", "contact", "status"
]

CATEGORIES = [
    "Electronics", "Accessories", "Documents", "Clothing", "Other"
]


class LostFoundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Lost & Found Management System")
        self.root.geometry("1180x720")
        self.root.minsize(950, 600)
        self.root.configure(bg="#F3F6FC")

        self.items = LinkedList()
        self.load_data()

        self.setup_style()
        self.build_interface()
        self.refresh_table()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#263247",
            rowheight=29,
            fieldbackground="white",
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#E4EAF5",
            foreground="#18253D",
            font=("Arial", 10, "bold")
        )
        style.configure(
            "TCombobox",
            padding=5
        )

    def load_data(self):
        """Load the CSV into the linked list."""
        if not DATA_FILE.exists():
            save_records(generate_records(1000), DATA_FILE)

        self.items = LinkedList()

        with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for record in reader:
                self.items.append(record)

    def save_data(self):
        """Save the current records to CSV."""
        records = self.items.get_all()

        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(records)

    def build_interface(self):
        header = tk.Frame(self.root, bg="#18253D", padx=22, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="SMART LOST & FOUND",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#18253D"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Campus item reporting • Search • Possible match suggestions",
            font=("Arial", 10),
            fg="#C8D7F0",
            bg="#18253D"
        ).pack(anchor="w", pady=(5, 0))

        stats = tk.Frame(self.root, bg="#F3F6FC", padx=20, pady=12)
        stats.pack(fill="x")

        self.total_label = tk.Label(
            stats, text="Total records: 0",
            font=("Arial", 11, "bold"),
            bg="#F3F6FC", fg="#18253D"
        )
        self.total_label.pack(side="left", padx=(0, 24))

        self.lost_label = tk.Label(
            stats, text="Lost: 0",
            font=("Arial", 11, "bold"),
            bg="#F3F6FC", fg="#B45353"
        )
        self.lost_label.pack(side="left", padx=(0, 24))

        self.found_label = tk.Label(
            stats, text="Found: 0",
            font=("Arial", 11, "bold"),
            bg="#F3F6FC", fg="#237A65"
        )
        self.found_label.pack(side="left")

        toolbar = tk.Frame(self.root, bg="#F3F6FC", padx=20, pady=5)
        toolbar.pack(fill="x")

        tk.Label(
            toolbar, text="Search:", bg="#F3F6FC",
            font=("Arial", 10, "bold")
        ).pack(side="left")

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            toolbar, textvariable=self.search_var, width=27
        )
        search_entry.pack(side="left", padx=8)
        search_entry.bind("<KeyRelease>", lambda event: self.refresh_table())

        self.filter_var = tk.StringVar(value="All")
        filter_box = ttk.Combobox(
            toolbar,
            textvariable=self.filter_var,
            values=["All", "Lost", "Found", "Active", "Claimed", "Returned"],
            state="readonly",
            width=12
        )
        filter_box.pack(side="left", padx=5)
        filter_box.bind(
            "<<ComboboxSelected>>", lambda event: self.refresh_table()
        )

        tk.Button(
            toolbar, text="+ Report Item", command=self.open_add_form,
            bg="#3C65A8", fg="white", relief="flat",
            padx=12, pady=7
        ).pack(side="right", padx=4)

        tk.Button(
            toolbar, text="Find Matches", command=self.show_matches,
            bg="#247A65", fg="white", relief="flat",
            padx=12, pady=7
        ).pack(side="right", padx=4)

        tk.Button(
            toolbar, text="Change Status", command=self.change_status,
            bg="#D9A441", fg="#18253D", relief="flat",
            padx=12, pady=7
        ).pack(side="right", padx=4)

        table_frame = tk.Frame(self.root, bg="#F3F6FC", padx=20, pady=12)
        table_frame.pack(fill="both", expand=True)

        columns = (
            "item_id", "report_type", "item_name", "category",
            "color", "location", "date_reported", "status"
        )

        self.table = ttk.Treeview(
            table_frame, columns=columns, show="headings",
            selectmode="browse"
        )

        headings = {
            "item_id": "ID",
            "report_type": "Type",
            "item_name": "Item",
            "category": "Category",
            "color": "Colour",
            "location": "Location",
            "date_reported": "Reported",
            "status": "Status"
        }

        widths = {
            "item_id": 80, "report_type": 70, "item_name": 140,
            "category": 110, "color": 80, "location": 130,
            "date_reported": 100, "status": 90
        }

        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=widths[column], anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        footer = tk.Label(
            self.root,
            text="Demo dataset contains synthetic records. Verify ownership before returning any item.",
            bg="#F3F6FC", fg="#64748B",
            font=("Arial", 9), pady=8
        )
        footer.pack()

    def refresh_table(self):
        """Refresh records according to search and filter."""
        for row in self.table.get_children():
            self.table.delete(row)

        query = self.search_var.get().strip().lower()
        selected_filter = self.filter_var.get()
        records = self.items.get_all()

        for record in records:
            if selected_filter != "All":
                if selected_filter in ("Lost", "Found"):
                    if record.get("report_type") != selected_filter:
                        continue
                elif record.get("status") != selected_filter:
                    continue

            searchable_text = " ".join(
                str(record.get(key, ""))
                for key in [
                    "item_id", "item_name", "category", "brand",
                    "color", "location", "description"
                ]
            ).lower()

            if query and query not in searchable_text:
                continue

            self.table.insert(
                "", "end",
                values=(
                    record.get("item_id", ""),
                    record.get("report_type", ""),
                    record.get("item_name", ""),
                    record.get("category", ""),
                    record.get("color", ""),
                    record.get("location", ""),
                    record.get("date_reported", ""),
                    record.get("status", "")
                )
            )

        self.update_stats()

    def update_stats(self):
        records = self.items.get_all()
        lost_count = sum(
            1 for record in records
            if record.get("report_type") == "Lost"
        )
        found_count = sum(
            1 for record in records
            if record.get("report_type") == "Found"
        )

        self.total_label.config(text=f"Total records: {len(records)}")
        self.lost_label.config(text=f"Lost: {lost_count}")
        self.found_label.config(text=f"Found: {found_count}")

    def open_add_form(self):
        """Open a form to add a lost or found item."""
        form = tk.Toplevel(self.root)
        form.title("Report an Item")
        form.geometry("440x590")
        form.configure(bg="#F3F6FC")
        form.transient(self.root)
        form.grab_set()

        tk.Label(
            form, text="Report a Lost or Found Item",
            font=("Arial", 16, "bold"),
            bg="#F3F6FC", fg="#18253D"
        ).pack(pady=15)

        variables = {}

        fields = [
            ("report_type", "Report type", ["Lost", "Found"]),
            ("item_name", "Item name", None),
            ("category", "Category", CATEGORIES),
            ("brand", "Brand", None),
            ("color", "Colour", None),
            ("location", "Location", None),
            ("description", "Description", None),
            ("contact", "Contact email or phone", None)
        ]

        body = tk.Frame(form, bg="#F3F6FC", padx=24)
        body.pack(fill="both", expand=True)

        for key, label, options in fields:
            tk.Label(
                body, text=label, bg="#F3F6FC",
                fg="#263247", font=("Arial", 10, "bold")
            ).pack(anchor="w", pady=(5, 2))

            if options:
                variable = tk.StringVar(value=options[0])
                widget = ttk.Combobox(
                    body, textvariable=variable,
                    values=options, state="readonly"
                )
            else:
                variable = tk.StringVar()
                widget = ttk.Entry(body, textvariable=variable)

            widget.pack(fill="x", pady=(0, 3))
            variables[key] = variable

        def submit():
            required = [
                "item_name", "category", "location", "description"
            ]

            if any(not variables[key].get().strip() for key in required):
                messagebox.showwarning(
                    "Missing information",
                    "Please complete item name, category, location, and description.",
                    parent=form
                )
                return

            existing_ids = {
                record["item_id"] for record in self.items.get_all()
            }
            number = 1

            while f"LF{number:04d}" in existing_ids:
                number += 1

            record = {
                "item_id": f"LF{number:04d}",
                "report_type": variables["report_type"].get(),
                "item_name": variables["item_name"].get().strip(),
                "category": variables["category"].get(),
                "brand": variables["brand"].get().strip() or "Unknown",
                "color": variables["color"].get().strip() or "Unknown",
                "location": variables["location"].get().strip(),
                "description": variables["description"].get().strip(),
                "date_reported": date.today().isoformat(),
                "contact": variables["contact"].get().strip(),
                "status": "Active"
            }

            self.items.append(record)

            try:
                self.save_data()
            except OSError as error:
                self.items.delete_by_id(record["item_id"])
                messagebox.showerror(
                    "Save failed", str(error), parent=form
                )
                return

            self.refresh_table()
            form.destroy()
            messagebox.showinfo(
                "Success",
                f"Item reported successfully.\nID: {record['item_id']}",
                parent=self.root
            )

        tk.Button(
            form, text="Submit Report", command=submit,
            bg="#247A65", fg="white", relief="flat",
            padx=15, pady=9
        ).pack(pady=14)

    def selected_record(self):
        selection = self.table.selection()

        if not selection:
            messagebox.showwarning(
                "Select a record", "Please select an item from the table."
            )
            return None

        item_id = self.table.item(selection[0], "values")[0]
        return self.items.find_by_id(item_id)

    def show_matches(self):
        """Find possible matches for a selected lost item."""
        selected = self.selected_record()

        if selected is None:
            return

        if selected.get("report_type") != "Lost":
            messagebox.showinfo(
                "Select a lost item",
                "Please select a record with report type Lost."
            )
            return

        found_records = [
            record for record in self.items.get_all()
            if record.get("report_type") == "Found"
        ]

        matches = find_possible_matches(selected, found_records)

        window = tk.Toplevel(self.root)
        window.title("Possible Matches")
        window.geometry("720x420")
        window.configure(bg="#F3F6FC")

        tk.Label(
            window,
            text=f"Possible matches for {selected['item_name']}",
            font=("Arial", 14, "bold"),
            bg="#F3F6FC", fg="#18253D"
        ).pack(pady=12)

        columns = ("item_id", "item_name", "location", "score")
        tree = ttk.Treeview(
            window, columns=columns, show="headings"
        )

        for column, heading in [
            ("item_id", "Found ID"),
            ("item_name", "Item"),
            ("location", "Location"),
            ("score", "Match score (%)")
        ]:
            tree.heading(column, text=heading)

        tree.pack(fill="both", expand=True, padx=16, pady=10)

        if not matches:
            tk.Label(
                window,
                text="No possible matches found. Try reviewing the description.",
                bg="#F3F6FC", fg="#64748B"
            ).pack(pady=8)
        else:
            for match in matches:
                tree.insert(
                    "", "end",
                    values=(
                        match["item_id"], match["item_name"],
                        match["location"], match["score"]
                    )
                )

        tk.Label(
            window,
            text="Scores are suggestions only; verify ownership manually.",
            bg="#F3F6FC", fg="#64748B"
        ).pack(pady=8)

    def change_status(self):
        """Mark the selected record as active, claimed, or returned."""
        record = self.selected_record()

        if record is None:
            return

        window = tk.Toplevel(self.root)
        window.title("Update Item Status")
        window.geometry("330x200")
        window.configure(bg="#F3F6FC")
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text=f"Update {record['item_id']}",
            font=("Arial", 13, "bold"),
            bg="#F3F6FC", fg="#18253D"
        ).pack(pady=16)

        status_var = tk.StringVar(value=record.get("status", "Active"))
        ttk.Combobox(
            window, textvariable=status_var,
            values=["Active", "Claimed", "Returned"],
            state="readonly"
        ).pack(pady=5)

        def save_status():
            old_status = record.get("status", "Active")
            record["status"] = status_var.get()

            try:
                self.save_data()
            except OSError as error:
                record["status"] = old_status
                messagebox.showerror(
                    "Save failed", str(error), parent=window
                )
                return

            self.refresh_table()
            window.destroy()

        tk.Button(
            window, text="Save Status", command=save_status,
            bg="#3C65A8", fg="white", relief="flat",
            padx=12, pady=7
        ).pack(pady=12)


def main():
    root = tk.Tk()
    LostFoundApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
