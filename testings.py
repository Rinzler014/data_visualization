import pandas as pd


df = pd.read_csv("C:/Users/ricar/Desktop/threats.csv")


df["Identifying Time (UTC)"] = pd.to_datetime(df["Identifying Time (UTC)"], format='%b %d, %Y %I:%M:%S %p')

#Minus 6 hours to get the correct time
df["Identifying Time (UTC)"] = df["Identifying Time (UTC)"] - pd.Timedelta(hours=6)

df["Identifying Time (UTC)"] = df["Identifying Time (UTC)"].dt.strftime('%m/%d/%Y %H:%M')

#overwirte the csv file
df.to_csv("C:/Users/ricar/Desktop/threats.csv", index=False)



