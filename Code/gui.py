# main gui

import queue, threading
import tkinter as tk
from tkinter import filedialog, ttk
from editor import  PDFEditorBackend

class PDFeditor_GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("MDES-PDF-Editor")
        self.window.geometry("720x550")
        self.window.resizable(False, False)

        self.message_queue = queue.Queue()
        self.stop_event = threading.Event() 
        self.pb = PDFEditorBackend()
        self.processing = False

        self.setup_layout()
        self._update_status("Hello, welcome to PDF Editor built entirely in Python!\n"
            "\nPDF Editor - Quick Guide"
            "\n•Select PDF - Choose input file"
            "\n•Choose Folder - Select output destination"
            "\n•Pick Function - Merge, Delete, Extract, or Split"
            "\nThat's it! The status area will show your results."
            "\nPS:"
            "\n• MERGE: Combine multiple PDFs (no page ranges needed)"
            "\n• EXTRACT/DELETE: Use 1, 3-5, 6 (includes these pages)"
            "\n• SPLIT: Use 5, 9, 12 (splits before these pages)")
        self._process_queue()
        self.window.mainloop()

    def setup_layout(self):
        self.buttons = {}
        self.window.grid_columnconfigure(2, weight=1)
        # Row 0: "PDF Editor" Label in the center 
        tk.Label(self.window, text="PDF Editor", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, padx=20, pady=20)

        label_texts = ["Input PDFs", "Output Folder", "Page Ranges"]
        for row, label_text in enumerate(label_texts, start=1):
            tk.Label(self.window, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="ew")
            self.window.grid_rowconfigure(row, weight=1)

        # Row 1: "Input PDFs" Section
        self.input_PDFs = tk.Listbox(self.window, width=50, height=1)
        self.input_PDFs.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.Add_PDFs_button = ttk.Button(self.window, text="Add PDFs", command=self.add_pdfs)
        self.Add_PDFs_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        self.buttons["add_pdfs"] = self.Add_PDFs_button

        # Row 2: "Output Folder" Section
        self.output_folder = tk.Entry(self.window, width=50)
        self.output_folder.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.Browse_Folder_button  = ttk.Button(self.window, text="Browse Folder", command=self.browse_folder)
        self.Browse_Folder_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
        self.buttons["browse_folder"] = self.Browse_Folder_button

        # Row 3: "Page Ranges" Section
        self.page_ranges = tk.Entry(self.window, width=50)
        self.page_ranges.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        tk.Label(self.window, text="for example, 1, 12-15, 17").grid(row=3, column=2, padx=10, pady=5, sticky="ew")

        # Row 4-8: "Merge", "Delete", "Extract", "Split"
        button_texts = ["Merge", "Delete", "Extract", "Split"]
        for row, text in enumerate(button_texts, start=5):
            button = ttk.Button(self.window, text=text, command=getattr(self, f"{text.lower()}"))
            button.grid(row=row, column=2, padx=5, pady=20, sticky="ew")
            self.buttons[text.lower()] = button

        tk.Label(self.window, text="Info Dashboard", font=("Arial", 14, "bold")).grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Row 4-8: Message Box
        self.message_box = tk.Text(self.window, height=5, width=60)
        self.message_box.grid(row=5, rowspan=4, column=0, columnspan=2, padx=10, pady=10, sticky="nesw")

        # Stop Button
        self.stop_button = ttk.Button(self.window, text="Stop", command=self.stop)
        self.stop_button.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.buttons["stop"] = self.stop_button

    def add_pdfs(self):
        self.file_paths = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf")]
        )

        current_paths_list = list(self.input_PDFs.get(0, tk.END))
        for path in self.file_paths:
            if path not in current_paths_list:
                self.input_PDFs.insert(tk.END, path)

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select an Output Folder")
        if self.folder_path:
            self.output_folder.insert(0, self.folder_path)

    def _disable_buttons(self):
        for name, button in self.buttons.items():
            if name != "stop":
                button.config(state=tk.DISABLED)
        self.window.config(cursor="wait")

    def _enable_buttons(self):
        for name, button in self.buttons.items():
            if name != "stop":
                button.config(state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)
        self.window.config(cursor="")
    
    def _clear_entries(self):
        self.input_PDFs.delete(0, tk.END)
        self.page_ranges.delete(0, tk.END)
        # self.message_box.delete("1.0", tk.END)

    def _update_status(self, message, is_error=False):
        self.message_box.insert("1.0", '\n' + message)
        self.message_box.config(fg="red" if is_error else "green")
    
    def _process_queue(self):
        try:
            while not self.message_queue.empty():
                message, is_error = self.message_queue.get_nowait()
                self._update_status(message, is_error)
                if "Operation finished!" in message or is_error:
                    self._enable_buttons()
                    self._clear_entries()
                    self.processing = False
                    self.stop_event.clear()

        except queue.Empty:
            pass

        finally:
            self.window.after(50, self._process_queue)
               

    def _run_threaded_operation(self, target_method, requires_page_ranges=False):

        input_paths = list(self.input_PDFs.get(0, tk.END))    
        output_folder = self.output_folder.get().strip()
    
        if not input_paths:
            self._update_status("Missing input PDFs.", is_error=True)
            return
        if not output_folder:
            self._update_status("Missing output folder.", is_error=True)
            return
         
        args_tuple = (input_paths, output_folder)   
        
        if requires_page_ranges:
            page_ranges = self.page_ranges.get().strip()
            if not page_ranges:
                self._update_status("Missing page ranges.", is_error=True)
                return
            args_tuple += (page_ranges.replace(" ", "").split(','),)
            self._update_status(f"PDF operation starts ...\nInput paths: {input_paths}, \nOutput folder: {output_folder}, \nPage ranges: {page_ranges}")
        else:
            self._update_status(f"PDF operation starts ... \nInput paths: {input_paths}, \nOutput folder: {output_folder}")

        self.processing = True
        self._disable_buttons()
        self.stop_event.clear()
        # Create and start the thread
        operation_thread = threading.Thread(target=target_method, args=args_tuple+ (self.message_queue, self.stop_event))
        operation_thread.daemon = True
        operation_thread.start()

    def merge(self):
        self._run_threaded_operation(self.pb.merge_pdfs)

    def delete(self):
        self._run_threaded_operation(self.pb.delete_pages, requires_page_ranges=True)

    def extract(self):
        self._run_threaded_operation(self.pb.extract_pages, requires_page_ranges=True)

    def split(self):
        self._run_threaded_operation(self.pb.split_pdfs, requires_page_ranges=True)


    def stop(self):
        if self.processing:
            self._update_status("Stopping operation...", False)
            self.stop_event.set()

    
if __name__ == "__main__":
    app = PDFeditor_GUI() 


