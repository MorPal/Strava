from bs4 import BeautifulSoup as soup
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
import numpy as np
import datetime
from geopy.distance import great_circle

run = open('20170215-180917-Run.gpx', 'r')
parser = soup(run, "html.parser")

hr_ = parser.findAll("gpxtpx:hr")
time_ = parser.findAll("time")
cad_ = parser.findAll("gpxtpx:cad")
ele_ = parser.findAll("ele")

lt = parser.findAll(lat=True)
lt_ = [str(i).split("\n")[0] for i in lt]
lo = [re.findall("-*\d+\.\d*", x) for x in lt_]
lat = [float(x[0]) for x in lo]
lon = [float(x[1]) for x in lo]

hr = []
time = []
cad = []
ele = []

for h in hr_:
    hr.append(int(h.text))

for t in time_:
    new_t = t.text.replace("T", " ")
    new_t = new_t.replace("Z", "\0")
    time.append(pd.to_datetime(new_t))

time.pop(0)

for c in cad_:
    cad.append(int(c.text))

for e in ele_:
    ele.append(float(e.text))


df = pd.DataFrame({'time': time, 'hr': hr, 'cad': cad, 'ele': ele, 'lat': lat, 'lon': lon})
df = df.set_index("time")

suma = 0

for i in range(len(lat)-1):
    suma = suma + great_circle((lat[i+1], lon[i+1]), (lat[i], lon[i])).meters

print(suma)

print((df.index[len(df.index)-1] - df.index[0]).seconds/(suma*60)*1000)

#plt.figure()
#plt.plot(df)
#plt.savefig("series.png")
#sns.jointplot(x='lat', y='lon', data=df)
#plt.savefig("joinplot.png")
