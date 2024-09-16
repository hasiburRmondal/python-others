import tkinter as tk
from tkinter import ttk, font, colorchooser, filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
from spellchecker import SpellChecker
import re
import webbrowser

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text Editor")
        self.root.geometry("800x600")

        self.text_area = ScrolledText(self.root, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill='both')

        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()

        self.current_font = font.Font(family="Arial", size=12)
        self.text_area.configure(font=self.current_font)

        self.spell_checker = SpellChecker()
        self.text_area.bind("<space>", self.check_spelling)

        self.undo_stack = []
        self.redo_stack = []
        self.text_area.bind("<<Modified>>", self.track_changes)

        self.link_tooltips = {}  # Store tooltips for links

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Print", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find and Replace", command=self.find_replace)

    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        font_families = font.families()
        self.font_family = ttk.Combobox(toolbar, values=font_families, width=30)
        self.font_family.set("Arial")
        self.font_family.bind("<<ComboboxSelected>>", self.change_font)
        self.font_family.pack(side=tk.LEFT, padx=5)

        self.font_size = ttk.Combobox(toolbar, values=list(range(8, 73)), width=5)
        self.font_size.set("12")
        self.font_size.bind("<<ComboboxSelected>>", self.change_font)
        self.font_size.pack(side=tk.LEFT, padx=5)

        ttk.Button(toolbar, text="B", width=5, command=self.toggle_bold).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="I", width=5, command=self.toggle_italic).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="U", width=5, command=self.toggle_underline).pack(side=tk.LEFT, padx=2)

        ttk.Button(toolbar, text="Left", width=5, command=lambda: self.align('left')).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Center", width=5, command=lambda: self.align('center')).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Right", width=5, command=lambda: self.align('right')).pack(side=tk.LEFT, padx=2)

        ttk.Button(toolbar, text="Color", width=5, command=self.change_color).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Link", width=5, command=self.insert_link).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Image", width=5, command=self.insert_image).pack(side=tk.LEFT, padx=2)

    def create_statusbar(self):
        self.statusbar = ttk.Label(self.root, text="", anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.bind("<KeyRelease>", self.update_statusbar)

    def update_statusbar(self, event=None):
        line, col = self.text_area.index(tk.INSERT).split('.')
        words = len(self.text_area.get(1.0, tk.END).split())
        self.statusbar.config(text=f"Line: {line} | Column: {col} | Words: {words}")

    def change_font(self, event=None):
        self.current_font.config(family=self.font_family.get(), size=int(self.font_size.get()))
        self.text_area.configure(font=self.current_font)

    def toggle_bold(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("bold", "sel.first", "sel.last")
        self.text_area.tag_configure("bold", font=font.Font(weight="bold"))

    def toggle_italic(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("italic", "sel.first", "sel.last")
        self.text_area.tag_configure("italic", font=font.Font(slant="italic"))

    def toggle_underline(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "underline" in current_tags:
            self.text_area.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("underline", "sel.first", "sel.last")
        self.text_area.tag_configure("underline", underline=1)

    def align(self, alignment):
        self.text_area.tag_add(alignment, "sel.first", "sel.last")
        self.text_area.tag_configure(alignment, justify=alignment)

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.tag_add("color", "sel.first", "sel.last")
            self.text_area.tag_configure("color", foreground=color)

    def insert_link(self):
        try:
            selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            messagebox.showinfo("No Selection", "Please select the text you want to make into a hyperlink.")
            return

        url = simpledialog.askstring("Insert Link", "Enter URL:")
        if url:
            start_index = self.text_area.index(tk.SEL_FIRST)
            end_index = self.text_area.index(tk.SEL_LAST)

            for tag in self.text_area.tag_names():
                self.text_area.tag_remove(tag, start_index, end_index)

            tag_name = f"link-{start_index}"
            self.text_area.tag_add(tag_name, start_index, end_index)
            self.text_area.tag_configure(tag_name, foreground="blue", underline=1)
            self.text_area.tag_bind(tag_name, "<Button-1>", lambda e: self.open_link(url))
            self.text_area.tag_bind(tag_name, "<Enter>", lambda e: self.show_link_tooltip(e, url, tag_name))
            self.text_area.tag_bind(tag_name, "<Leave>", lambda e: self.hide_link_tooltip(tag_name))


    def show_link_tooltip(self, event, url, tag_name):
        x, y, _, height = self.text_area.bbox(f"@{event.x},{event.y}")
        tooltip = tk.Toplevel(self.root)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root}+{event.y_root + height}")
        label = tk.Label(tooltip, text=url, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()
        self.link_tooltips[tag_name] = tooltip

    def hide_link_tooltip(self, tag_name):
        if tag_name in self.link_tooltips:
            self.link_tooltips[tag_name].destroy()
            del self.link_tooltips[tag_name]

    def open_link(self, url):
        webbrowser.open(url)

    def insert_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            image = tk.PhotoImage(file=file_path)
            self.text_area.image_create(tk.INSERT, image=image)
            self.text_area.image = image  # Keep a reference to prevent garbage collection

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file = filedialog.askopenfile(mode='r')
        if file:
            content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, content)
            file.close()

    def save_file(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if file:
            content = self.text_area.get(1.0, tk.END)
            file.write(content)
            file.close()

    def print_file(self):
        content = self.text_area.get(1.0, tk.END)
        print_window = tk.Toplevel(self.root)
        print_window.title("Print Preview")
        print_text = tk.Text(print_window)
        print_text.insert(tk.INSERT, content)
        print_text.pack()
        print_text.config(state=tk.DISABLED)

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def find_replace(self):
        find_window = tk.Toplevel(self.root)
        find_window.title("Find and Replace")
        find_window.geometry("300x100")

        ttk.Label(find_window, text="Find:").grid(row=0, column=0, padx=5, pady=5)
        find_entry = ttk.Entry(find_window)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(find_window, text="Replace:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = ttk.Entry(find_window)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(find_window, text="Replace All", command=lambda: self.replace_text(find_entry.get(), replace_entry.get())).grid(row=2, column=0, columnspan=2, pady=5)

    def replace_text(self, find_str, replace_str):
        content = self.text_area.get(1.0, tk.END)
        new_content = content.replace(find_str, replace_str)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.INSERT, new_content)

    def check_spelling(self, event):
        content = self.text_area.get(1.0, tk.END)
        words = re.findall(r'\b\w+\b', content)
        misspelled = self.spell_checker.unknown(words)
        for word in misspelled:
            start_index = "1.0"
            while True:
                start_index = self.text_area.search(word, start_index, stopindex=tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                self.text_area.tag_add("misspelled", start_index, end_index)
                start_index = end_index
        self.text_area.tag_configure("misspelled", foreground="red", underline=1)

    def track_changes(self, event):
        if self.text_area.edit_modified():
            self.undo_stack.append(self.text_area.get(1.0, tk.END))
            self.redo_stack.clear()
            self.text_area.edit_modified(False)

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            text = self.undo_stack[-1]
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, text)

    def redo(self):
        if self.redo_stack:
            text = self.redo_stack.pop()
            self.undo_stack.append(text)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.INSERT, text)

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()