import csv


def task(fname):
    lstart, mstart = -1, -1
    size, msize = 0, 0
    lprev = 0
    dt, cdt, pdt, mdt = '', '', '', ''

    with open(fname) as csvf:
        rdr = csv.DictReader(csvf, delimiter=';')
        ii = 0
        for row in rdr:
            lcurr = int(row['luminosity'])
            cdt = row['date'] + ' ' + row['time']
            if lcurr <= lprev:
                if lstart == -1:
                    lstart = ii - 1
                    dt = pdt
                    size = 2
                else:
                    size += 1
            else:
                if size > msize:
                    mstart = lstart
                    msize = size
                    mdt = dt
                lstart = -1
                size = 0

            lprev = lcurr
            pdt = cdt
            ii += 1

    if size > msize:
        mstart = lstart
        msize = size
        mdt = dt

    return mstart, msize, mdt


start, length, date_time = task('alpha_oriona.csv')
with open('result.txt', 'w') as fout:
    fout.write(str(length) + '\n')
    fout.write(date_time)
