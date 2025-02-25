import os
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from config import year_chunks, year_chunks_general, year_chunks_3

df = pd.read_csv("pireps_200311300000_202502132359 (1).csv", low_memory=False)

df.columns = df.columns.str.lower().str.replace(" ", "_")

for column in df.select_dtypes(include='object').columns:
    df[column] = df[column].str.lstrip('0')

df['valid'] = pd.to_datetime(df['valid'], format='%Y%m%d%H%M', utc=True)
df['fl'] = pd.to_numeric(df['fl'], errors='coerce').astype('Int64')
df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
fl_42000_or_above = df[df['fl'] >= 42000]

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

'''
df.to_csv("preprocessed_dataset.csv", index=False)
burbank_turbulence.to_csv("burbank_turbulence.csv", index=False)
burbank_turbulence_severe.to_csv("burbank_turbulence_severe.csv", index=False)
fl_42000_or_above.to_csv("fl_42000_or_above.csv", index=False)
'''

df['year'] = df['valid'].dt.year
burbank_turbulence.loc[:,'year'] = burbank_turbulence['valid'].dt.year

min_year = df['year'].min()
max_year = df['year'].max()
year_chunks = list(range(min_year, max_year + 1, 2))
year_chunks_general = list(range(min_year, max_year))
year_chunks_3 = list(range(min_year, max_year + 1, 3))

output_dir_svg = "svg_plots"
detailed_general_dir_svg = os.path.join(output_dir_svg, "turbulence_detailed_general")
detailed_burbank_dir_svg = os.path.join(output_dir_svg, "turbulence_detailed_burbank")
general_3year_dir_svg = os.path.join(output_dir_svg, "general_3year")
burbank_3year_dir_svg = os.path.join(output_dir_svg, "burbank_3year")
burbank_full_dir_svg = os.path.join(output_dir_svg, "burbank_full")
general_full_dir_svg = os.path.join(output_dir_svg, "general_full")

os.makedirs(output_dir_svg, exist_ok=True)
os.makedirs(detailed_general_dir_svg, exist_ok=True)
os.makedirs(detailed_burbank_dir_svg, exist_ok=True)
os.makedirs(general_3year_dir_svg, exist_ok=True)
os.makedirs(burbank_3year_dir_svg, exist_ok=True)
os.makedirs(general_full_dir_svg, exist_ok=True)
os.makedirs(burbank_full_dir_svg, exist_ok=True)

output_dir_png= "png_plots"
detailed_general_dir_png = os.path.join(output_dir_png, "turbulence_detailed_general")
detailed_burbank_dir_png = os.path.join(output_dir_png, "turbulence_detailed_burbank")
general_3year_dir_png = os.path.join(output_dir_png, "general_3year")
burbank_3year_dir_png = os.path.join(output_dir_png, "burbank_3year")
burbank_full_dir_png = os.path.join(output_dir_png, "burbank_full")
general_full_dir_png = os.path.join(output_dir_png, "general_full")

os.makedirs(output_dir_png, exist_ok=True)
os.makedirs(detailed_general_dir_png, exist_ok=True)
os.makedirs(detailed_burbank_dir_png, exist_ok=True)
os.makedirs(general_3year_dir_png, exist_ok=True)
os.makedirs(burbank_3year_dir_png, exist_ok=True)
os.makedirs(general_full_dir_png, exist_ok=True)
os.makedirs(burbank_full_dir_png, exist_ok=True)

if __name__ == "__main__":
    from turbulence3yearchunks import plot_turbulence_by_3year_chunks
    from turbulencedetailedburbank import plot_detailed_turbulence_burbank
    from turbulencedetailedgeneral import plot_detailed_turbulence_general
    from turbulencefull import plot_turbulence_full_range

    #svg plots

    #PLOT TURBULENCE DETAILED
    plot_detailed_turbulence_general(df, "Detailed Turbulence Reports", detailed_general_dir_svg, True)
    plot_detailed_turbulence_burbank(burbank_turbulence, "Detailed Turbulence Reports - Burbank (BUR)", detailed_burbank_dir_svg, True)
    

    #PLOT TURBULENCE 3 YEAR CHUNKS
    #plot_turbulence_by_3year_chunks(df, "Turbulence Reports", general_3year_dir_svg, False, True)
    #plot_turbulence_by_3year_chunks(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_3year_dir_svg, True, True)
    

    #PLOT TURBULENCE FULL Range
    #plot_turbulence_full_range(df, "Turbulence Reports", general_full_dir_svg, False, True)
    #plot_turbulence_full_range(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_full_dir_svg, True, True)

    #png plots

    #PLOT TURBULENCE DETAILED
    #plot_detailed_turbulence_general(df, "Detailed Turbulence Reports", detailed_general_dir_png, False)
    #plot_detailed_turbulence_burbank(burbank_turbulence, "Detailed Turbulence Reports - Burbank (BUR)", detailed_burbank_dir_png, False)

    #PLOT TURBULENCE 3 YEAR CHUNKS
    #plot_turbulence_by_3year_chunks(df, "Turbulence Reports", general_3year_dir_png, False, False)
    #plot_turbulence_by_3year_chunks(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_3year_dir_png, True, False)

    #PLOT TURBULENCE FULL Range
    #plot_turbulence_full_range(df, "Turbulence Reports", general_full_dir_png, False, False)
    #plot_turbulence_full_range(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_full_dir_png, True, False)

