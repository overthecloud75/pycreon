
def momentum(dataList, includeLastMonth=False):

    # data는 period + 1만큰의 data가 필요
    if includeLastMonth:
        growth = round((dataList[-1] - dataList[0])/dataList[0], 2)
    else:
        growth = round((dataList[-2] - dataList[0])/dataList[0], 2)
    return growth


