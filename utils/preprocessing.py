import pandas as pd
import numpy as np
import re

def preprocess_data(input_csv, output_csvs):
    df = pd.read_csv(input_csv, low_memory=False)

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    for column in df.select_dtypes(include='object').columns:
        df[column] = df[column].str.lstrip('0')

    df['valid'] = pd.to_datetime(df['valid'], format='%Y%m%d%H%M', utc=True)
    df['fl'] = pd.to_numeric(df['fl'], errors='coerce').astype('Int64')
    df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    fl_42000_or_above = df[df['fl'] >= 42000]

    def extract_fl(report):
        if pd.isna(report):
            return None
        match = re.search(r'/FL(\d+)', report)
        if match:
            return int(match.group(1))
        return None

    df['fl_extracted'] = df['report'].apply(extract_fl)
    df.loc[df['fl'] >= 42000, 'fl'] = df['fl_extracted']

    df.drop(columns=['fl_extracted'], inplace=True)

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
    df.to_csv(output_csvs['preprocessed'], index=False)
    burbank_turbulence.to_csv(output_csvs['burbank_turbulence'], index=False)
    burbank_turbulence_severe.to_csv(output_csvs['burbank_turbulence_severe'], index=False)
    fl_42000_or_above.to_csv(output_csvs['fl_42000_or_above'], index=False)
    '''
    return df, burbank_turbulence