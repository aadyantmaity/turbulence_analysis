import os
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from config import year_chunks, year_chunks_general, year_chunks_3
from preprocessing import preprocess_data
from santaana import offshoreFilter

#PREPROCESSING
input_csv = "pireps_200311300000_202502132359 (1).csv"
output_csvs = {
    'preprocessed': "data_csv_files/preprocessed_dataset.csv",
    'burbank_turbulence': "data_csv_files/burbank_turbulence.csv",
    'burbank_turbulence_severe': "data_csv_files/burbank_turbulence_severe.csv",
    'fl_42000_or_above': "data_csv_files/fl_42000_or_above.csv"
}

offshore_flow = offshoreFilter()

df, burbank_turbulence = preprocess_data(input_csv, output_csvs)

#PLOTTING
df['year'] = df['valid'].dt.year
burbank_turbulence.loc[:,'year'] = burbank_turbulence['valid'].dt.year
offshore_flow['valid'] = pd.to_datetime(offshore_flow['valid'])
offshore_flow['year'] = offshore_flow['valid'].dt.year

min_year = df['year'].min()
max_year = df['year'].max()
year_chunks = list(range(min_year, max_year + 1, 2))
year_chunks_general = list(range(min_year, max_year))
year_chunks_3 = list(range(min_year, max_year + 1, 3))

# Directories for SVG plots
output_dir_svg_general = "svg_plots/general"
output_dir_svg_burbank = "svg_plots/burbank"
output_dir_svg_santaana = "svg_plots/santaana"
output_dir_svg_spatial = "svg_plots/spatial"
detailed_general_dir_svg = os.path.join(output_dir_svg_general, "turbulence_detailed_general")
detailed_burbank_dir_svg = os.path.join(output_dir_svg_burbank, "turbulence_detailed_burbank")
detailed_offshore_dir_svg = os.path.join(output_dir_svg_santaana, "turbulence_detailed_offshore")
general_3year_dir_svg = os.path.join(output_dir_svg_general, "general_3year")
burbank_3year_dir_svg = os.path.join(output_dir_svg_burbank, "burbank_3year")
offshore_3year_dir_svg = os.path.join(output_dir_svg_santaana, "offshore_3year")
burbank_full_dir_svg = os.path.join(output_dir_svg_burbank, "burbank_full")
general_full_dir_svg = os.path.join(output_dir_svg_general, "general_full")
offshore_full_dir_svg = os.path.join(output_dir_svg_santaana, "offshore_full")

os.makedirs(output_dir_svg_spatial, exist_ok=True)
os.makedirs(output_dir_svg_general, exist_ok=True)
os.makedirs(output_dir_svg_burbank, exist_ok=True)
os.makedirs(output_dir_svg_santaana, exist_ok=True)
os.makedirs(detailed_general_dir_svg, exist_ok=True)
os.makedirs(detailed_burbank_dir_svg, exist_ok=True)
os.makedirs(detailed_offshore_dir_svg, exist_ok=True)
os.makedirs(general_3year_dir_svg, exist_ok=True)
os.makedirs(burbank_3year_dir_svg, exist_ok=True)
os.makedirs(offshore_3year_dir_svg, exist_ok=True)
os.makedirs(general_full_dir_svg, exist_ok=True)
os.makedirs(burbank_full_dir_svg, exist_ok=True)
os.makedirs(offshore_full_dir_svg, exist_ok=True)

# Directories for PNG plots
output_dir_png_general = "png_plots/general"
output_dir_png_burbank = "png_plots/burbank"
output_dir_png_santaana = "png_plots/santaana"
output_dir_png_spatial = "png_plots/spatial"
detailed_general_dir_png = os.path.join(output_dir_png_general, "turbulence_detailed_general")
detailed_burbank_dir_png = os.path.join(output_dir_png_burbank, "turbulence_detailed_burbank")
detailed_offshore_dir_png = os.path.join(output_dir_png_santaana, "turbulence_detailed_offshore")
general_3year_dir_png = os.path.join(output_dir_png_general, "general_3year")
burbank_3year_dir_png = os.path.join(output_dir_png_burbank, "burbank_3year")
offshore_3year_dir_png = os.path.join(output_dir_png_santaana, "offshore_3year")
burbank_full_dir_png = os.path.join(output_dir_png_burbank, "burbank_full")
general_full_dir_png = os.path.join(output_dir_png_general, "general_full")
offshore_full_dir_png = os.path.join(output_dir_png_santaana, "offshore_full")

