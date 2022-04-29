import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import pyperclip

class MainWindow(tk.Frame):
    def __init__(self, adapter, parser, master=None):
        super().__init__(master)
        self.master = master
        self.adapter = adapter
        self.parser = parser
        self.init_window()
        self.create_widgets()

    def init_window(self):
        self.master.title('PocketBookNotes')
        self.master.state('zoomed')

    def create_widgets(self):
        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=0)
        self.master.rowconfigure(3, weight=0)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=0)
        self.master.columnconfigure(3, weight=0)
        #self.columnconfigure(1, weight=3)
        self.frameButton = tk.Frame(self.master)
        self.frameButton.grid(row=0, column=0, padx=5, pady=5, stick='nswe', columnspan=3)
        self.buttonOpenSorted = tk.Button(self.frameButton, command=lambda: self.load_file(sort_data=False),
                                          text='Load sorted notes', pady=10)
        self.buttonOpenSorted.grid(row=0, column=0, padx=5, pady=5, sticky='nwe')
        self.buttonOpenUnSorted = tk.Button(self.frameButton, command=lambda: self.load_file(sort_data=True),
                                            text='Load unsorted notes', pady=10)
        self.buttonOpenUnSorted.grid(row=1, column=0, padx=5, pady=5, sticky='nwe')
        self.buttonSave = tk.Button(self.frameButton, command=self.save_file, text='Save notes', pady=10)
        self.buttonSave.grid(row=1, column=1, padx=5, pady=5, sticky='nwe')
        separator = ttk.Separator(self.frameButton, orient='vertical')
        separator.grid(row=0, column=2, rowspan=2, sticky='wns')
        # self.topLabel = ttk.Label(self.master, ) name of book TODO
        self.buttonUp = tk.Button(self.frameButton, command=lambda:
                                                        self.move('up'), text='↑ Move note up', pady=10)
        self.buttonUp.grid(row=0, column=3, padx=5, pady=5, sticky='we')
        self.buttonDown = tk.Button(self.frameButton, command=lambda:
                                                        self.move('down'), text='↓ Move note down', pady=10)
        self.buttonDown.grid(row=1, column=3, padx=5, pady=5, sticky='we')
        self.buttonCopy = tk.Button(self.frameButton, command=self.copy_note_to_clipboard,
                                    text='copy note to clipboard', pady=10)
        self.buttonCopy.grid(row=1, column=4, padx=5, pady=5, sticky='e')
        #treeview
        self.treeviewFrame = ttk.Frame(self.master)
        self.treeviewFrame.grid(row=1, column=0, sticky='nswe', rowspan=3)
        self.treeView = ttk.Treeview(self.treeviewFrame, columns=('page', 'note'), show='headings')
        self.treeView.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')
        self.noteContent = tk.Text(self.master, state="disabled", wrap="word")
        self.noteContent.grid(row=1, column=1, padx=5, pady=5, sticky='nswe', columnspan=2)
        #scrollbar
        self.treeview_scrollbar_vertical = ttk.Scrollbar(self.treeviewFrame, orient='vertical')
        self.treeview_scrollbar_vertical.grid(row=0, column=0, sticky='ns')
        self.treeView.configure(yscrollcommand=self.treeview_scrollbar_vertical.set)
        self.treeview_scrollbar_vertical.configure(command=self.treeView.yview)
        # noteconent scrollbar
        self.notecontent_scrollbar_vertical = ttk.Scrollbar(self.master, orient='vertical')
        self.notecontent_scrollbar_vertical.grid(row=1, column=2, stick='ns')
        self.noteContent.configure(yscrollcommand=self.notecontent_scrollbar_vertical.set)
        self.notecontent_scrollbar_vertical.configure(command=self.noteContent.yview)
        # row and column configure
        self.treeviewFrame.rowconfigure(0, weight=1)
        self.treeviewFrame.columnconfigure(0, weight=0)
        self.treeviewFrame.columnconfigure(1, weight=1)
        self.frameButton.rowconfigure(0, weight=1)
        self.frameButton.rowconfigure(1, weight=1)
        self.frameButton.columnconfigure(0, weight=0)
        self.frameButton.columnconfigure(1, weight=0)
        self.frameButton.columnconfigure(2, weight=0)
        self.frameButton.columnconfigure(3, weight=0)
        self.frameButton.columnconfigure(4, weight=1)

    def init_tree_view(self, treeview, notes):
        treeview.column('# 1', anchor='center', width=40)
        treeview.heading('# 1', text="page")
        treeview.column('# 2', anchor='center')
        treeview.heading('# 2', text="note")
        treeview_index = 0
        if notes:
            # clear treeview
            # delete children if exists
            if treeview.get_children():
                treeview.delete(*treeview.get_children())
            for note in notes:
                treeview.insert(parent="", index=treeview_index, text='', values=(note.page, note.content))
                treeview_index += 1

    def move(self, direction):
        items = self.treeView.selection()
        if direction == "up":
            for item in items:
                self.treeView.move(item, self.treeView.parent(item), self.treeView.index(item) - 1)
        elif direction == "down":
            for item in items:
                self.treeView.move(item, self.treeView.parent(item), self.treeView.index(item) + 1)

    def show_item(self, event):
        index = self.treeView.selection()[0]
        item = self.treeView.item(index)
        #tk.messagebox.showinfo(title=None, message=item['values'][1])
        #self.noteContent['text'] = item['values'][1]
        self.noteContent.configure(state='normal')
        self.noteContent.delete(1.0, 'end')
        self.noteContent.insert(1.0, item['values'][1])
        self.noteContent.configure(state='disabled')

    def load_data(self, path: str, sort_data: bool):
        file_handler = self.adapter.open_file(path)
        if(file_handler):
            notes = self.parser.parse_html_file(file_handler)
        # sorting
            if(sort_data is True):
                notes = sorted(notes, key=lambda note: int(note.page))
            self.refresh_treeview()
            self.init_tree_view(self.treeView, notes)

    def refresh_treeview(self):
        self.treeView.destroy()
        self.treeView = ttk.Treeview(self.treeviewFrame, columns=('page', 'note'), show='headings')
        self.treeView.bind("<Double-Button-1>", self.show_item)
        self.treeView.configure(yscrollcommand=self.treeview_scrollbar_vertical.set)
        self.treeview_scrollbar_vertical.configure(command=self.treeView.yview)
        self.treeView.grid(row=0, column=1, padx=5, pady=5, sticky='nswe')


    def copy_note_to_clipboard(self):
        content = self.noteContent.get(1.0, 'end')
        pyperclip.copy(str(content))

    def load_file(self, sort_data: bool):
        filetypes = [('notes from pocketbook', '.html')]
        path = tk.filedialog.askopenfilename(title="Please select a file to open:", filetypes=filetypes,)
        if path:
            self.load_data(path, sort_data)

    def save_file(self):
        values_list = []
        for child in self.treeView.get_children():
            values_list.append(self.treeView.item(child)['values'])
        path = tk.filedialog.asksaveasfilename(
            defaultextension='.pdf',
            filetypes=[("pdf file", '*.pdf'), ("html file", '*.html')],
            title="Save sorted notes")
        if path:
            self.adapter.save_file(path, values_list)