import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import os
from datetime import datetime

class DatabaseApp:
    VERSION = "1.3"
    def __init__(self, master):
        self.master = master
        self.master.title("MySQL Writer")
        self.master.state('zoomed')
        self.master.minsize(800, 600)

        self.create_widgets()
        self.connection = None
        self.log_folder = "C:/SQLWriterLogs"
        self.ensure_log_folder_exists()

    def create_widgets(self):
        # Main frame to contain all widgets
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Database Connection")
        conn_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(conn_frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.host_entry = ttk.Entry(conn_frame)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(conn_frame, text="Port:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.port_entry = ttk.Entry(conn_frame)
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(conn_frame, text="User:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.user_entry = ttk.Entry(conn_frame)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(conn_frame, text="Password:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(conn_frame, show="*")
        self.password_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(conn_frame, text="Database:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.database_entry = ttk.Entry(conn_frame)
        self.database_entry.grid(row=2, column=1, padx=5, pady=5)

        self.connect_button = ttk.Button(conn_frame, text="Connect", command=self.connect_to_database)
        self.connect_button.grid(row=3, column=1, columnspan=2, pady=10)

        # Query frame
        query_frame = ttk.LabelFrame(main_frame, text="SQL Query")
        query_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.query_text = tk.Text(query_frame, height=10)
        self.query_text.pack(padx=5, pady=5, fill="both", expand=True)

        self.execute_button = ttk.Button(query_frame, text="Execute Query", command=self.execute_query)
        self.execute_button.pack(pady=10)

        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Query Results")
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.results_text = tk.Text(results_frame, height=15)
        self.results_text.pack(padx=5, pady=5, fill="both", expand=True)

        # Version label
        self.version_label = ttk.Label(main_frame, text=f"v{self.VERSION}")
        self.version_label.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=5)

    def connect_to_database(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        user = self.user_entry.get()
        password = self.password_entry.get()
        database = self.database_entry.get()

        try:
            self.connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            messagebox.showinfo("Success", "Connected to the database successfully!")
        except pymysql.Error as err:
            messagebox.showerror("Error", f"Error connecting to the database: {err}")

    def execute_query(self):
        if not self.connection:
            messagebox.showerror("Error", "Please connect to a database first.")
            return

        query = self.query_text.get("1.0", "end-1c")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()

            self.results_text.delete("1.0", tk.END)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                self.results_text.insert(tk.END, " | ".join(columns) + "\n")
                self.results_text.insert(tk.END, "-" * (len(" | ".join(columns))) + "\n")

            for row in results:
                self.results_text.insert(tk.END, " | ".join(map(str, row)) + "\n")

            self.connection.commit()
            self.log_query(query, "Success")
        except pymysql.Error as err:
            error_message = f"Error executing query: {err}"
            messagebox.showerror("Error", error_message)
            self.log_query(query, f"Failed: {error_message}")

    def ensure_log_folder_exists(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

    def log_query(self, query, status):
        self.ensure_log_folder_exists()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Query: {query} - Status: {status}\n"
        log_file_path = os.path.join(self.log_folder, "query_log.txt")
        with open(log_file_path, "a") as log_file:
            log_file.write(log_entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()