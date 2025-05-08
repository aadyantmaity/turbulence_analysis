import os
# Directories for Spatial plots
output_dir_svg_spatial_terrain = "spatial/terrain"
output_dir_svg_spatial_terrain_altitude = os.path.join(output_dir_svg_spatial_terrain, "altitude")

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