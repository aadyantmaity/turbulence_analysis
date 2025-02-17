import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import os

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
df = df.drop(columns=['product_id', 'icing'])

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

output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

general_dir = os.path.join(output_dir, "general")
burbank_dir = os.path.join(output_dir, "burbank")

os.makedirs(general_dir, exist_ok=True)
os.makedirs(burbank_dir, exist_ok=True)

df['year'] = df['valid'].dt.year
burbank_turbulence.loc[:,'year'] = burbank_turbulence['valid'].dt.year

min_year = df['year'].min()
max_year = df['year'].max()

year_chunks = list(range(min_year, max_year + 1, 3))

def plot_turbulence_by_chunks(df, title_prefix, save_dir):
    for start_year in year_chunks:
        end_year = start_year + 2
        chunk_df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
        
        if chunk_df.empty:
            continue  
        
        title = f"{title_prefix} {start_year}-{end_year}"
        filename = f"turbulence_{start_year}_{end_year}.png"
        filepath = os.path.join(save_dir, filename)
        
        plt.figure(figsize=(12, 6))

        mod_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD', na=False)]
        plt.scatter(mod_turbulence['valid'], mod_turbulence['fl'], color='green', label='Moderate Turbulence (MOD)', alpha=0.7)

        sev_turbulence = chunk_df[chunk_df['turbulence'].str.contains('SEV', na=False)]
        plt.scatter(sev_turbulence['valid'], sev_turbulence['fl'], color='red', label='Severe Turbulence (SEV)', alpha=0.7)

        plt.xlabel("Date (UTC)")
        plt.ylabel("Flight Level (feet)")
        plt.title(title)
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)

        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Saved plot: {filepath}")
        plt.close()


plot_turbulence_by_chunks(df, "Turbulence Reports", general_dir)
plot_turbulence_by_chunks(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_dir)
