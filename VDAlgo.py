import math
import copy
import sys
from shapely import geometry as geo
from functools import cmp_to_key

INT_MIN = -sys.maxsize - 1


def orientation(p1, p2, p3):
    val = (float(p2[1] - p1[1]) * (p3[0] - p2[0])) - \
        (float(p2[0] - p1[0]) * (p3[1] - p2[1]))

    if val > 0:
        # Clockwise orientation
        return 1

    elif val < 0:
        # Counterclockwise orientation
        return -1

    elif val == 0:
        # Collinear orientation
        return 0


class ConvexHull:
    def __init__(self, point_list):
        self.point_list = point_list
        self.upper_tan = list()
        self.lower_tan = list()
        self.cvhull = list()
        self.mid_point = [0] * 2

        for point in point_list:
            self.mid_point[0] += point[0]
            self.mid_point[1] += point[1]
        self.mid_point[0] /= len(point_list)
        self.mid_point[1] /= len(point_list)

        self.brute_cvhull()

    def __clockwise_compare(self, point1, point2):
        vec_p = [point1[0] - self.mid_point[0], point1[1] - self.mid_point[1]]
        vec_q = [point2[0] - self.mid_point[0], point2[1] - self.mid_point[1]]
        val = vec_p[1] * vec_q[0] - vec_q[1] * vec_p[0]

        if val > 0:
            return 1
        elif val == 0:
            return 0
        elif val < 0:
            return -1

    # Convex Hull Brute Force
    def brute_cvhull(self):
        if len(self.point_list) == 1:
            self.cvhull.append(self.point_list[0])

        elif len(self.point_list) >= 2:
            print("convex hull >= 2 point")
            self.cvhull += self.point_list
            self.cvhull.sort(key=cmp_to_key(self.__clockwise_compare))


def convex_hull_merge(hull_a: ConvexHull, hull_b: ConvexHull) -> ConvexHull:
    print(f"Start to merge the Convex Hull: {hull_a.cvhull} {hull_b.cvhull}")
    size_a = len(hull_a.cvhull)
    size_b = len(hull_b.cvhull)
    upper_done = False
    lower_done = False
    ret_hull = list()
    ind_a = hull_a.cvhull.index(max(hull_a.cvhull, key=lambda x: x[0]))
    ind_b = hull_b.cvhull.index(min(hull_b.cvhull, key=lambda x: x[0]))

    # upper tangent
    upper_a = ind_a
    upper_b = ind_b
    while not upper_done:
        upper_done = True
        while orientation(hull_b.cvhull[upper_b],
                          hull_a.cvhull[upper_a], hull_a.cvhull[(upper_a + 1) % size_a]) > 0:
            upper_a = (upper_a + 1) % size_a

        while orientation(hull_a.cvhull[upper_a],
                          hull_b.cvhull[upper_b], hull_b.cvhull[(upper_b - 1) % size_b]) < 0:
            upper_b = (upper_b - 1) % size_b
            upper_done = False

    hull_a.upper_tan = [hull_b.cvhull[upper_b], hull_a.cvhull[upper_a]]
    print("hull a upper tangent: ", hull_a.upper_tan)

    # lower tangent
    lower_a = ind_a
    lower_b = ind_b
    while not lower_done:
        lower_done = True
        while orientation(hull_a.cvhull[lower_a],
                          hull_b.cvhull[lower_b], hull_b.cvhull[(lower_b + 1) % size_b]) > 0:
            lower_b = (lower_b + 1) % size_b

        while orientation(hull_b.cvhull[lower_b],
                          hull_a.cvhull[lower_a], hull_a.cvhull[(lower_a - 1) % size_a]) < 0:
            lower_a = (lower_a - 1) % size_a
            lower_done = False

    hull_a.lower_tan = [hull_a.cvhull[lower_a], hull_b.cvhull[lower_b]]
    print("hull lower tangent: ", hull_a.lower_tan)

    ind = upper_a
    ret_hull.append(hull_a.cvhull[ind])
    while ind != lower_a:
        ind = (ind + 1) % size_a
        ret_hull.append(hull_a.cvhull[ind])

    ind = lower_b
    ret_hull.append(hull_b.cvhull[ind])
    while(ind != upper_b):
        ind = (ind + 1) % size_b
        ret_hull.append(hull_b.cvhull[ind])
    # ret_hull.append(ret_hull[0])

    hull_a.cvhull = ret_hull.copy()
    return hull_a


