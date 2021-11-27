from shapely.geometry import LineString, Point


class VoronoiDiagram:
    def __init__(self, point_list):
        self.point_list = sorted(point_list, key=lambda x: x[0])
        self.record = list()

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
            return

        elif len(t_point_list) == 2:
            print(f"{t_point_list} return")
            self.__perpendicular(t_point_list[0], t_point_list[1])
            return

        self.__force_way(t_point_list[0: split])
        print("finish left")
        self.__force_way(t_point_list[split:])
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
            const_n = (stable_x - midpoint[0]) / normal_vector[0]
            result_y = midpoint[1] + const_n * normal_vector[1]

            # print(f"const_n: {const_n}, coord: {stable_x} {result_y}")
            if 0 <= stable_x <= 600 and 0 <= result_y <= 600:
                ppdcline.append([stable_x, result_y])

            stable_y = point
            const_n = (stable_y - midpoint[1]) / normal_vector[1]
            result_x = midpoint[0] + const_n * normal_vector[0]

            # print(f"const_n: {const_n}, coord: {stable_y} {result_x}")
            if 0 <= stable_y <= 600 and 0 <= result_x <= 600:
                ppdcline.append([stable_y, result_x])

        # print(f"length: {len(ppdcline)} {ppdcline}")
        return ppdcline


if __name__ == '__main__':
    point_list = [[9, 5], [3, 5], [1, 6], [10, 2], [4, 4]]
    vd = VoronoiDiagram(point_list)
    print(vd.point_list)
    vd.run()
