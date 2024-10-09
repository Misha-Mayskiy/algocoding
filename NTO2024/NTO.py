gribs_live = [4]
for hours in range(1, 25):
    for grib in range(len(gribs_live)):
        gribs_live[grib] -= 1
        if gribs_live[grib] == 0:
            gribs_live[grib] = 4
            gribs_live.append(10)
            gribs_live.append(10)
    print(hours, len(gribs_live), gribs_live)