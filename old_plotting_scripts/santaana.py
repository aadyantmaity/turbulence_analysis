import pandas as pd

def offshoreFilter():
    turbulence_data = pd.read_csv('/Users/aadyant/Desktop/turbulence_analysis/data_csv_files/burbank_turbulence.csv')
    burbank_data = pd.read_csv('/Users/aadyant/Desktop/turbulence_analysis/data_csv_files/Burbank Data.csv')
    
    burbank_data.columns = burbank_data.columns.str.strip()
    
    burbank_data.rename(columns={'rel_h (%)': 'RH'}, inplace=True)

    burbank_data['RH'] = pd.to_numeric(burbank_data['RH'], errors='coerce')

    burbank_data['wind_dir (deg)'] = pd.to_numeric(burbank_data['wind_dir (deg)'], errors='coerce')
    
    turbulence_data['date'] = pd.to_datetime(turbulence_data['valid']).dt.date
    burbank_data['date'] = pd.to_datetime(burbank_data['time']).dt.date
    
    merged_data = pd.merge(turbulence_data, burbank_data, on='date')
    
    dry_periods = merged_data[merged_data['RH'] <= 50]
    
    offshore_flow = dry_periods[(dry_periods['wind_dir (deg)'] >= 315) | (dry_periods['wind_dir (deg)'] <= 45)]
    
    offshore_flow.to_csv('/Users/aadyant/Desktop/turbulence_analysis/filtered_data.csv', index=False)

    return offshore_flow
