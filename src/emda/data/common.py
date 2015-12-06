from sys import float_info
from decimal import Decimal

def getFeatureInfo(fin, desc):
    features = desc['features']
    cntFeatures = len(features)

    mins = [float_info.max for i in range(cntFeatures)]
    maxs = [float_info.min for i in range(cntFeatures)]
    cnts = [0 for i in range(cntFeatures)]
    sums = [0 for i in range(cntFeatures)]
    
    while True:
        l = fin.readline().strip()
        if len(l) == 0:
            break
        feature = [i.strip() for i in l.split(',')]
        for i in range(cntFeatures):
            feature[i] = eval(feature[i])
            try:
                sums[i] = sums[i] + feature[i]
                if feature[i] < mins[i]:
                    mins[i] = feature[i]
                if feature[i] > maxs[i]:
                    maxs[i] = feature[i]
                cnts[i] = cnts[i] + 1
            except TypeError, err:
                #print 'debug[25] err = %s' % err
                #print 'debug[28]', feature[i], maxs[i]
                #raw_input()
                pass
    return (mins, maxs, cnts, sums)

def normalize(value, maxValue, minValue):
    if maxValue == minValue:
        return 1.0
    else:
        return float(value - minValue) /  (maxValue - minValue)

def dummy(value, maxValue, minValue, cntBox, isFromMax):
    if maxValue == minValue:
        lst = [1 for i in range(cntBox)]
    else:
        intercept = float(maxValue - minValue) / cntBox
        lst = [0 for i in range(cntBox)]
        idx = int((value - minValue) / intercept)
        #print 'debug[48] value = %f, maxValue = %f, minValue = %f, intercept = %f, idx = %d' % (value, maxValue, minValue, intercept, idx)

        for i in range(cntBox):
            if i <= idx and not isFromMax:
                lst[i] = 1
            if i >= idx and isFromMax:
                lst[i] = 1
    return lst

def FormatString(src, simbol, string):
    cntString = len(string)
    i = 0
    while i < cntString:
        if string[i] == simbol:
            start = i + 2
            end = start
            while end < cntString and string[end] != '}':
                end = end + 1
            idx = int(string[start:end])
            target = str(src[idx])
            string = string[0:i] + target + string[end+1:]
            i = i + len(target) - 1
        cntString = len(string)
        i = i + 1
    return string       
