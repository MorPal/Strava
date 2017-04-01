## Primera prueba Strava Python ##

from bs4 import BeautifulSoup as soup
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Leer el fichero
run = open('20170329-163559-Run.gpx','r')
parser = soup(run, 'html.parser')

# Parser de la seccion concreto
hr_   = parser.findAll('gpxtpx:hr')
time_ = parser.findAll('time')

# Lista de pulsaciones y tiempo
hr   = []
time = []

for h in hr_:
    hr.append(int(h.text))

for t in time_:
    new_t = t.text.replace("T", " ")
    new_t = new_t.replace("Z", "\0")
    time.append(pd.to_datetime(new_t))

# Sobra un valor, lo sacamos asi
time.pop(0)

# Dataframe
# df = pd.DataFrame({'year': [], 'month': [], 'day': [], 'hour': [], 'minute': [], 'seconds': [] })
df = pd.DataFrame({'time': time, 'hr': hr})
# Cambio de indice
# df = df.set_index('hr')

#Informacion del dataframe
print(df.describe())

# Plot de hr vs tiempo

# Plot en forma histograma
ax = sns.distplot(df.hr)
fig = ax.get_figure()
fig.savefig('hr_histograma.png')

#pair Plot
plt.figure()
ay = sns.pairplot(df)
ay.savefig('pairPlot.png')
