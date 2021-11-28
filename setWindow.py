import tkinter as tk
from tkinter import Canvas
from tkinter import filedialog, messagebox
from VDAlgo import VoronoiDiagram


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Voronoi Diagram')
        # self.window.geometry('750x650')
        self.file_path = ""
        self.point_list = []
        self.input_case_list = []

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
        self.__graph = Canvas(self.__canvas_frame,
                              width=600, height=600, bg='white')
        self.__graph.bind("<Button-1>", self.__draw_point)

        # exe part
        self.__output_btn_frame = tk.Frame(self.window, width=130, height=600)
        self.__clear_btn = tk.Button(
            self.__output_btn_frame, text="Clear", command=self.__clear_graph, width=15, height=3)
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

        self.__file_path_msg.insert('end', 'Please choose a input file')

        # place the canvas part
        self.__canvas_frame.grid(
            column=0, row=1, padx=pad, pady=pad, sticky=tk.N)
        self.__graph.grid(column=0, row=0)

        # place the exe button part
        self.__output_btn_frame.grid(
            column=1, row=1, padx=pad, pady=pad, sticky=tk.W + tk.N)
        self.__clear_btn.grid(column=0, row=0, padx=2 * pad, pady=2 * pad)
        self.__sts_btn.grid(column=0, row=1, pady=2 * pad)
        self.__run_btn.grid(column=0, row=2, pady=2 * pad)

    def __choose_file(self):
        self.__file_path_msg.delete('1.0', 'end')
        self.file_path = filedialog.askopenfilename()
        self.__file_path_msg.insert('end', self.file_path)

    def __enter_file(self):
        if not self.file_path:
            messagebox.showerror(
                title="Read File Error", message="Please choose the file.")
        else:
            self.__clear_graph()
            print("Deal with the input file.")
            self.__input_preprocess()
            self.file_path = ""

    def __input_preprocess(self):
        print(self.file_path)
        point_num = 0
        with open(self.file_path, 'r') as f:
            for line in f:
                if "#" in line:
                    continue
                if(len(line.split()) == 1):
                    point_num = int(line.split()[0])
                    continue
                if(point_num):
                    tmp_list = list()
                    tmp_list.append(int(line.split()[0]))
                    tmp_list.append(int(line.split()[1]))
                    self.point_list.append(tmp_list.copy())
                    point_num -= 1
                if(not point_num):
                    self.input_case_list.append(self.point_list.copy())
                    self.point_list.clear()
        self.__point_init()
        self.__file_path_msg.delete('1.0', 'end')
        self.__file_path_msg.insert('end', 'File read successfully')

    def __point_init(self):
        self.point_list = self.input_case_list[0]
        del self.input_case_list[0]
        print(self.point_list)
        for point in self.point_list:
            x1, y1 = (point[0] - 3), (point[1] - 3)
            x2, y2 = (point[0] + 3), (point[1] + 3)
            self.__graph.create_oval(x1, y1, x2, y2, fill='black')

    def __draw_point(self, event):
        x1, y1 = (event.x - 3), (event.y - 3)
        x2, y2 = (event.x + 3), (event.y + 3)
        tmp_list = [event.x, event.y]
        self.point_list.append(tmp_list)
        self.__graph.create_oval(x1, y1, x2, y2, fill='black')

    def __clear_graph(self):
        self.point_list.clear()
        self.__graph.delete('all')

    def __step_by_step(self):
        print("press one time show one step.")
        self.__run()


    def __run_to_end(self):
        print("the final output")
        self.__run()

    def __run(self):
        self.vd = VoronoiDiagram(self.point_list)
        print(self.point_list)

        print(f"num of line: {len(self.vd.polyedge_list)}")
        self.__graph.create_line(*self.vd.polyedge_list[0], fill='blue')
        self.__graph.create_line(*self.vd.polyedge_list[1], fill='red')
        self.__graph.create_line(*self.vd.polyedge_list[2], fill='yellow')


        # for line in self.vd.polyedge_list:
        #     self.__graph.create_line(*line, color=)
