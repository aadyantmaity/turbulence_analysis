from config import year_chunks_3
import matplotlib.pyplot as plt
import os

def plot_turbulence_by_3year_chunks(df, title_prefix, save_dir):
    for start_year in year_chunks_3:
        end_year = start_year + 3
        chunk_df = df[(df['year'] >= start_year) & (df['year'] < end_year)]
        
        if chunk_df.empty:
            continue  
        
        title = f"{title_prefix} {start_year}-{end_year - 1}"
        filename = f"turbulence_{start_year}_{end_year - 1}.png"
        filepath = os.path.join(save_dir, filename)
        
        plt.figure(figsize=(12, 6))

        mod_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD', na=False)]
        sev_turbulence = chunk_df[chunk_df['turbulence'].str.contains('SEV', na=False)]

        plt.scatter(mod_turbulence['valid'], mod_turbulence['fl'], color='green', label='Moderate Turbulence (MOD)', alpha=0.7)
        plt.scatter(sev_turbulence['valid'], sev_turbulence['fl'], color='red', label='Severe Turbulence (SEV)', alpha=0.7)

        plt.xlabel("Date (UTC)")
        plt.ylabel("Flight Level (feet)")
        plt.title(title)
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.ylim(0, 40000)

        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Saved plot: {filepath}")
        plt.close()