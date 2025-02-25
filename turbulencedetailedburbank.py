import matplotlib.pyplot as plt
from config import year_chunks_general
import os
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates

def plot_detailed_turbulence_burbank(df, title_prefix, save_dir, svg_status):
    for start_year in year_chunks_general:
        end_year = start_year + 1
        chunk_df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
        
        if chunk_df.empty:
            continue  

        title = f"{title_prefix} {start_year}-{end_year}"
        if svg_status:
            filename = f"detailed_turbulence_burbank{start_year}_{end_year}.svg"
        else:
            filename = f"detailed_turbulence_burbank{start_year}_{end_year}.png"
        filepath = os.path.join(save_dir, filename)

        plt.figure(figsize=(25, 10))

        mod_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD', na=False)]
        sev_turbulence = chunk_df[chunk_df['turbulence'].str.contains('SEV', na=False)]
        combined_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD-SEV', na=False)]

        mod_color = 'green'
        sev_color = 'red'
        combined_color = 'orange'

        plt.scatter(mod_turbulence['valid'], mod_turbulence['fl'], color=mod_color, label='Moderate Turbulence (MOD)', alpha=0.7, s=20)
        plt.scatter(sev_turbulence['valid'], sev_turbulence['fl'], color=sev_color, label='Severe Turbulence (SEV)', alpha=0.7, s=20)
        plt.scatter(combined_turbulence['valid'], combined_turbulence['fl'], color=combined_color, label='Moderate-Severe Turbulence (MOD-SEV)', alpha=0.7, s=20)

        plt.xlabel("Date (UTC)")
        plt.ylabel("Flight Level (FL)")
        plt.title(title)
        plt.legend()
        plt.grid(True)

        plt.ylim(0, 40000)

        start_date = chunk_df['valid'].min()
        end_date = chunk_df['valid'].max()
        total_days = (end_date - start_date).days + 1

        '''plt.gca().set_xticklabels([])
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='lower', nbins=total_days))
        plt.gca().xaxis.set_tick_params(width=1, length=4, direction='inout', grid_color='gray', grid_alpha=0.5)'''

        plt.gca().xaxis.set_major_locator(mdates.MonthLocator()) 
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        grouped_by_date = chunk_df.groupby(chunk_df['valid'].dt.date).size()

        for date, count in grouped_by_date.items():
            first_occurrence = chunk_df[chunk_df['valid'].dt.date == date].iloc[0]
            if first_occurrence['fl'] is not None:
                annotation_text = first_occurrence['valid'].strftime('%m-%d')
                if count > 1:
                    annotation_text += f" ({count})"
                plt.annotate(annotation_text, 
                 (first_occurrence['valid'], first_occurrence['fl']),
                 ha='center', 
                 fontsize=4, 
                 color='blue', 
                 rotation=20)

    
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Saved plot: {filepath}")
        plt.close()