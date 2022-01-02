from numpy.lib.function_base import percentile
import pandas
import numpy

df = pandas.read_csv("fulldata20.csv")
drivers = df['driver'].unique()
races = df['race'].unique()
clean = pandas.read_csv("clean.csv")

#STEP 2: Find LTD (Lap Time Differential) for each driver/race combo
#2.1 find fastest lap time for each race by lap (Optimal Pace)
#2D racelap dict: dict[race][lap] = fastesttime
racelap = pandas.DataFrame(columns=['race','lap','fastestTime'])
for race in races:
    laps = df[df['race']==race]
    laps = laps['lap'].unique()
    for lap in laps:
        x = df[(df['race']==race) & (df['lap']==lap)]
        fastestTime = x['time'].min()
        to_append = pandas.Series([race,lap,fastestTime],index=racelap.columns)
        racelap = racelap.append(to_append,ignore_index=True)

#2.2 For each driver: find their total time, compare with fastest time, do TT/FT -> LTD for one race
LTD = pandas.DataFrame(columns=['race','driver','LTD'])
for driver in drivers:
    for race in races:
        driverData = clean[(clean['race']==race) & (clean['driver']==driver)]
        driverLaps = driverData['lap']
        driverLaps = driverLaps.to_numpy()
        #find fastestTime
        fastestData = racelap[(racelap['race'] == race) & (racelap["lap"].isin(driverLaps))]
        fastestTime = sum(fastestData['fastestTime'])
        #find driverTime
        driverTime = sum(driverData['time'])
        #find LTD
        try:
            driverLTD = round(driverTime/fastestTime,6)
            #add to LTD df
            to_append = pandas.Series([driver,race,driverLTD],index=LTD.columns)
            LTD = LTD.append(to_append,ignore_index=True)
        except:
            continue

LTD.to_csv("LTD.csv",index=False)