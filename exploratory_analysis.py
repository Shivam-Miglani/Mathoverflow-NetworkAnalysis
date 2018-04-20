import pandas as pd
import numpy as np

df = pd.read_csv('SNAP/examples/temporalmotifs/data/tp1/sx-mathoverflow-a2q-tp1.txt',names=['u', 'v', 'ts'],header=None,sep=' ')

print(df.u.unique().size)
print(df.v.unique().size)
print(pd.unique(df[['u', 'v']].values.ravel('K')).size)


df2 = pd.read_csv('SNAP/examples/temporalmotifs/data/tp1/sx-mathoverflow-c2a-tp1.txt',names=['u', 'v', 'ts'],header=None,sep=' ')

print(df2.u.unique().size)



df3 = pd.read_csv('SNAP/examples/temporalmotifs/data/tp1/sx-mathoverflow-c2q-tp1.txt',names=['u', 'v', 'ts'],header=None,sep=' ')

print(df3.u.unique().size)


df4 = pd.read_csv('SNAP/examples/temporalmotifs/c1.txt',names=['u', 'count'],header=None,sep=' ')

print(df4.u.unique().size)