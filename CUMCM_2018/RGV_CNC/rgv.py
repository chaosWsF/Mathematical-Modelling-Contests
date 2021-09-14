import numpy as np


def find_cnc_loc(code):
    """get CNC's location"""
    if code in [1, 2]:
        cnc_loc = 0
    elif code in [3, 4]:
        cnc_loc = 1
    elif code in [5, 6]:
        cnc_loc = 2
    else:
        cnc_loc = 3
    return cnc_loc


def rgv_cnc(cnc_name_list, rgv_loc):
    """For the one-process production, get the distance between RGV and each CNC, which means RGV subtracts CNC
    at the same time, returns the best choice among CNCs in index form"""
    d_list = []
    for name in cnc_name_list:
        code = int(name[-1])
        cnc_loc = find_cnc_loc(code)
        d = rgv_loc - cnc_loc
        d_list.append(d)

    d_array = np.array(d_list)
    if rgv_loc == 0:
        if 'CNC1' in cnc_name_list:
            index_num = cnc_name_list.index('CNC1')
        elif 'CNC2' in cnc_name_list:
            index_num = cnc_name_list.index('CNC2')
        else:
            index_num = d_list.index(max(d_list))

    elif rgv_loc == 1:
        if 0 in d_array:
            if 'CNC3' in cnc_name_list:
                index_num = cnc_name_list.index('CNC3')
            else:
                index_num = cnc_name_list.index('CNC4')
        elif (d_array > 0).all():
            if 'CNC1' in cnc_name_list:
                index_num = cnc_name_list.index('CNC1')
            else:
                index_num = cnc_name_list.index('CNC2')
        elif (d_array < 0).all():
            index_num = d_list.index(max(d_list))
        else:
            if len(np.unique(d_array)) == 3:
                if 'CNC1' in cnc_name_list:
                    index_num = cnc_name_list.index('CNC1')
                else:
                    index_num = cnc_name_list.index('CNC2')
            else:
                if 'CNC1' in cnc_name_list:
                    index_num = cnc_name_list.index('CNC1')
                elif 'CNC5' in cnc_name_list:
                    index_num = cnc_name_list.index('CNC5')
                else:
                    index_num = cnc_name_list.index('CNC2')

    elif rgv_loc == 2:
        if 0 in d_array:
            if 'CNC5' in cnc_name_list:
                index_num = cnc_name_list.index('CNC5')
            else:
                index_num = cnc_name_list.index('CNC6')
        elif (d_array > 0).all():
            index_num = d_list.index(min(d_list))
        elif (d_array < 0).all():
            if 'CNC7' in cnc_name_list:
                index_num = cnc_name_list.index('CNC7')
            else:
                index_num = cnc_name_list.index('CNC8')
        else:
            if len(np.unique(d_array)) == 3:
                if 'CNC7' in cnc_name_list:
                    index_num = cnc_name_list.index('CNC7')
                else:
                    index_num = cnc_name_list.index('CNC8')
            else:
                if 'CNC7' in cnc_name_list:
                    index_num = cnc_name_list.index('CNC7')
                elif 'CNC3' in cnc_name_list:
                    index_num = cnc_name_list.index('CNC3')
                else:
                    index_num = cnc_name_list.index('CNC8')

    else:
        if 'CNC7' in cnc_name_list:
            index_num = cnc_name_list.index('CNC7')
        elif 'CNC8' in cnc_name_list:
            index_num = cnc_name_list.index('CNC8')
        else:
            index_num = d_list.index(min(d_list))

    return d_list, index_num


def moving_time(code, rgv_loc, move1, move2, move3):
    d = abs(rgv_loc - find_cnc_loc(code))
    if d == 1:
        return move1
    elif d == 2:
        return move2
    elif d == 3:
        return move3
    else:
        return 0


