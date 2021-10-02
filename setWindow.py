import tkinter as tk
from tkinter import filedialog


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Voronoi Diagram')
        self.window.geometry('750x650')
        self.file_path = ""

        # basic setting
        # read file part
        self.__read_file_frame = tk.Frame(self.window, width=740, height=25)
        self.__file_path_msg = tk.Text(
            self.__read_file_frame, width=80, height=1)
        self.__file_choose_btn = tk.Button(
            self.__read_file_frame, text='Choose', command=self.__choose_file, width=9)
        self.__enter_btn = tk.Button(
            self.__read_file_frame, text='Enter', command=self.__enter_file, width=9)

        # canvas part
        self.__canvas_frame = tk.Frame(
            self.window, width=600, height=600, bg='orange')

        # exe part
        self.__output_btn_frame = tk.Frame(self.window, width=130, height=600)
        self.__sts_btn = tk.Button(
            self.__output_btn_frame, text='Step by Step', command=self.__step_by_step, width=15, height=3)
        self.__run_btn = tk.Button(
            self.__output_btn_frame, text='Run', command=self.__run_to_end, width=15, height=3)

        self.__place_obj()

    def __place_obj(self):
        pad = 5

        # place the read file part
        self.__read_file_frame.grid(
            column=0, row=0, padx=pad, pady=pad, columnspan=2, sticky=tk.W + tk.N)
        self.__file_path_msg.grid(column=0, row=0, padx=pad, pady=pad)
        self.__file_choose_btn.grid(column=1, row=0, padx=pad)
        self.__enter_btn.grid(column=2, row=0, padx=pad)

        self.__file_path_msg.insert('end', 'Hello World')

        # place the canvas part
        self.__canvas_frame.grid(
            column=0, row=1, padx=pad, pady=pad, sticky=tk.N)

        # place the exe button part
        self.__output_btn_frame.grid(
            column=1, row=1, padx=pad, pady=pad, sticky=tk.W + tk.N)
        self.__sts_btn.grid(column=0, row=0, pady=2 * pad)
        self.__run_btn.grid(column=0, row=1, pady=2 * pad)

    def __choose_file(self):
        self.__file_path_msg.delete('1.0', 'end')
        self.__file_path = filedialog.askopenfilename()
        self.__file_path_msg.insert('end', self.__file_path)

    def __enter_file(self):
        print("The algorithm starts here.")

    def __step_by_step(self):
        print("press one time show one step.")

    def __run_to_end(self):
        print("the final output")


if __name__ == '__main__':

    testWindow = MainWindow()

    testWindow.window.mainloop()
