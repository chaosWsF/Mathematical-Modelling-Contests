
from CNC import CNC
from rgv import RGV


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

delta_time = 1
duration = 8 * 60 * 60
repairing_time = 15 * 60
usedCase3 = False
# usedCase3 = True

# 第1组
t1 = 20
t2 = 33
t3 = 46
t4 = 700
t5 = 400
t6 = 378
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
rgv = RGV(t1, t2, t3, t7, t8, t9)

t = 0
n = 0
while t < duration:
    cncLocList, errorCNC = sea_info(cncList)
    if cncLocList:
        calling_cnc = [cnc_calling[0] for cnc_calling in cncLocList]
        calling_cnc = [cncList[int(name[-1])-1] for name in calling_cnc]
        errorCncList = [cncList[int(name[-1])-1] for name in errorCNC]  # 对象
        rgv_delta, rgvMovingDelta, cncName = rgv.run(cncLocList)
        cncProcessed = cncList[int(cncName[-1])-1]    # RGV本次处理的CNC
        if usedCase3:
            errorOccur = cncProcessed.processing(0, t4, case3=True)
            if errorOccur:
                cncProcessed.error_repairing(0, repairing_time)
                print(n, cncName, t + rgvMovingDelta, 'Error')
                t += rgv_delta
            else:
                n += 1
                print(n, cncName, t + rgvMovingDelta)
                t += rgv_delta
        else:
            cncProcessed.processing(0, t4)
            n += 1
            print(n, cncName, t + rgvMovingDelta)
            t += rgv_delta

        for cncProcessing in cncList:
            if (cncProcessing not in calling_cnc) and (cncProcessing not in errorCncList):    # 正在运行的CNC
                cncProcessing.processing(rgv_delta, t4)
            elif cncProcessing in errorCncList:   # 故障中的CNC
                cncProcessing.error_repairing(rgv_delta, repairing_time)

    else:   # 所有未故障CNC都在加工
        t += delta_time
        for cnc in cncList:
            if cnc not in errorCNC:
                cnc.processing(delta_time, t4)
            else:
                cnc.error_repairing(delta_time, repairing_time)
