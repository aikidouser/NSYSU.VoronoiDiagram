import math
from shapely import geometry as geo

class VoronoiDiagram:
    def __init__(self, point_list):
        self.point_list = sorted(point_list)
        self.record = list()
        self.polyedge_list = list()
        self.polypoints_list = list()

        self.run()

    def run(self, type=0):
        print("Start")

        if len(self.point_list) == 1:
            temp_dict = {'points': self.point_list, 'edge': [[-1, -1], [-1, 1]]}
            self.record.append(temp_dict)

        elif len(self.point_list) == 2:
            ppdc = self.__perpendicular(*self.point_list)
            self.polyedge_list.append(ppdc)
            self.polypoints_list.append(self.point_list)
            temp_dict = {'points': self.point_list, 'edge': ppdc}
            self.record.append(temp_dict)


        elif len(self.point_list) == 3:
            self.__3p_force(self.point_list)

    def __garbage(self, t_point_list):
        # This can only be used in the case of three points.
        print(t_point_list)
        split = int(len(t_point_list)/2)
        hyperplane_list = list()

        if len(t_point_list) <= 1:
            print(f"{t_point_list} return")
            return t_point_list

        elif len(t_point_list) == 2:
            self.polyedge_list.append(
                self.__perpendicular(t_point_list[0], t_point_list[1]))
            self.polypoints_list.append([t_point_list[0], t_point_list[1]])

            # t_point_list = sorted(t_point_list, key=lambda x: x[0]) 

            print(f"{t_point_list} return")
            return t_point_list

        l_pointlist = self.__garbage(t_point_list[0: split])
        print("finish left")
        r_pointlist = self.__garbage(t_point_list[split:])
        print("finish right")

        # Merge
        print("Merge")
        l_point = l_pointlist[0]
        for r_point in r_pointlist:
            hyperplane = self.__perpendicular(l_point, r_point)
            inters = self.__line_intersection(hyperplane, self.polyedge_list[0])

            hyper_part1 = [hyperplane[0], inters]
            hyper_part2 = [inters, hyperplane[1]]
            check1 = self.__line_intersection(hyper_part1, [l_point, r_point])
            check2 = self.__line_intersection(hyper_part2, [l_point, r_point])

            if(check1):
                hyperplane = hyper_part1
            elif(check2):
                hyperplane = hyper_part2


            self.polyedge_list.append(hyperplane)

    def __3p_force(self, points):
        points.sort()
        if_out = False
        if_exists = False
        s_point = 0
        dis_list = list()

        for i in range(len(points)):
            dis_list.append(math.dist(points[i], points[(i+1)%3]))
        
        s_point = (dis_list.index(max(dis_list)) + 1) % 3
        print(s_point, dis_list)

        
        l_ppdc = self.__perpendicular(points[s_point], points[(s_point + 1) % 3])
        r_ppdc = self.__perpendicular(points[(s_point + 1) % 3], points[(s_point + 2) % 3])
        inters = self.__line_intersection(l_ppdc, r_ppdc)

        def check(inters, line, point_list, type=0):
            line_part1 = [line[0], inters]
            line_part2 = [inters, line[1]]
            print(f"line_part1: {line_part1}, line_part2: {line_part2}")
            iters1 = self.__line_intersection(line_part1, point_list)
            # iters2 = self.__line_intersection(line_part2, point_list)

            if type == 0:
                return line_part1 if iters1 else line_part2
            elif type == 1:
                return line_part1 if not iters1 else line_part2

        if inters:
            if_exists = True
            l_ppdc = check(inters, l_ppdc, [points[s_point], points[(s_point + 1) % 3]])
            r_ppdc = check(inters, r_ppdc, [points[(s_point + 1) % 3], points[(s_point + 2) % 3]])
            m_ppdc = self.__perpendicular(points[s_point], points[(s_point - 1) % 3])
            
            if self.__line_intersection(l_ppdc, [points[s_point], points[(s_point - 1) % 3]]):
                if_out = True

            if not if_out:
                m_ppdc = check(inters, m_ppdc, [points[s_point], points[(s_point - 1) % 3]])
            else:
                m_ppdc = check(inters, m_ppdc, [points[s_point], points[(s_point - 1) % 3]], 1)
                
        def wb_record(ppdc, points):
            temp_dict = {'points': points,
                         'edge': ppdc}
            self.record.append(temp_dict)

        self.polyedge_list.append(l_ppdc)
        self.polypoints_list.append([points[s_point], points[(s_point + 1) % 3]])
        wb_record(l_ppdc, [points[s_point], points[(s_point + 1) % 3]])
        self.polyedge_list.append(r_ppdc)
        self.polypoints_list.append([points[(s_point + 1) % 3], points[(s_point + 2) % 3]])
        wb_record(r_ppdc, [points[(s_point + 1) % 3], points[(s_point + 2) % 3]])
        if if_exists:
            self.polyedge_list.append(m_ppdc)
            self.polypoints_list.append([points[s_point], points[(s_point - 1) % 3]])
            wb_record(m_ppdc, [points[s_point], points[(s_point - 1) % 3]])

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
                if [stable_x, result_y] not in ppdcline:
                    ppdcline.append([stable_x, result_y])

            stable_y = point
            try:
                const_n = (stable_y - midpoint[1]) / normal_vector[1]
                result_x = midpoint[0] + const_n * normal_vector[0]
            except ZeroDivisionError:
                result_x = -1

            # print(f"const_n: {const_n}, coord: {stable_y} {result_x}")
            if 0 <= stable_y <= 600 and 0 <= result_x <= 600:
                if [result_x, stable_y] not in ppdcline:
                    ppdcline.append([result_x, stable_y])

        ppdcline.sort(key=lambda x: x[1])
        print(f"ppdc: {a}, {b} --> {ppdcline}")
        return ppdcline

    def __line_intersection(self, line_a, line_b):
        geo_line1 = geo.LineString(line_a)
        geo_line2 = geo.LineString(line_b)
        print("intersection: ", geo_line1, geo_line2)

        if geo_line1.intersects(geo_line2):
            intersection = geo_line1.intersection(geo_line2)
            return [intersection.x, intersection.y]
        else:
            return None


if __name__ == '__main__':
    point_list = [[3, 8], [5, 4], [1, 6]]
    vd = VoronoiDiagram(point_list)
    print(vd.point_list)
