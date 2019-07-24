##!/bin/sh

echo "Stashing"
echo "========"

mkdir -p data/stashed


# curl -Lo gistemp-v4-land-ocean.txt \
#     https://data.giss.nasa.gov/gistemp/graphs_v4/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt


echo "Downloading global temperature data (http://data.giss.nasa.gov/gistemp/graphs_v3/)"
curl -sLo data/stashed/gistemp-v3-fig-a.txt \
    http://data.giss.nasa.gov/gistemp/graphs_v3/Fig.A.txt


echo "Downloading historical greenhouse gases data (https://data.giss.nasa.gov/modelforce/ghgases)"
curl -sLo data/stashed/ghgases-fig-1a-ext.txt \
    https://data.giss.nasa.gov/modelforce/ghgases/Fig1A.ext.txt


echo "Downloading CO2 data (ftp://aftp.cmdl.noaa.gov/products/trends/co2/)"
curl -sLo data/stashed/co2_mm_mlo.txt \
    ftp://aftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.txt
