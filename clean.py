import pandas

df = pandas.read_csv("fulldata20.csv")

#STEP 1: Catch outliers for each race/driver
drivers = df['driver'].unique()
races = df['race'].unique()

clean = pandas.DataFrame(columns=['race','name','driver','team','lap','time'])

#1.1 for each race: find the fastest lap
FL = {}
for race in races:
    x = df[(df['race']==race)]
    FL[race] = x['time'].values.min()

#1.2 for rach driver in a race: find all laps that are at most 20% slower than the fastest lap
for driver in drivers:
    for race in races:
        times = df[(df['driver']==driver) & (df['race']==race)]
        if not times.empty:
             if times.shape[0] >= 20:
                cleanTimes = times[(times['time']) <= FL[race]*1.2]
                clean = clean.append(cleanTimes)

#1.3 export clean data to a csv 
clean.sort_values(by=['race','driver'])
clean.to_csv("clean.csv",index=False)