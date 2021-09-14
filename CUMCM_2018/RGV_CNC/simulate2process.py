# The followig codes are for the simulation of two processes production
from CNC import CNC
from rgv import RGV2


def sea_info(cnc_list):
    """找出当前发出信号的所有CNC，并记录故障机器"""
    cnc_loc_list = []
    error_cnc_list = []
    for cnc_call in cnc_list:
        cnc_stat = cnc_call.call_rgv()
        if cnc_stat[1] in ['off', 'empty']:
            cnc_loc_list.append(cnc_stat)
        elif cnc_stat[1] == 'error':
            error_cnc_list.append(cnc_stat[0])

    return cnc_loc_list, error_cnc_list

delta_time = 1     # RGV扫描频率，模拟实时
duration = 8 * 60 * 60
repairing_time = 15 * 60

# CNC装的刀片情况
cncProcess1 = [1, 3, 5, 7]
cncProcess2 = [2, 4, 6, 8]
# cncProcess1 = [1, 3, 5]
# cncProcess2 = [2, 4, 6, 7, 8]
# cncProcess1 = [1, 4, 5, 7, 8]
# cncProcess2 = [2, 3, 6]

# CNC是否会出故障
usedCase3 = False
# usedCase3 = True

# 第1组，依顺序对应
t1 = 20
t2 = 33
t3 = 46
t4 = 560
t5 = 400
t6 = 500
t7 = 28
t8 = 31
t9 = 25
# 第2组
# t1 = 23
# t2 = 41
# t3 = 59
# t4 = 580
# t5 = 280
# t6 = 500
# t7 = 30
# t8 = 35
# t9 = 30
# 第3组
# t1 = 18
# t2 = 32
# t3 = 46
# t4 = 545
# t5 = 455
# t6 = 182
# t7 = 27
# t8 = 32
# t9 = 25

cncList = [CNC('CNC' + str(i)) for i in range(1, 9)]
rgv = RGV2(t1, t2, t3, t7, t8, t9, cncProcess1, cncProcess2)

t = 0   # 记录时刻
n = 0   # 记录加工物件序号

while t < duration:
    cncLocList, errorCNC = sea_info(cncList)
    errorCncList = [cncList[int(name[-1])-1] for name in errorCNC]    # 对象
    if cncLocList:
        calling_cnc = [cnc_calling[0] for cnc_calling in cncLocList]    # CNC's name
        calling_cnc = [cncList[int(name[-1])-1] for name in calling_cnc]    # 对象
        rgv_delta, rgvMovingDelta, cncName, processID = rgv.run(cncLocList)
        if processID != 0:
            cncProcessed = cncList[int(cncName[-1])-1]    # RGV本次处理的CNC
            if usedCase3:
                if processID == 1:
                    errorOccur = cncProcessed.processing(0, t5, case3=True)
                else:
                    errorOccur = cncProcessed.processing(0, t6, case3=True)

                if errorOccur:
                    cncProcessed.error_repairing(0, repairing_time)
                    print(n, cncName, t + rgvMovingDelta, 'Error')
                    t += rgv_delta
                else:
                    if processID == 1:
                        n += 1
                        print(n, cncName, t + rgvMovingDelta)
                    else:
                        print('None', cncName, t + rgvMovingDelta)

                    t += rgv_delta
            else:
                if processID == 1:
                    cncProcessed.processing(0, t5)
                    n += 1
                    print(n, cncName, t + rgvMovingDelta)
                else:
                    cncProcessed.processing(0, t6)
                    print('None', cncName, t + rgvMovingDelta)

                t += rgv_delta

            for cncProcessing in cncList:
                cncNum = cncList.index(cncProcessing) + 1
                if (cncProcessing not in calling_cnc) and (cncProcessing not in errorCncList):    # 正在运行的CNC
                    if cncNum in cncProcess1:
                        cncProcessing.processing(rgv_delta, t5)
                    else:
                        cncProcessing.processing(rgv_delta, t6)
                elif cncProcessing in errorCncList:   # 故障中的CNC
                    cncProcessing.error_repairing(rgv_delta, repairing_time)

        else:
            for cnc in cncList:
                if cnc not in calling_cnc:
                    cncNum = cncList.index(cnc) + 1
                    if cnc not in errorCNC:  # 该CNC未故障
                        if cncNum in cncProcess1:
                            cnc.processing(delta_time, t5)
                        else:
                            cnc.processing(delta_time, t6)
                    else:
                        cnc.error_repairing(delta_time, repairing_time)

            t += delta_time

    else:   # 所有未故障的CNC都在加工
        for cnc in cncList:
            cncNum = cncList.index(cnc) + 1
            if cnc not in errorCNC:     # 该CNC未故障
                if cncNum in cncProcess1:
                    cnc.processing(delta_time, t5)
                else:
                    cnc.processing(delta_time, t6)
            else:
                cnc.error_repairing(delta_time, repairing_time)

        t += delta_time
