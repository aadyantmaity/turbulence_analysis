import numpy as np
import pandas as pd
import re
from collections import Counter

df = pd.read_csv("pireps_200311300000_202502132359 (1).csv", low_memory=False)

df.columns = df.columns.str.lower().str.replace(" ", "_")

for column in df.select_dtypes(include='object').columns:
    df[column] = df[column].str.lstrip('0')

df['valid'] = pd.to_datetime(df['valid'], format='%Y%m%d%H%M', utc=True)

df['fl'] = pd.to_numeric(df['fl'], errors='coerce').astype('Int64')

df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

df = df.dropna(subset=['fl'])

df.replace("None", np.nan, inplace=True)

df.drop_duplicates(inplace=True)
df = df.drop(columns=['product_id'])
df = df.drop(columns=['icing'])

def extract_airports(report):
    if pd.isna(report):
        return None
    return re.findall(r'\b[A-Z]{3}\b', report)

all_airports = df['report'].dropna().apply(extract_airports)
unique_airports = set([airport for sublist in all_airports.dropna() for airport in sublist])
num_unique_airports = len(unique_airports)

burbank_turbulence = df[df['report'].str.contains('BUR', na=False) & df['turbulence'].str.contains('MOD|SEV', na=False)]
burbank_turbulence_severe = df[df['report'].str.contains('BUR', na=False) & df['turbulence'].str.contains('SEV', na=False)]

print("Preprocessed Data frame")
print(df)

print("Number of unique airports")
print(num_unique_airports)

print("Burbank Reports with Moderate to Severe Turbulence:")
print(burbank_turbulence)

print("Burbank Reports with Severe Turbulence:")
print(burbank_turbulence_severe)

df.to_csv("preprocessed_dataset.csv", index=False)
burbank_turbulence.to_csv("burbank_turbulence.csv", index=False)
burbank_turbulence_severe.to_csv("burbank_turbulence_severe.csv", index=False)