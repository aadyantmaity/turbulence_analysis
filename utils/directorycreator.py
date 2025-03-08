import os
def createDirectories():
    # Directories for SVG plots
    output_dir_svg_general = "svg_plots/general"
    output_dir_svg_burbank = "svg_plots/burbank"
    output_dir_svg_santaana = "svg_plots/santaana"
    output_dir_svg_spatial = "svg_plots/spatial"
    output_dir_svg_spatial_terrain = "svg_plots/spatial/terrain"
    detailed_general_dir_svg = os.path.join(output_dir_svg_general, "turbulence_detailed_general")
    detailed_burbank_dir_svg = os.path.join(output_dir_svg_burbank, "turbulence_detailed_burbank")
    detailed_offshore_dir_svg = os.path.join(output_dir_svg_santaana, "turbulence_detailed_offshore")
    output_dir_svg_spatial_terrain_altitude = os.path.join(output_dir_svg_spatial_terrain, "altitude")
    general_3year_dir_svg = os.path.join(output_dir_svg_general, "general_3year")
    burbank_3year_dir_svg = os.path.join(output_dir_svg_burbank, "burbank_3year")
    offshore_3year_dir_svg = os.path.join(output_dir_svg_santaana, "offshore_3year")
    burbank_full_dir_svg = os.path.join(output_dir_svg_burbank, "burbank_full")
    general_full_dir_svg = os.path.join(output_dir_svg_general, "general_full")
    offshore_full_dir_svg = os.path.join(output_dir_svg_santaana, "offshore_full")

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