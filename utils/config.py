import pandas as pd
import os

df = pd.read_csv("pireps_200311300000_202502132359 (1).csv", low_memory=False)

df.columns = df.columns.str.lower().str.replace(" ", "_")

df['valid'] = pd.to_datetime(df['valid'], format='%Y%m%d%H%M', utc=True)
df['year'] = df['valid'].dt.year

min_year = df['year'].min()
max_year = df['year'].max()

year_chunks = list(range(min_year, max_year + 1, 2))
year_chunks_general = list(range(min_year, max_year))
year_chunks_3 = list(range(min_year, max_year + 1, 3))
