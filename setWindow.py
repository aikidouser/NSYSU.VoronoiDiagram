import tkinter as tk


class MainWindow:
    def __init__(self):
        pad = 5

        window = tk.Tk()
        window.title('Voronoi Diagram')
        window.geometry('750x650')

        # basic setting
        # read file part
        read_file_frame = tk.Frame(window, width=740, height=25)
        file_path_msg = tk.Text(read_file_frame, width=80, height=1)
        file_input_btn = tk.Button(read_file_frame, text='Choose', width=9)
        enter_btn = tk.Button(read_file_frame, text='Enter', width=9)

        # canvas part
        canvas_frame = tk.Frame(window, width=600, height=600, bg='orange')

        # place
        # place the read file part
        read_file_frame.grid(column=0, row=0, padx=pad, pady=pad, sticky=tk.W + tk.N)
        file_path_msg.grid(column=0, row=0, padx=pad, pady=pad)
        file_input_btn.grid(column=1, row=0, padx=pad)
        enter_btn.grid(column=2, row=0, padx=pad)

        file_path_msg.insert('end', 'Hello World')

        # place the canvas part
        canvas_frame.grid(column=0, row=1, padx=pad, pady=pad, sticky=tk.W + tk.N)

        window.mainloop()
