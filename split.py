import splitfolders

# Arguments: source_folder, output_folder, ratio, seed
splitfolders.ratio(
    "G:/PlantVillage",                # source folder (positional)
    output="G:/potato_classification_project/dataset",  # output folder (positional)
    seed=42,
    ratio=(.7, .1, .2)                # train/val/test
)
