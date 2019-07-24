#!/usr/bin/env python3
import csv
from pathlib import Path
import re
from sys import stderr

DEST_DIR = Path('data', 'collated')
SRC_GHMIXR_PATH = Path('data', 'stashed', 'ghgases-fig-1a-ext.txt')
SRC_GISTEMPS_PATH = Path('data', 'stashed', 'gistemp-v3-fig-a.txt')
SRC_CO2MM_PATH = Path('data', 'stashed', 'co2_mm_mlo.txt')

SRC = {
    'ghmixr': Path('data', 'stashed', 'ghgases-fig-1a-ext.txt'),
    'gistemps': Path('data', 'stashed', 'gistemp-v3-fig-a.txt'),
    'co2mm': Path('data', 'stashed', 'co2_mm_mlo.txt'),
}




CO2MM = {
    'dest': DEST_DIR / 'co2-mm.csv',
    'headers': ('year', 'month', 'decimal_date', 'average', 'interpolated', 'trend', 'days'),
    'pattern': re.compile(r'^(\d{4}) +(1?\d) +(\d{4}\.\d+) +(-?\d+\.\d+) +(\d+\.\d+) +(\d+\.\d+) +(-1|\d{1,2})$', re.MULTILINE),
}

# the raw ghgases data two sets of data, lines 1-57ish, and lines 60+; we
#  want the top half
GH_MIXR_LINE_CUTOFF = 58
GH_MIXR_OBV = {
    'dest': DEST_DIR / 'ghgases-mixr-observed.csv',
    'headers': ('year', 'mixing_ratio'),
    'pattern': re.compile(r'(\b\d{4})  (\d{3}\.\d{1,2}\b)'),
}

GH_MIXR_ALT = {
    'dest': DEST_DIR / 'ghgases-mixr-future.csv',
    'headers': ('year', 'mixing_ratio'),
    'pattern': re.compile(r'(\b\d{4})  (\d{3}\.\d{1,2}\b)'),
}


GISTEMPS = {
    'dest': DEST_DIR / 'gistemp-v3-surface-air-temp-anomalies.csv',
    'headers': ('year', 'annual_mean_anomaly', '5_year_mean_anomaly'),
    'pattern': re.compile(r'^ +(\d{4}) +(-?\d+\.\d+) +(-?\d+\.\d+|\*) *$', re.MULTILINE),
}

# GISTEMPS_FIVEYR = {
#     'dest': DEST_DIR / 'gistemp-5yr-means.csv',
#     'headers': ('year', 'five_year_mean'),
#     'pattern': re.compile(r'^ +(\d{4}) .+?(-?\d+\.\d+) *$', re.MULTILINE),
# }





def collate(cfg, rawtext):
    """cfg is either the GISTEMPS_FIVEYR or GISTEMPS_ANNUAL or GHGASES dict"""

    stderr.write("Read {} chars ({} lines)\n".format(len(rawtext), len(rawtext.splitlines())))
    data = re.findall(cfg['pattern'], rawtext)
    with open(cfg['dest'], 'w') as w:
        c = csv.writer(w)
        c.writerow(cfg['headers'])
        c.writerows(sorted(data))

    stderr.write("Wrote {} rows to: {}\n".format(len(data), cfg['dest']))


def collate_co2mm():
    txt = SRC['co2mm'].read_text()

    collate(CO2MM, txt)


def collate_gistemps():
    txt = SRC['gistemps'].read_text()

    collate(GISTEMPS, txt)

def collate_gh_mixing_ratios():

    _t = SRC['ghmixr'].read_text()

    _lines = _t.splitlines()[0:GH_MIXR_LINE_CUTOFF]
    txt = "\n".join(_lines)
    collate(GH_MIXR_OBV, txt)

    _lines = _t.splitlines()[GH_MIXR_LINE_CUTOFF:]
    txt = "\n".join(_lines)
    collate(GH_MIXR_ALT, txt)



if __name__ == '__main__':
    stderr.write("\nCollating\n=========\n")
    DEST_DIR.mkdir(exist_ok=True, parents=True)

    stderr.write("\n- the co2 mm data...\n")
    collate_co2mm()

    stderr.write("\n- the historical co2 data...\n")
    collate_gh_mixing_ratios()

    stderr.write("\n- the gistemps data...\n")
    collate_gistemps()

