from shapely.geometry import LineString, Point


class VoronoiDiagram:
    def __init__(self, point_list):
        self.point_list = sorted(point_list)
        self.record = list()
        self.ppdc_list = list()
        self.polypoints_list = list()

    def run(self, type=0):
        print("Start")
        if(not type):
            self.__force_way(self.point_list)

    def __force_way(self, t_point_list):
        # This can only be used in the case of three points.
        print(t_point_list)
        split = int(len(t_point_list)/2)

        if len(t_point_list) <= 1:
            print(f"{t_point_list} return")
            return t_point_list

        elif len(t_point_list) == 2:
            print(f"{t_point_list} return")
            self.ppdc_list.append(
                self.__perpendicular(t_point_list[0], t_point_list[1]))
            self.polypoints_list.append([t_point_list[0], t_point_list[1]])

            t_point_list = sorted(t_point_list, key=lambda x: x[1])

            return t_point_list

        l_pointlist = self.__force_way(t_point_list[0: split])
        print("finish left")
        r_pointlist = self.__force_way(t_point_list[split:])
        print("finish right")

        print("Merge")

    def __perpendicular(self, a, b):
        ppdcline = list()
        midpoint = [(a[0] + b[0])/2, (a[1] + b[1])/2]
        # vector = [a[0] - b[0], a[1] - b[1]]
        normal_vector = [a[1] - b[1], - (a[0] - b[0])]

        try_list = [0, 600]

        for point in try_list:
            stable_x = point
            try:
                const_n = (stable_x - midpoint[0]) / normal_vector[0]
                result_y = midpoint[1] + const_n * normal_vector[1]
            except ZeroDivisionError:
                result_y = -1

            # print(f"const_n: {const_n}, coord: {stable_x} {result_y}")
            if 0 <= stable_x <= 600 and 0 <= result_y <= 600:
                ppdcline.append([stable_x, result_y])

            stable_y = point
            try:
                const_n = (stable_y - midpoint[1]) / normal_vector[1]
                result_x = midpoint[0] + const_n * normal_vector[0]
            except ZeroDivisionError:
                result_x = -1

            # print(f"const_n: {const_n}, coord: {stable_y} {result_x}")
            if 0 <= stable_y <= 600 and 0 <= result_x <= 600:
                ppdcline.append([result_x, stable_y])

        print(f"length: {len(ppdcline)} {ppdcline}")
        return ppdcline

    def __line_intersection(self, line_a, line_b):
        xdiff = (line_a[0][0] - line_a[1][0], line_b[0][0] - line_b[1][0])
        ydiff = (line_a[0][1] - line_a[1][1], line_b[0][1] - line_b[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None

        d = (det(*line_a), det(*line_b))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return [x, y]


if __name__ == '__main__':
    point_list = [[3, 8], [5, 4], [1, 6], [2, 3]]
    vd = VoronoiDiagram(point_list)
    print(vd.point_list)
    vd.run()
