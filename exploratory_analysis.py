import pandas as pd
import numpy as np

df = pd.read_csv('data/tp1/sx-mathoverflow-c2q-tp1.txt',names=['u', 'v', 'ts'],header=None,sep=' ')

print(df.u.unique().size)


df2 = pd.read_csv('data/tp2/sx-mathoverflow-a2q-tp2.txt',names=['u', 'v', 'ts'],header=None,sep=' ')

print(df.u.unique().size)


df3 = pd.read_csv('data/tp2/sx-mathoverflow-c2a-tp2.txt',names=['u', 'v', 'ts'],header=None,sep=' ')

print(df.u.unique().size)