class RGV:
    def __init__(self, t1, t2, t3, t7, t8, t9):
        self.cur_position = 0
        self.move1_time = t1
        self.move2_time = t2
        self.move3_time = t3
        self.odd_cnc_time = t7
        self.even_cnc_time = t8
        self.clean_time = t9

    def run(self, cnc_loc_list):
        """移动所需时间 + 上下料时间 + 清洗时间（有或无）"""
        cnc_stat_list = []
        cnc_name_list = []
        for c in cnc_loc_list:
            cnc_name_list.append(c[0])
            cnc_stat_list.append(c[1])
        distance_list, i = rgv_cnc(cnc_name_list, self.cur_position)
        cnc_name = cnc_name_list[i]
        cnc_code = int(cnc_name[-1])
        cnc_stat = cnc_stat_list[i]
        d = abs(distance_list[i])

        if cnc_stat == 'off':
            rgv_delta = self.clean_time
            if d == 1:
                rgv_delta += self.move1_time
                rgv_moving_delta = self.move1_time
                if cnc_code % 2 == 0:
                    rgv_delta += self.even_cnc_time
                else:
                    rgv_delta += self.odd_cnc_time
            elif d == 2:
                rgv_delta += self.move2_time
                rgv_moving_delta = self.move2_time
                if cnc_code % 2 == 0:
                    rgv_delta += self.even_cnc_time
                else:
                    rgv_delta += self.odd_cnc_time
            elif d == 3:
                rgv_delta += self.move3_time
                rgv_moving_delta = self.move3_time
                if cnc_code % 2 == 0:
                    rgv_delta += self.even_cnc_time
                else:
                    rgv_delta += self.odd_cnc_time
            else:
                rgv_moving_delta = 0
                if cnc_code % 2 == 0:
                    rgv_delta += self.even_cnc_time
                else:
                    rgv_delta += self.odd_cnc_time
        else:
            rgv_delta = 0
            if d == 1:
                rgv_delta += self.move1_time
                rgv_moving_delta = self.move1_time
                if cnc_code % 2 == 0:
                    rgv_delta += self.even_cnc_time
                else:
                    rgv_delta += self.odd_cnc_time
            elif d == 2:
                rgv_delta += self.move2_time
                rgv_moving_delta = self.move2_time
                if cnc_code % 2 == 0:
                    rgv_delta += self.even_cnc_time
                else:
                    rgv_delta += self.odd_cnc_time
            elif d == 3:
                rgv_delta += self.move3_time
                rgv_moving_delta = self.move3_time
                if cnc_code % 2 == 0:
                    rgv_delta += self.even_cnc_time
                else:
                    rgv_delta += self.odd_cnc_time
            else:
                rgv_moving_delta = 0
                if cnc_code % 2 == 0:
                    rgv_delta += self.even_cnc_time
                else:
                    rgv_delta += self.odd_cnc_time

        self.cur_position = find_cnc_loc(cnc_code)
        return rgv_delta, rgv_moving_delta, cnc_name


