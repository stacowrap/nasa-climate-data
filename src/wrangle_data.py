#!/usr/bin/env python3
import csv
from pathlib import Path
from statistics import mean
from sys import stderr

DEST_PATH = Path('data', 'wrangled', 'nasa-co2-temps.csv')
SRC_DIR = Path('data', 'collated')
SRC = {
    'co2_new': SRC_DIR / 'co2-mm.csv',
    'co2_old': SRC_DIR / 'ghgases-mixr-observed.csv',
    'gistemps': SRC_DIR / 'gistemp-v3-surface-air-temp-anomalies.csv',
}

WRANGLED_HEADERS = ('year', 'surface_air_temp_anomaly', 'co2_ppm')


CO2_YEAR_SWITCH_FILE = '1959'


def wrangle():
    co2x = list(csv.DictReader(SRC['co2_old'].open()))
    co2y = list(csv.DictReader(SRC['co2_new'].open()))

    data = []
    for t in csv.DictReader(SRC['gistemps'].open()):
        row = {'year': t['year'],
               'surface_air_temp_anomaly': t['annual_mean_anomaly']}

        if row['year'] < CO2_YEAR_SWITCH_FILE:
            row['co2_ppm'] = next(z['mixing_ratio'] for z in co2x if z['year'] == row['year'])
        else:
            v = mean(float(z['interpolated']) for z in co2y if z['year'] == row['year'])
            row['co2_ppm'] = round(v, 1)

        data.append(row)

    return data


if __name__ == '__main__':
    stderr.write("\nWrangling\n=========\n")
    data = wrangle()
    stderr.write("Wrangled {} records\n".format(len(data)))

    DEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DEST_PATH, 'w') as w:
        outs = csv.DictWriter(w, fieldnames=WRANGLED_HEADERS)
        outs.writeheader()
        outs.writerows(data)

        stderr.write("Wrote {} wrangled records to: {}\n".format(len(data), DEST_PATH))

