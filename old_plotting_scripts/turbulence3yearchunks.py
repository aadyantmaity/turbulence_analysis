from config import year_chunks_3
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MaxNLocator
import pandas as pd
import matplotlib.dates as mdates


def plot_turbulence_by_3year_chunks(df, title_prefix, save_dir, annotation_status, svg_status):
    for start_year in year_chunks_3:
        end_year = start_year + 3
        chunk_df = df[(df['year'] >= start_year) & (df['year'] < end_year)]

        if chunk_df.empty:
            continue

        title = f"{title_prefix} {start_year}-{end_year - 1}"
        if svg_status:
            filename = f"turbulence_{start_year}_{end_year - 1}.svg"
        else:
            filename = f"turbulence_{start_year}_{end_year - 1}.png"
        filepath = os.path.join(save_dir, filename)

        plt.figure(figsize=(25, 10))

        modsev_turbulence = chunk_df[
            (chunk_df['turbulence'].str.contains(r'\bMOD-SEV\b', na=False) |
             chunk_df['report'].str.contains(r'\bMOD-SEV\b', na=False))
        ]

        sev_turbulence = chunk_df[
            ~chunk_df.index.isin(modsev_turbulence.index) &
            (chunk_df['turbulence'].str.contains(r'\bSEVERE\b|\bSEV\b', na=False) |
             chunk_df['report'].str.contains(r'\bSEVERE\b|\bSEV\b', na=False))
        ]

        modsev_turbulence = chunk_df[
            ~chunk_df.index.isin(sev_turbulence.index) &
            (chunk_df['turbulence'].str.contains(r'\bMOD-SEV\b', na=False) |
             chunk_df['report'].str.contains(r'\bMOD-SEV\b', na=False))
        ]

        mod_turbulence = chunk_df[
            ~chunk_df.index.isin(sev_turbulence.index) &
            ~chunk_df.index.isin(modsev_turbulence.index) &
            (chunk_df['turbulence'].str.contains(r'\bMOD\b', na=False) |
             chunk_df['report'].str.contains(r'\bMOD\b', na=False))
        ]

        mod_color = 'green'
        sev_color = 'red'
        modsev_color = 'orange'
        dot_size = 75

        grouped_by_date = chunk_df.groupby(chunk_df['valid'].dt.date).size()
        if annotation_status:
            for date, count in grouped_by_date.items():
                daily_mod_turbulence = mod_turbulence[mod_turbulence['valid'].dt.date == date]
                daily_sev_turbulence = sev_turbulence[sev_turbulence['valid'].dt.date == date]
                daily_combined_turbulence = modsev_turbulence[
                    modsev_turbulence['valid'].dt.date == date]

                plt.scatter(daily_mod_turbulence['valid'], daily_mod_turbulence['fl'],
                            color=mod_color, label='Moderate Turbulence (MOD)', alpha=0.4, s=15 * count)
                plt.scatter(daily_sev_turbulence['valid'], daily_sev_turbulence['fl'],
                            color=sev_color, label='Severe Turbulence (SEV)', alpha=0.4, s=15 * count)
                plt.scatter(daily_combined_turbulence['valid'], daily_combined_turbulence['fl'],
                            color=modsev_color, label='Moderate-Severe Turbulence (MOD-SEV)', alpha=0.4, s=15 * count)
        else:
            plt.scatter(mod_turbulence['valid'], mod_turbulence['fl'], color=mod_color,
                        label='Moderate Turbulence (MOD)', alpha=0.7, s=dot_size)
            plt.scatter(sev_turbulence['valid'], sev_turbulence['fl'], color=sev_color,
                        label='Severe Turbulence (SEV)', alpha=0.7, s=dot_size)
            plt.scatter(modsev_turbulence['valid'], modsev_turbulence['fl'], color=modsev_color,
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

        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        plt.xticks(rotation=45, ha='right')

        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Saved plot: {filepath}")
        plt.close()
