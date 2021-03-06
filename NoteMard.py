import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class Menubar:

    def __init__(self, parent):
        font_specs = ("ubuntu", 9)

        menubar = tk.Menu(parent.master)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="Nuovo File",
                                  accelerator="Ctrl+N",
                                  command=parent.new_file)
        file_dropdown.add_command(label="Apri File",
                                  accelerator="Ctrl+O",
                                  command=parent.open_file)
        file_dropdown.add_command(label="Salva",
                                  accelerator="Ctrl+S",
                                  command=parent.save)
        file_dropdown.add_command(label="Salva con Nome",
                                  accelerator="Ctrl+Shift+S",
                                  command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Esci",
                                  command=parent.master.destroy)

        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Note di Rilascio",
                                   command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About",
                                   command=self.show_about_message)

        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)


    def show_about_message(self):
        box_title = "Riguardo NoteMard"
        box_message = "Un semplice Editor Testuale creato con Python e Tkinter!\nCreato da Marco\nCodice da PyMike"
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = "Note di Rilascio"
        box_message = "Beta 0.10 - NoteMard"
        messagebox.showinfo(box_title, box_message)


class Statusbar:

    def __init__(self, parent):
        font_specs = ("ubuntu", 12)

        self.status = tk.StringVar()
        self.status.set("NoteMard - Text Editor")

        label = tk.Label(parent.textarea, textvariable=self.status, fg="black",
                         bg="lightgrey", anchor='sw', font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set("Il tuo file è stato salvato!")
        else:
            self.status.set("NoteMard - Text Editor")





class PyText:

    def __init__(self, master):
        master.title("Untitled - NoteMard")
        master.geometry("1200x700")

        font_specs = ("ubuntu", 15)

        self.master = master
        self.filename = None

        self.textarea = tk.Text(master, font=font_specs)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)

        self.bind_shortcuts()

    def set_window_title(self, name=None):
        if name:
            self.master.title(name + " - NoteMard")
        else:
            self.master.title("Untitled - NoteMard")

    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Tutti i file", "*.*"),
                       ("File di Testo", "*.txt"),
                       ("Script Python", "*.py"),
                       ("Markdown Text", "*.md"),
                       ("File JavaScript", "*.js"),
                       ("Documenti HTML", "*.html"),
                       ("Documenti CSS", "*.css")])


        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read())
            self.set_window_title(self.filename)

    def save(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textarea_content)
                self.statusbar.update_status(True)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("Tutti i file", "*.*"),
                           ("File di Testo", "*.txt"),
                           ("Script Python", "*.py"),
                           ("Markdown Text", "*.md"),
                           ("File JavaScript", "*.js"),
                           ("Documenti HTML", "*.html"),
                           ("Documenti CSS", "*.css")])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)
            self.statusbar.update_status(True)
        except Exception as e:
            print(e)

    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-S>', self.save_as)
        self.textarea.bind('<Key>', self.statusbar.update_status)


if __name__ == "__main__":
    master = tk.Tk()
    pt = PyText(master)
    master.mainloop()