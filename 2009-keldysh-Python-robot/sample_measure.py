maxLen = 1000
measureHistory = []

while True:
    measureHistory.append(GetNewMeasure())
    if len(measureHistory) > maxLen:
        measureHistory = measureHistory[-maxLen:]