class VoronoiDiagram:
    def __init__(self, point_list):
        self.point_list = sorted(point_list)
        self.record = list()
        self.polyedge_list = list()     # for final result
        self.polypoints_list = list()   # for final result
        self.convex_hull_list = list()
        self.hyperplane_list = list()

        self.run()

    def run(self, type=0):
        print("Start:", self.point_list)
        self.__garbage(self.point_list)

    def __garbage(self, point_list):
        print("Divided:", point_list)
        split = int(len(point_list)/2)
        l_pointlist = point_list[0: split]
        r_pointlist = point_list[split:]

        # Brute Fore
        if len(point_list) <= 3:
            ret_cvhull = ConvexHull(point_list)
            self.convex_hull_list = (
                ret_cvhull.cvhull + [ret_cvhull.cvhull[0]]).copy()
            self.__writeback_record('c', False, point_list)
            self.__brute_vd(point_list)
            # ret_cvhull.brute_cvhull()

            return ret_cvhull

        # Get the ret_cvhull from conquer
        l_cvhull = self.__garbage(l_pointlist)
        print("finish left:", l_pointlist)
        r_cvhull = self.__garbage(r_pointlist)
        print("finish right:", r_pointlist)

        # Merge
        print(f"Merge: l: {l_pointlist}, r: {r_pointlist}")
        ret_cvhull = convex_hull_merge(l_cvhull, r_cvhull)
        self.convex_hull_list = ret_cvhull.cvhull.copy()
        self.__writeback_record('c', True, point_list)

        # Hyperplane
        self.__hyperplane(ret_cvhull)
        self.__writeback_record('h', False, [])
        self.__writeback_record('n', True, [])

        return ret_cvhull

    def __brute_vd(self, point_list):
        s_index = 0
        dis_list = list()

        # 1 point case
        if len(point_list) == 1:
            self.__writeback_record('n', False, point_list)
            return

        # 2 points case
        elif len(point_list) == 2:
            p_bisector = self.__p_bisector(*point_list)
            self.polyedge_list.append(p_bisector)
            self.polypoints_list.append(point_list)
            self.__writeback_record('n', False, point_list)
            return

        # 3 points case
        for i in range(len(point_list)):
            dis_list.append(math.dist(point_list[i], point_list[(i+1) % 3]))

        s_index = (dis_list.index(max(dis_list)) + 1) % 3
        point_list += point_list[:s_index]
        del point_list[0:s_index]

        # point_list = anti_clockwise(point_list)
        if orientation(*point_list) == 1:  # if it is clockwise
            point_list.reverse()
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
            self.__writeback_record('n', False, point_list)

        else:
            write_back()
            self.__writeback_record('n', False, point_list)

        return

    def __p_bisector(self, a, b):
        p_bisector = list()
        midpoint = [(a[0] + b[0])/2, (a[1] + b[1])/2]
        # vector = [a[0] - b[0], a[1] - b[1]]
        normal_vector = [b[1] - a[1], - (b[0] - a[0])]
        vector_extend = [i * 600 for i in normal_vector]

        start_p = [midpoint[0] - vector_extend[0],
                   midpoint[1] - vector_extend[1]]
        end_p = [midpoint[0] + vector_extend[0],
                 midpoint[1] + vector_extend[1]]
        p_bisector = [start_p, end_p]

        print(f"bisector: {a}, {b} --> {p_bisector}")
        return p_bisector

    def __line_intersection(self, line_a, line_b, h=0):
        if line_a == line_b:
            return None
        geo_line1 = geo.LineString(line_a)
        geo_line2 = geo.LineString(line_b)
        print("intersection: ", geo_line1, geo_line2, end=" - ")

        if geo_line1.intersects(geo_line2):
            intersection = geo_line1.intersection(geo_line2)
            if (0 <= intersection.x <= 600 and 0 <= intersection.y <= 600) or h == 1:
                print([intersection.x, intersection.y])
                return [intersection.x, intersection.y]
        print("None")
        return None

    def __hyperplane(self, cvhull: ConvexHull):
        l_cur_point = list()
        r_cur_point = list()
        hyperplane = self.__p_bisector(*cvhull.upper_tan)
        # Sort by y, make sure the hyperplane can go down
        hyperplane.sort(reverse=True, key=lambda x: x[1])
        r_cur_point = cvhull.upper_tan[0].copy()
        l_cur_point = cvhull.upper_tan[1].copy()
        l_next_point = list()
        r_next_point = list()
        l_prev_checked = -1
        r_prev_checked = -1
        temp_polypoint_list = list()
        temp_polyedge_list = list()

        while l_cur_point != cvhull.lower_tan[0] or r_cur_point != cvhull.lower_tan[1]:
            l_highest_inters = [0, INT_MIN]
            r_highest_inters = [0, INT_MIN]
            l_line_ind = None
            r_line_ind = None
            l_line_set = list()
            r_line_set = list()

            for points in self.polypoints_list:
                temp_idx = self.polypoints_list.index(points)
                if l_cur_point in points and temp_idx != l_prev_checked:
                    l_line_set.append(temp_idx)

                if r_cur_point in points and temp_idx != r_prev_checked:
                    r_line_set.append(temp_idx)

            # Find the highest intersection between the hyperplane and the lines beside the point
            for ind in l_line_set:
                check_line = self.polyedge_list[ind]
                hyper_inters = self.__line_intersection(
                    hyperplane[-2:], check_line, h=1)
                if hyper_inters:
                    if hyper_inters[1] > l_highest_inters[1]:
                        l_highest_inters = hyper_inters.copy()
                        l_next_point = self.polypoints_list[ind][0].copy() \
                            if self.polypoints_list[ind][0] != l_cur_point else self.polypoints_list[ind][1].copy()
                        l_line_ind = ind

            for ind in r_line_set:
                check_line = self.polyedge_list[ind]
                hyper_inters = self.__line_intersection(
                    hyperplane[-2:], check_line, h=1)
                if hyper_inters:
                    if hyper_inters[1] > r_highest_inters[1]:
                        r_highest_inters = hyper_inters.copy()
                        r_next_point = self.polypoints_list[ind][0].copy() \
                            if self.polypoints_list[ind][0] != r_cur_point else self.polypoints_list[ind][1]
                        r_line_ind = ind

            temp_polypoint_list.append([l_cur_point, r_cur_point])
            hyperplane.pop()

            # Judge the relation between the hyperplane and the lines
            if l_highest_inters == r_highest_inters:
                hyperplane.append(l_highest_inters)

                cut_checked = orientation(
                    hyperplane[-2], hyperplane[-1], self.polyedge_list[l_line_ind][0])
                if cut_checked == 1:
                    self.polyedge_list[l_line_ind][1] = l_highest_inters.copy()
                else:
                    self.polyedge_list[l_line_ind][0] = l_highest_inters.copy()

                cut_checked = orientation(
                    hyperplane[-2], hyperplane[-1], self.polyedge_list[r_line_ind][0])
                if cut_checked == -1:
                    self.polyedge_list[r_line_ind][1] = r_highest_inters.copy()
                else:
                    self.polyedge_list[r_line_ind][0] = r_highest_inters.copy()

                l_cur_point = l_next_point.copy()
                l_prev_checked = l_line_ind
                l_line_set.remove(l_line_ind)

                for idx in l_line_set:
                    checked_s = orientation(
                        hyperplane[-2], hyperplane[-1], self.polyedge_list[idx][0])
                    checked_e = orientation(
                        hyperplane[-2], hyperplane[-1], self.polyedge_list[idx][1])
                    if checked_s == checked_e and checked_s == -1:
                        self.polyedge_list.pop(idx)
                        self.polypoints_list.pop(idx)
                # l_ending()

                r_cur_point = r_next_point.copy()
                r_prev_checked = r_line_ind
                r_line_set.remove(r_line_ind)

                for idx in r_line_set:
                    checked_s = orientation(
                        hyperplane[-2], hyperplane[-1], self.polyedge_list[idx][0])
                    checked_e = orientation(
                        hyperplane[-2], hyperplane[-1], self.polyedge_list[idx][1])
                    if checked_s == checked_e and checked_s == -1:
                        self.polyedge_list.pop(idx)
                        self.polypoints_list.pop(idx)
                # r_ending()

            elif l_highest_inters[1] > r_highest_inters[1]:
                hyperplane.append(l_highest_inters)

                cut_checked = orientation(
                    hyperplane[-2], hyperplane[-1], self.polyedge_list[l_line_ind][0])
                if cut_checked == 1:
                    self.polyedge_list[l_line_ind][1] = l_highest_inters.copy()
                else:
                    self.polyedge_list[l_line_ind][0] = l_highest_inters.copy()

                l_cur_point = l_next_point.copy()
                l_prev_checked = l_line_ind
                r_prev_checked = -1
                l_line_set.remove(l_line_ind)

                for idx in l_line_set:
                    checked_s = orientation(
                        hyperplane[-2], hyperplane[-1], self.polyedge_list[idx][0])
                    checked_e = orientation(
                        hyperplane[-2], hyperplane[-1], self.polyedge_list[idx][1])
                    if checked_s == checked_e and checked_s == -1:
                        self.polyedge_list.pop(idx)
                        self.polypoints_list.pop(idx)
                # l_ending()

            elif l_highest_inters[1] < r_highest_inters[1]:
                hyperplane.append(r_highest_inters)

                cut_checked = orientation(
                    hyperplane[-2], hyperplane[-1], self.polyedge_list[r_line_ind][0])
                if cut_checked == -1:
                    self.polyedge_list[r_line_ind][1] = r_highest_inters.copy()
                else:
                    self.polyedge_list[r_line_ind][0] = r_highest_inters.copy()

                r_cur_point = r_next_point.copy()
                l_prev_checked = -1
                r_prev_checked = r_line_ind
                r_line_set.remove(r_line_ind)

                for idx in r_line_set:
                    checked_s = orientation(
                        hyperplane[-2], hyperplane[-1], self.polyedge_list[idx][0])
                    checked_e = orientation(
                        hyperplane[-2], hyperplane[-1], self.polyedge_list[idx][1])
                    if checked_s == checked_e and checked_s == 1:
                        self.polyedge_list.pop(idx)
                        self.polypoints_list.pop(idx)
                # r_ending()

            temp_hyper = self.__p_bisector(l_cur_point, r_cur_point)
            temp_hyper.sort(reverse=True, key=lambda x: x[1])
            temp_polyedge_list.append(hyperplane[-2:])
            hyperplane.append(temp_hyper[1])

        temp_polypoint_list.append([l_cur_point, r_cur_point])
        temp_polyedge_list.append(hyperplane[-2:])
        print(f"hyperplane: {hyperplane}")
        self.hyperplane_list = hyperplane.copy()
        self.polypoints_list += temp_polypoint_list
        self.polyedge_list += temp_polyedge_list

    def __writeback_record(self, type, clean, points):
        temp_dict = dict()
        temp_dict['type'] = type
        temp_dict['clean'] = clean
        temp_dict['points'] = points

        if type == 'n':
            temp_dict['edges'] = copy.deepcopy(self.polyedge_list)
        elif type == 'c':
            temp_dict['edges'] = copy.deepcopy(self.convex_hull_list)
        elif type == 'h':
            temp_dict['edges'] = copy.deepcopy(self.hyperplane_list)

        self.record.append(temp_dict)


if __name__ == '__main__':
    point_list_a = [[5, 3], [4, 8], [7, 6]]
    point_list_b = [[9, 8], [10, 2], [12, 6]]

    vd = VoronoiDiagram(point_list_a)
    print("main: ", vd.polyedge_list)

    # ch = ConvexHull(point_list_a)
    # print(ch.point_list)
    # print(max(point_list_a, key=lambda x: x[0]))
    # orientation(*ch.point_list)

    # hull_a = ConvexHull(point_list_a)
    # print(hull_a.cvhull)
    # hull_b = ConvexHull(point_list_b)
    # print(hull_b.cvhull)
    # out_hull = convex_hull_merge(hull_a, hull_b)

    # print(out_hull.cvhull)
