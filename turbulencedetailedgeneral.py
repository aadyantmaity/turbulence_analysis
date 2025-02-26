import matplotlib.pyplot as plt
from config import year_chunks_general
import os
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates

def plot_detailed_turbulence_general(df, title_prefix, save_dir, svg_status):
    for start_year in year_chunks_general:
        end_year = start_year + 1
        chunk_df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
        
        if chunk_df.empty:
            continue  

        title = f"{title_prefix} {start_year}-{end_year}"
        if svg_status:
            filename = f"detailed_turbulence_general{start_year}_{end_year}.svg"
        else:
            filename = f"detailed_turbulence_general{start_year}_{end_year}.png"
        filepath = os.path.join(save_dir, filename)

        plt.figure(figsize=(25, 10))

        mod_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD', na=False)]
        sev_turbulence = chunk_df[chunk_df['turbulence'].str.contains('SEV', na=False)]
        combined_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD-SEV', na=False)]

        mod_color = 'green'
        sev_color = 'red'
        combined_color = 'orange'

        grouped_by_date = chunk_df.groupby(chunk_df['valid'].dt.date).size()
        for date, count in grouped_by_date.items():
            daily_mod_turbulence = mod_turbulence[mod_turbulence['valid'].dt.date == date]
            daily_sev_turbulence = sev_turbulence[sev_turbulence['valid'].dt.date == date]
            daily_combined_turbulence = combined_turbulence[combined_turbulence['valid'].dt.date == date]

            plt.scatter(daily_mod_turbulence['valid'], daily_mod_turbulence['fl'], color=mod_color, label='Moderate Turbulence (MOD)', alpha=0.4, s=15 * count)
            plt.scatter(daily_sev_turbulence['valid'], daily_sev_turbulence['fl'], color=sev_color, label='Severe Turbulence (SEV)', alpha=0.4, s=15 * count)
            plt.scatter(daily_combined_turbulence['valid'], daily_combined_turbulence['fl'], color=combined_color, label='Moderate-Severe Turbulence (MOD-SEV)', alpha=0.4, s=15 * count)

        plt.xlabel("Date (UTC)")
        plt.ylabel("Flight Level (FL)")
        plt.title(title)
        plt.grid(True)

        plt.ylim(0, 40000)

        start_date = chunk_df['valid'].min()
        end_date = chunk_df['valid'].max()
        total_days = (end_date - start_date).days + 1

        plt.gca().xaxis.set_major_locator(mdates.MonthLocator()) 
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        plt.xticks(rotation=45, ha='right')

        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Saved plot: {filepath}")
        plt.close()