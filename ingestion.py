import os
import json
import pandas as pd


with open("config.json", "r") as f:
    config = json.load(f)

input_folder_path = config["input_folder_path"]
output_folder_path = config["output_folder_path"]


def merge_multiple_dataframe():
    """
    Read all csv files from the input folder, combine them into one dataframe,
    remove duplicate rows, save the final dataframe, and save the list of
    ingested files.
    """
    csv_files = [file for file in os.listdir(input_folder_path) if file.endswith(".csv")]
    dataframes = []

    for file in csv_files:
        file_path = os.path.join(input_folder_path, file)
        df = pd.read_csv(file_path)
        dataframes.append(df)

    final_df = pd.concat(dataframes, ignore_index=True)
    final_df = final_df.drop_duplicates()

    os.makedirs(output_folder_path, exist_ok=True)

    final_df.to_csv(os.path.join(output_folder_path, "finaldata.csv"), index=False)

    with open(os.path.join(output_folder_path, "ingestedfiles.txt"), "w") as f:
        f.write(str(csv_files))

    return final_df


if __name__ == "__main__":
    merge_multiple_dataframe()