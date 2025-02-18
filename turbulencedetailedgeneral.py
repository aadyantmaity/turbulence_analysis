import matplotlib.pyplot as plt
from config import year_chunks_general
from matplotlib.ticker import MaxNLocator
import pandas as pd
import os

def plot_detailed_turbulence_general(df, title_prefix, save_dir, svg_status):
    for start_year in year_chunks_general:
        end_year = start_year + 1
        chunk_df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
        
        if chunk_df.empty:
            continue  

        title = f"{title_prefix} {start_year}-{end_year}"
        if svg_status:
            filename = f"detailed_turbulence_general_{start_year}_{end_year}.svg"
        else:
            filename = f"detailed_turbulence_general_{start_year}_{end_year}.png"
        filepath = os.path.join(save_dir, filename)

        plt.figure(figsize=(150, 10))

        mod_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD', na=False)]
        sev_turbulence = chunk_df[chunk_df['turbulence'].str.contains('SEV', na=False)]
        combined_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD-SEV', na=False)]

        mod_color = 'green'
        sev_color = 'red'
        combined_color = 'orange'

        plt.scatter(mod_turbulence['valid'], mod_turbulence['fl'], color=mod_color, label='Moderate Turbulence (MOD)', alpha=0.7, s=10)
        plt.scatter(sev_turbulence['valid'], sev_turbulence['fl'], color=sev_color, label='Severe Turbulence (SEV)', alpha=0.7, s=10)
        plt.scatter(combined_turbulence['valid'], combined_turbulence['fl'], color=combined_color, label='Moderate-Severe Turbulence (MOD-SEV)', alpha=0.7, s=10)

        plt.xlabel("Date (UTC)")
        plt.ylabel("Flight Level (feet)")
        plt.title(title)
        plt.grid(True)

        plt.ylim(0, 40000)

        start_date = chunk_df['valid'].min()
        end_date = chunk_df['valid'].max()
        plt.xlim(start_date, end_date)

        total_days = (end_date - start_date).days + 1
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='lower', nbins=total_days))

        all_ticks = pd.date_range(start=start_date, end=end_date, freq='D')

        alternate_ticks = all_ticks[::2]

        plt.xticks(
            alternate_ticks,
            rotation=45,
            ha='right'
        )

        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Saved plot: {filepath}")
        plt.close()