import pandas as pd

df = pd.read_csv('cost_revenue.csv')
df.shape

df.drop( df[df['domestic_gross_usd'] == 0].index, inplace=True)   # removes all 0 
df.drop( df[df['worldwide_gross_usd'] == 0].index, inplace=True)  # removes all 0 

del df['domestic_gross_usd']  # we just use worldwide gross

df.to_csv('cost_revenue_clean.csv', index = False, header=True)