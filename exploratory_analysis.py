import pandas as pd
import numpy as np

df = pd.read_csv('data/tp1/sx-mathoverflow-c2q-tp1.txt',names=['u', 'v', 'ts'],header=None,sep=' ')

print(df.u.unique().size)