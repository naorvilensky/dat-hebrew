import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from utils.constants import DAT_MODELS
from utils.dat_hebrew import DatHebrew


class FileProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DAT Hebrew Transpiler")
        self.root.geometry("600x400")

        self.add_model_selection_dropdown()
        self.add_input_and_output_files()
        self.add_log_area()
        self.add_buttons()

    def add_model_selection_dropdown(self):
        self.dropdown_frame = tk.Frame(self.root)
        self.dropdown_frame.pack(anchor='w', padx=20, pady=20)

        # Model selector variable
        self.selected_model = tk.StringVar()
        self.selected_model.set(DAT_MODELS[0])  # Default value

        # Label
        tk.Label(self.dropdown_frame, text="Choose model:").pack(side='left')

        # Dropdown
        self.dropdown = tk.OptionMenu(
            self.dropdown_frame, self.selected_model, *DAT_MODELS)
        self.dropdown.pack(side="left", padx=(10, 0))

        def selected_model_trace(*_):
            model = self.selected_model.get()
            self.dat_hebrew.set_used_model(model)
            self.log(f"Model '{model}' was selected")

        self.selected_model.trace_add("write", selected_model_trace)

    def add_input_and_output_files(self):
        # File selection
        self.file_label = tk.Label(self.root, text="Select Input File:")
        self.file_label.pack(anchor='w', padx=10, pady=(10, 0))

        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack(fill='x', padx=10)

        self.file_entry = tk.Entry(self.file_frame, width=50)
        self.file_entry.pack(side='left', fill='x', expand=True)

        self.browse_button = tk.Button(
            self.file_frame, text="Browse", command=self.browse_file)
        self.browse_button.pack(side='left', padx=5)

        self.dropdown_frame = tk.Frame(self.root)
        self.dropdown_frame.pack(anchor='w', padx=20, pady=20
                                 )

        # Output filename
        self.output_label = tk.Label(self.root, text="Output File Name:")
        self.output_label.pack(anchor='w', padx=10, pady=(10, 0))

        self.output_entry = tk.Entry(self.root, width=50)
        self.output_entry.pack(fill='x', padx=10)

    def add_log_area(self):
        # Log area
        self.log_label = tk.Label(self.root, text="Logs:")
        self.log_label.pack(anchor='w', padx=10, pady=(10, 0))

        self.log_area = scrolledtext.ScrolledText(
            self.root, wrap='word', height=10)
        self.log_area.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.log_area.config(state='disabled')

    def add_buttons(self):
        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=(0, 10))

        self.apply_button = tk.Button(
            self.button_frame, text="Apply", command=self.apply)
        self.apply_button.pack(side='left', padx=5)

        self.clear_button = tk.Button(
            self.button_frame, text="Clear Logs", command=self.clear_logs)
        self.clear_button.pack(side='left', padx=5)

        self.dat_hebrew = DatHebrew(lambda l: self.log(l))

    def browse_file(self):
        filepath = filedialog.askopenfilename(initialdir=os.getcwd())
        if filepath:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filepath)
            base, ext = os.path.splitext(self.file_entry.get())
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(
                0, base + f'_{self.selected_model.get()}_answers' + ext)
            self.log(f"Selected file: {filepath}")

    def apply(self):
        input_file = self.file_entry.get()
        output_file = self.output_entry.get()

        if not input_file:
            messagebox.showwarning(
                "Missing Input", "Please select an input file.")
            return

        if not output_file:
            messagebox.showwarning(
                "Missing Output", "Please specify an output file name.")
            return

        self.log(f"Processing '{input_file}' and creating '{output_file}'...")
        self.dat_hebrew.set_input_path(input_file)
        self.dat_hebrew.set_output_path(output_file)
        self.dat_hebrew.computed_and_write_to_file()
        self.log("Done!")

    def clear_logs(self):
        self.log_area.config(state='normal')
        self.log_area.delete('1.0', tk.END)
        self.log_area.config(state='disabled')

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
