import math
from os import write
import re
from shapely import geometry as geo


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


class Bisector:
    def __init__(self, point_a, point_b, p_bisector):
        self.p = (point_a, point_b)
        self.line = p_bisector


class VoronoiDiagram:
    def __init__(self, point_list):
        self.point_list = sorted(point_list)
        # self.point_list = point_list
        self.record = list()
        self.polyedge_list = list()     # for final result
        self.polypoints_list = list()   # for final result

        self.run()

    def run(self, type=0):
        print("Start")

        # if len(self.point_list) == 1:
        #     temp_dict = {'points': self.point_list,
        #                  'edge': [[-1, -1], [-1, 1]]}
        #     self.record.append(temp_dict)

        # elif len(self.point_list) == 2:
        #     ppdc = self.__p_bisector(*self.point_list)
        #     self.polyedge_list.append(ppdc)
        #     self.polypoints_list.append(self.point_list)
        #     temp_dict = {'points': self.point_list, 'edge': ppdc}
        #     self.record.append(temp_dict)

        self.__force(self.point_list)

    def __garbage(self, point_list):
        # This can only be used in the case of three points.
        print(point_list)
        split = int(len(point_list)/2)
        hyperplane_list = list()

        if len(point_list) <= 1:
            print(f"{point_list} return")
            return point_list

        elif len(point_list) == 2:
            self.polyedge_list.append(
                self.__p_bisector(point_list[0], point_list[1]))
            self.polypoints_list.append([point_list[0], point_list[1]])

            # point_list = sorted(point_list, key=lambda x: x[0])

            print(f"{point_list} return")
            return point_list

        l_pointlist = self.__garbage(point_list[0: split])
        print("finish left")
        r_pointlist = self.__garbage(point_list[split:])
        print("finish right")

        # Merge
        print("Merge")
        l_point = l_pointlist[0]
        for r_point in r_pointlist:
            hyperplane = self.__p_bisector(l_point, r_point)
            inters = self.__line_intersection(
                hyperplane, self.polyedge_list[0])

            hyper_part1 = [hyperplane[0], inters]
            hyper_part2 = [inters, hyperplane[1]]
            check1 = self.__line_intersection(hyper_part1, [l_point, r_point])
            check2 = self.__line_intersection(hyper_part2, [l_point, r_point])

            if(check1):
                hyperplane = hyper_part1
            elif(check2):
                hyperplane = hyper_part2

            self.polyedge_list.append(hyperplane)

    def __force(self, point_list):
        s_index = 0
        dis_list = list()

        # TODO: check if need to merge
        if len(point_list) == 1:
            self.__writeback_record('n', point_list, None)
            return

        elif len(point_list) == 2:
            p_bisector = self.__p_bisector(*self.point_list)
            self.polyedge_list.append(p_bisector)
            self.polypoints_list.append(point_list)
            self.__writeback_record('n', point_list, p_bisector)
            return

        for i in range(len(point_list)):
            dis_list.append(math.dist(point_list[i], point_list[(i+1) % 3]))

        s_index = (dis_list.index(max(dis_list)) + 1) % 3
        point_list += point_list[:s_index]
        del point_list[0:s_index]

        def anti_clockwise(point_list):
            d = 0
            for i in range(1, len(point_list)):
                d += det(point_list[i-1], point_list[i])
            d += (det(point_list[-1], point_list[0]))
            if d < 0:
                point_list.reverse()
            return point_list

        point_list = anti_clockwise(point_list)
        l_p_bisector = self.__p_bisector(point_list[0], point_list[1])
        r_p_bisector = self.__p_bisector(point_list[1], point_list[2])
        circumcenter = self.__line_intersection(l_p_bisector, r_p_bisector)

        def write_back():
            self.polyedge_list.append(l_p_bisector)
            self.polypoints_list.append([point_list[0], point_list[1]])
            self.polyedge_list.append(r_p_bisector)
            self.polypoints_list.append([point_list[1], point_list[2]])

        if circumcenter:
            m_p_bisector = self.__p_bisector(point_list[2], point_list[0])

            l_p_bisector[0] = circumcenter
            r_p_bisector[0] = circumcenter
            m_p_bisector[0] = circumcenter
            write_back()
            self.polyedge_list.append(m_p_bisector)
            self.polypoints_list.append([point_list[2], point_list[0]])
            self.__writeback_record(
                'n', point_list, l_p_bisector, r_p_bisector, m_p_bisector)

        else:
            write_back()
            self.__writeback_record(
                'n', point_list, l_p_bisector, r_p_bisector)

    def __p_bisector(self, a, b):
        p_bisector = list()
        midpoint = [(a[0] + b[0])/2, (a[1] + b[1])/2]
        # vector = [a[0] - b[0], a[1] - b[1]]
        normal_vector = [b[1] - a[1], - (b[0] - a[0])]
        vector_extend = [i * 600 for i in normal_vector]
        print(f"{a} {b} {normal_vector} {vector_extend}")

        start_p = [midpoint[0] - vector_extend[0],
                   midpoint[1] - vector_extend[1]]
        end_p = [midpoint[0] + vector_extend[0],
                 midpoint[1] + vector_extend[1]]
        p_bisector = [start_p, end_p]

        print(f"bisector: {a}, {b} --> {p_bisector}")
        return p_bisector

    def __line_intersection(self, line_a, line_b):
        geo_line1 = geo.LineString(line_a)
        geo_line2 = geo.LineString(line_b)
        print("intersection: ", geo_line1, geo_line2)

        if geo_line1.intersects(geo_line2):
            intersection = geo_line1.intersection(geo_line2)
            if(0 <= intersection.x <= 600 and 0 <= intersection.y <= 600):
                return [intersection.x, intersection.y]
        return None

    # TODO:
    def __writeback_record(self, type, points, *lines):
        temp_dict = dict()
        temp_dict['type'] = type
        temp_dict['points'] = points
        temp_dict['edges'] = lines
        self.record.append(temp_dict)


if __name__ == '__main__':
    point_list = [[10, 20], [20, 40], [200, 400]]
    vd = VoronoiDiagram(point_list)
    print(vd.point_list)
