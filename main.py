from MainWindow import MainWindow
import tkinter as tk
from Adapter import Adapter
from Parser import Parser


def main():
    root = tk.Tk()
    adapter = Adapter()
    parser = Parser()
    main_window = MainWindow(adapter, parser, master=root)
    main_window.mainloop()


if __name__ == '__main__':
    main()
