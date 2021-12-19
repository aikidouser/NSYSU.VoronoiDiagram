from os import write
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
        self.__case_i = 0
        self.input_case_list = []

        # Step by Step
        self.__if_finished = False
        self.__step_i = 0
        self.__draw_point_set = list()
        self.__draw_line_set = list()
        self.__draw_cvhull_set = list()
        self.__draw_hyper = None

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
        self.__next_btn = tk.Button(
            self.__output_btn_frame, text="Next Case", command=self.__next_case, width=15, height=3)
        self.__clear_btn = tk.Button(
            self.__output_btn_frame, text="Clear", command=self.__clear_graph, width=15, height=3)
        self.__sts_btn = tk.Button(
            self.__output_btn_frame, text='Step by Step', command=self.__step_by_step, width=15, height=3)
        self.__run_btn = tk.Button(
            self.__output_btn_frame, text='Run', command=self.__run_to_end, width=15, height=3)
        self.__write_btn = tk.Button(
            self.__output_btn_frame, text='Output Txt', command=self.__output_file, width=15, height=3)

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
        self.__next_btn.grid(column=0, row=0, padx=2 * pad, pady=2 * pad)
        self.__clear_btn.grid(column=0, row=1, padx=2 * pad, pady=2 * pad)
        self.__sts_btn.grid(column=0, row=2, padx=2 * pad, pady=2 * pad)
        self.__run_btn.grid(column=0, row=3, padx=2 * pad, pady=2 * pad)
        self.__write_btn.grid(column=0, row=4, sticky=tk.S,
                              padx=2 * pad, pady=8 * pad)

    def __choose_file(self):
        self.__file_path_msg.delete('1.0', 'end')
        self.file_path = filedialog.askopenfilename()
        self.__file_path_msg.insert('end', self.file_path)

    def __enter_file(self):
        self.__case_i = 0
        if not self.file_path:
            messagebox.showerror(
                title="Read File Error", message="Please choose the file.")
        else:
            self.__clear_graph()
            self.input_case_list.clear()
            if '.txt' in self.file_path:
                self.__input_preprocess()
            elif '.out' in self.file_path:
                self.__output_show_graph()
            self.file_path = ""

    def __input_preprocess(self):
        print(self.file_path)
        point_num = 0
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "#" in line or (len(line) == 1 and line[0] == "\n"):
                    continue
                if(len(line.split()) == 1):
                    point_num = int(line.split()[0])
                    continue
                if(point_num):
                    tmp_list = list()
                    tmp_list.append(int(line.split()[0]))
                    tmp_list.append(int(line.split()[1]))
                    if tmp_list not in self.point_list:
                        self.point_list.append(tmp_list.copy())
                    point_num -= 1
                if(not point_num):
                    self.input_case_list.append(self.point_list.copy())
                    self.point_list.clear()
        self.__point_init()
        self.__file_path_msg.delete('1.0', 'end')
        self.__file_path_msg.insert('end', 'File read successfully')

    # TODO:
    def __output_show_graph(self):
        print(self.file_path)

        def draw_point(x, y):
            x1, y1 = (x - 3), (y - 3)
            x2, y2 = (x + 3), (y + 3)
            self.__graph.create_oval(x1, y1, x2, y2, fill='black')

        with open(self.file_path, 'r') as f:
            for line in f:
                split_line = line.split()
                if split_line[0] == 'P':
                    draw_point(int(split_line[1]), int(split_line[2]))
                elif split_line[0] == 'E':
                    temp = list(map(float, split_line[1:]))
                    self.__graph.create_line(*temp)

    def __point_init(self):
        self.point_list = self.input_case_list[self.__case_i]
        # del self.input_case_list[0]
        print(self.point_list)
        for point in self.point_list:
            x1, y1 = (point[0] - 3), (point[1] - 3)
            x2, y2 = (point[0] + 3), (point[1] + 3)
            self.__graph.create_oval(x1, y1, x2, y2, fill='black')

    def __draw_point(self, event):
        x1, y1 = (event.x - 3), (event.y - 3)
        x2, y2 = (event.x + 3), (event.y + 3)
        tmp_list = [event.x, event.y]
        if tmp_list not in self.point_list:
            self.point_list.append(tmp_list)
        self.__graph.create_oval(x1, y1, x2, y2, fill='black')

    def __next_case(self):
        print(f"case: {self.__case_i}/{len(self.input_case_list)}")
        if len(self.input_case_list):
            self.__clear_graph()
            self.__case_i += 1
            self.__case_i %= len(self.input_case_list)
            print("test: ", self.input_case_list[self.__case_i])
            self.__point_init()
        else:
            messagebox.showerror(
                title="Read File Error", message="Please choose the file.")

    def __clear_graph(self):
        self.point_list.clear()
        self.__graph.delete('all')
        self.__if_finished = False
        self.__step_i = 0

    def __step_by_step(self):
        print("press one time show one step.")
        # TODO: Del the Hyperplane
        if not self.__if_finished:
            self.__run()
            self.__if_finished = True

        # Del the highlight points
        for point in self.__draw_point_set:
            self.__graph.delete(point)

        if self.__draw_hyper:
            self.__graph.delete(self.__draw_hyper)

        self.__draw_point_set.clear()
        self.__draw_hyper = None

        if self.__step_i >= len(self.vd.record):
            return

        # Draw new highlight points
        for point in self.vd.record[self.__step_i]['points']:
            x1, y1 = (point[0] - 5), (point[1] - 5)
            x2, y2 = (point[0] + 5), (point[1] + 5)
            self.__draw_point_set.append(
                self.__graph.create_oval(x1, y1, x2, y2, fill='red'))

        # Check if I need to del the prev line
        clean_prev = self.vd.record[self.__step_i]['clean']
        edge_type = self.vd.record[self.__step_i]['type']

        if self.vd.record[self.__step_i]['edges']:
            if edge_type == 'n':
                if clean_prev:
                    for edge in self.__draw_line_set:
                        self.__graph.delete(edge)
                    self.__draw_line_set.clear()
                for line in self.vd.record[self.__step_i]['edges']:
                    self.__draw_line_set.append(self.__graph.create_line(line))

            elif edge_type == 'c':
                if clean_prev:
                    # FIXME:
                    for cvhull in self.__draw_cvhull_set[-2:]:
                        self.__graph.delete(cvhull)
                    del self.__draw_cvhull_set[-2:]
                self.__draw_cvhull_set.append(
                    self.__graph.create_line(
                        *self.vd.record[self.__step_i]['edges'], fill="Purple"))

            if edge_type == 'h':
                self.__draw_hyper = self.__graph.create_line(
                    *self.vd.record[self.__step_i]['edges'], fill="Pink")

        self.__step_i += 1

    def __run_to_end(self):
        print("the final output")
        self.__run()
        self.__step_i = len(self.vd.record)

        for line in self.vd.polyedge_list:
            self.__graph.create_line(*line)

        self.__graph.create_line(*self.vd.convex_hull_list, fill="Purple")
        # self.__graph.create_line(*self.vd.hyperplane_list, fill="Blue")

    def __run(self):
        self.vd = VoronoiDiagram(self.point_list)
        print(self.point_list)

    def __output_file(self):
        file_path = str(self.__case_i) + '.out'
        wb_edge = self.vd.polyedge_list.copy()
        wb_point = sorted(self.point_list)

        for edge in wb_edge:
            edge.sort()
        wb_edge.sort()

        with open(file_path, 'w') as f:
            for point in wb_point:
                f.write(f'P {point[0]} {point[1]}\n')
            for edge in wb_edge:
                f.write(
                    f'E {edge[0][0]} {edge[0][1]} {edge[1][0]} {edge[1][1]}\n')
        self.vd.polyedge_list.clear()