class RGV2:
    def __init__(self, t1, t2, t3, t7, t8, t9, process1_id, process2_id):
        self.cur_position = 0
        self.move1_time = t1
        self.move2_time = t2
        self.move3_time = t3
        self.odd_cnc_time = t7
        self.even_cnc_time = t8
        self.clean_time = t9
        self.id1 = process1_id
        self.id2 = process2_id
        self.holding = 0    # RGV是否持有半成品，持有为1

    def run(self, cnc_loc_list):
        """移动所需时间 + 上下料时间 + 清洗时间（有或无）"""
        cnc_stat_list = []
        cnc_name_list = []
        cnc_name_list_id1 = []
        cnc_name_list_id2 = []
        for c in cnc_loc_list:
            ccode = int(c[0][-1])
            cnc_stat_list.append(c[1])
            cnc_name_list.append(c[0])
            if ccode in self.id1:
                cnc_name_list_id1.append(c[0])
            else:
                cnc_name_list_id2.append(c[0])

        if len(cnc_name_list_id1) + len(cnc_name_list_id2) == 1:
            if len(cnc_name_list_id1) == 1:
                if self.holding == 0:
                    cnc_name = cnc_name_list_id1[0]
                    process_id = 1
                    cnc_code = int(cnc_name[-1])
                    cnc_stat = cnc_stat_list[cnc_name_list.index(cnc_name)]
                    if cnc_stat == 'off':
                        self.holding = 1
                    rgv_moving_delta = moving_time(cnc_code, self.cur_position, self.move1_time, self.move2_time, self.move3_time)
                    if cnc_code % 2 == 0:
                        rgv_delta = rgv_moving_delta + self.even_cnc_time
                    else:
                        rgv_delta = rgv_moving_delta + self.odd_cnc_time

                else:
                    cnc_name = 'CNC0'
                    process_id = 0
                    rgv_moving_delta = 0
                    rgv_delta = 0
            else:
                if self.holding == 1:
                    cnc_name = cnc_name_list_id2[0]
                    cnc_code = int(cnc_name[-1])
                    cnc_stat = cnc_stat_list[cnc_name_list.index(cnc_name)]
                    process_id = 2
                    self.holding = 0
                    rgv_moving_delta = moving_time(cnc_code, self.cur_position, self.move1_time, self.move2_time, self.move3_time)
                    if cnc_code % 2 == 0:
                        rgv_delta = rgv_moving_delta + self.even_cnc_time
                    else:
                        rgv_delta = rgv_moving_delta + self.odd_cnc_time
                    if cnc_stat == 'off':
                        rgv_delta += self.clean_time
                else:
                    rgv_delta = 0
                    rgv_moving_delta = 0
                    cnc_name = 'CNC0'
                    process_id = 0

        elif (len(cnc_name_list_id1) == 0) and (len(cnc_name_list_id2) > 1):
            if self.holding == 1:
                _, i = rgv_cnc(cnc_name_list_id2, self.cur_position)
                cnc_name = cnc_name_list_id2[i]
                process_id = 2
                self.holding = 0
                cnc_code = int(cnc_name[-1])
                cnc_stat = cnc_stat_list[cnc_name_list.index(cnc_name)]
                rgv_moving_delta = moving_time(cnc_code, self.cur_position, self.move1_time, self.move2_time, self.move3_time)
                if cnc_code % 2 == 0:
                    rgv_delta = rgv_moving_delta + self.even_cnc_time
                else:
                    rgv_delta = rgv_moving_delta + self.odd_cnc_time
                if cnc_stat == 'off':
                    rgv_delta += self.clean_time
            else:
                rgv_delta = 0
                rgv_moving_delta = 0
                cnc_name = 'CNC0'
                process_id = 0

        elif (len(cnc_name_list_id2) == 0) and (len(cnc_name_list_id1) > 1):
            if self.holding == 0:
                d_list, _ = rgv_cnc(cnc_name_list_id1, self.cur_position)
                d_array = np.array(d_list)
                i = np.argmin(np.abs(d_array))
                cnc_name = cnc_name_list_id1[i]
                process_id = 1
                cnc_code = int(cnc_name[-1])
                cnc_stat = cnc_stat_list[cnc_name_list.index(cnc_name)]
                if cnc_stat == 'off':
                    self.holding = 1
                rgv_moving_delta = moving_time(cnc_code, self.cur_position, self.move1_time, self.move2_time, self.move3_time)
                if cnc_code % 2 == 0:
                    rgv_delta = rgv_moving_delta + self.even_cnc_time
                else:
                    rgv_delta = rgv_moving_delta + self.odd_cnc_time

            else:
                cnc_name = 'CNC0'
                process_id = 0
                rgv_delta = 0
                rgv_moving_delta = 0
        else:
            if self.holding == 0:
                d_list, _ = rgv_cnc(cnc_name_list_id1, self.cur_position)
                d_array = np.array(d_list)
                i = np.argmin(np.abs(d_array))
                cnc_name = cnc_name_list_id1[i]
                process_id = 1
                cnc_code = int(cnc_name[-1])
                cnc_stat = cnc_stat_list[cnc_name_list.index(cnc_name)]
                if cnc_stat == 'off':
                    self.holding = 1
                rgv_moving_delta = moving_time(cnc_code, self.cur_position, self.move1_time, self.move2_time, self.move3_time)
                if cnc_code % 2 == 0:
                    rgv_delta = rgv_moving_delta + self.even_cnc_time
                else:
                    rgv_delta = rgv_moving_delta + self.odd_cnc_time

            else:
                d_list, _ = rgv_cnc(cnc_name_list_id2, self.cur_position)
                d_array = np.array(d_list)
                i = np.argmin(np.abs(d_array))
                cnc_name = cnc_name_list_id2[i]
                process_id = 2
                self.holding = 0
                cnc_code = int(cnc_name[-1])
                cnc_stat = cnc_stat_list[cnc_name_list.index(cnc_name)]
                rgv_moving_delta = moving_time(cnc_code, self.cur_position, self.move1_time, self.move2_time, self.move3_time)
                if cnc_code % 2 == 0:
                    rgv_delta = rgv_moving_delta + self.even_cnc_time
                else:
                    rgv_delta = rgv_moving_delta + self.odd_cnc_time
                if cnc_stat == 'off':
                    rgv_delta += self.clean_time

        if process_id != 0:
            cnc_code = int(cnc_name[-1])
            self.cur_position = find_cnc_loc(cnc_code)
        
        return rgv_delta, rgv_moving_delta, cnc_name, process_id
