from datetime import date, timedelta
import numpy as np
import pandas as pd

def cleanup(fname):
    df = pd.read_csv(fname, header=0, index_col=0)
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.rename(columns={df.columns[0]:'Dateonmarket'}, inplace=True)
    df['Dateonmarket'] = [date.today() - timedelta(days=int(x.split(' ')[0])) for x in df['Dateonmarket']]
    df.to_csv('StatenIsland.csv')
    return df

frame = cleanup('C:\Users\Laolu\Dropbox\GitHub\Group1\Staten_Island.csv')
2+2