os.makedirs(output_dir_png_spatial, exist_ok=True)
os.makedirs(output_dir_png_general, exist_ok=True)
os.makedirs(output_dir_png_burbank, exist_ok=True)
os.makedirs(output_dir_png_santaana, exist_ok=True)
os.makedirs(detailed_general_dir_png, exist_ok=True)
os.makedirs(detailed_burbank_dir_png, exist_ok=True)
os.makedirs(detailed_offshore_dir_png, exist_ok=True)
os.makedirs(general_3year_dir_png, exist_ok=True)
os.makedirs(burbank_3year_dir_png, exist_ok=True)
os.makedirs(offshore_3year_dir_png, exist_ok=True)
os.makedirs(general_full_dir_png, exist_ok=True)
os.makedirs(burbank_full_dir_png, exist_ok=True)
os.makedirs(offshore_full_dir_png, exist_ok=True)

if __name__ == "__main__":
    from turbulence3yearchunks import plot_turbulence_by_3year_chunks
    from turbulencedetailedburbank import plot_detailed_turbulence_burbank
    from turbulencedetailedgeneral import plot_detailed_turbulence_general
    from turbulencefull import plot_turbulence_full_range
    from spatialturbulence import plot_turbulence_on_map, plot_turbulence_for_dec30_to_jan8

    #svg plots

    #PLOT TURBULENCE DETAILED
    #plot_detailed_turbulence_general(df, "Detailed Turbulence Reports", detailed_general_dir_svg, True)
    #plot_detailed_turbulence_burbank(burbank_turbulence, "Detailed Turbulence Reports - Burbank (BUR)", detailed_burbank_dir_svg, True)
    #plot_detailed_turbulence_general(offshore_flow, "Detailed Turbulence Reports - Offshore Flow", detailed_offshore_dir_svg, True)

    #PLOT TURBULENCE 3 YEAR CHUNKS
    #plot_turbulence_by_3year_chunks(df, "Turbulence Reports", general_3year_dir_svg, False, True)
    #plot_turbulence_by_3year_chunks(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_3year_dir_svg, True, True)
    #plot_turbulence_by_3year_chunks(offshore_flow, "Turbulence Reports - Offshore Flow", offshore_3year_dir_svg, False, True)
    
    #PLOT TURBULENCE FULL Range
    #plot_turbulence_full_range(df, "Turbulence Reports", general_full_dir_svg, False, True)
    #plot_turbulence_full_range(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_full_dir_svg, True, True)
    #plot_turbulence_full_range(offshore_flow, "Turbulence Reports - Offshore Flow", offshore_full_dir_svg, True, True)

    #PLOT TURBULENCE ON MAP
    #plot_turbulence_on_map(df, "Turbulence Reports", output_dir_svg_spatial, True)

    #PLOT TURBULENCE FOR DEC 30 to JAN 8
    plot_turbulence_for_dec30_to_jan8(df, "Turbulence Reports", output_dir_svg_spatial, True)

    #png plots

    #PLOT TURBULENCE DETAILED
    #plot_detailed_turbulence_general(df, "Detailed Turbulence Reports", detailed_general_dir_png, False)
    #plot_detailed_turbulence_burbank(burbank_turbulence, "Detailed Turbulence Reports - Burbank (BUR)", detailed_burbank_dir_png, False)
    #plot_detailed_turbulence_general(offshore_flow, "Detailed Turbulence Reports - Offshore Flow", detailed_offshore_dir_png, False)

    #PLOT TURBULENCE 3 YEAR CHUNKS
    #plot_turbulence_by_3year_chunks(df, "Turbulence Reports", general_3year_dir_png, False, False)
    #plot_turbulence_by_3year_chunks(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_3year_dir_png, True, False)
    #plot_turbulence_by_3year_chunks(offshore_flow, "Turbulence Reports - Offshore Flow", offshore_3year_dir_png, False, False)

    #PLOT TURBULENCE FULL Range
    #plot_turbulence_full_range(df, "Turbulence Reports", general_full_dir_png, False, False)
    #plot_turbulence_full_range(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_full_dir_png, True, False)
    #plot_turbulence_full_range(offshore_flow, "Turbulence Reports - Offshore Flow", offshore_full_dir_png, True, False)

    #PLOT TURBULENCE ON MAP
    #plot_turbulence_on_map(df, "Turbulence Reports", output_dir_png_spatial, False)

    #PLOT TURBULENCE FOR JAN 6 TO JAN 8
    plot_turbulence_for_dec30_to_jan8(df, "Turbulence Reports", output_dir_png_spatial, False)