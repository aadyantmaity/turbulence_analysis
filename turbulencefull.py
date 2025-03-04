from config import year_chunks_3
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MaxNLocator
import pandas as pd
import matplotlib.dates as mdates


def plot_turbulence_full_range(df, title_prefix, save_dir, annotation_status, svg_status):
    start_year, end_year = 2003, 2026
    chunk_df = df[(df['year'] >= start_year) & (df['year'] < end_year)]

    if chunk_df.empty:
        return

    title = f"{title_prefix} {start_year}-{end_year - 1}"

    if svg_status:
        filename = f"turbulence_{start_year}_{end_year - 1}.svg"
    else:
        filename = f"turbulence_{start_year}_{end_year - 1}.png"
    filepath = os.path.join(save_dir, filename)

    plt.figure(figsize=(35, 10))

    combined_turbulence = chunk_df[
        (chunk_df['turbulence'].str.contains(r'\bMOD-SEV\b', na=False) |
         chunk_df['report'].str.contains(r'\bMOD-SEV\b', na=False))
    ]

    sev_turbulence = chunk_df[
        ~chunk_df.index.isin(combined_turbulence.index) &
        (chunk_df['turbulence'].str.contains(r'\bSEVERE\b|\bSEV\b', na=False) |
         chunk_df['report'].str.contains(r'\bSEVERE\b|\bSEV\b', na=False))
    ]

    combined_turbulence = chunk_df[
        ~chunk_df.index.isin(sev_turbulence.index) &
        (chunk_df['turbulence'].str.contains(r'\bMOD-SEV\b', na=False) |
         chunk_df['report'].str.contains(r'\bMOD-SEV\b', na=False))
    ]

    mod_turbulence = chunk_df[
        ~chunk_df.index.isin(sev_turbulence.index) &
        ~chunk_df.index.isin(combined_turbulence.index) &
        (chunk_df['turbulence'].str.contains(r'\bMOD\b', na=False) |
         chunk_df['report'].str.contains(r'\bMOD\b', na=False))
    ]

    mod_color = 'green'
    sev_color = 'red'
    combined_color = 'orange'

    dot_size = 50

    plt.scatter(mod_turbulence['valid'], mod_turbulence['fl'], color=mod_color,
                label='Moderate Turbulence (MOD)', alpha=0.7, s=dot_size)
    plt.scatter(sev_turbulence['valid'], sev_turbulence['fl'], color=sev_color,
                label='Severe Turbulence (SEV)', alpha=0.7, s=dot_size)
    plt.scatter(combined_turbulence['valid'], combined_turbulence['fl'], color=combined_color,
                label='Moderate-Severe Turbulence (MOD-SEV)', alpha=0.7, s=dot_size)

    plt.xlabel("Date (UTC)")
    plt.ylabel("Flight Level (FL)")
    plt.title(title)
    plt.xticks(rotation=90)
    plt.grid(True)

    start_date = chunk_df['valid'].min()
    end_date = chunk_df['valid'].max()
    total_days = (end_date - start_date).days + 1
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

    plt.xlim(start_date, end_date)
    plt.ylim(0, 40000)

    '''plt.xticks(all_dates, [date.strftime('%Y-%m-%d') for date in all_dates], rotation=90, fontsize=3)
    plt.gca().xaxis.set_tick_params(width=1, length=4, direction='inout', grid_color='gray', grid_alpha=0.5)
    '''

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    '''if annotation_status:
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
                rotation=20)'''

    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    print(f"Saved plot: {filepath}")
    plt.close()
