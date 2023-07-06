import os
import pandas as pd

# Define the base directory
base_dir = r"V:\projects\p00659_dec_glo_phase3\00_collection\Survey_Deliverable\Eastfork and Spindletop 023-03-02\East Fork Bayou"

# Prepare output DataFrame
output_df = pd.DataFrame(
    columns=["Survey Point ID", "Structure ID", "Survey Code", "Structure Description", "Northing", "Easting"])

# Loop over all subdirectories and files
for root, dirs, files in os.walk(base_dir):
    for file in files:
        # Check if the file is a CSV file
        if file.endswith(".csv"):
            # Construct the full filepath
            filepath = os.path.join(root, file)

            # Load the CSV file into a pandas DataFrame
            df = pd.read_csv(filepath)

            # Find the index of the first occurrence of 'RDCL' in the third column
            rdcl_index = df[df.columns[2]].eq('RDCL').idxmax() if 'RDCL' in df[df.columns[2]].values else None

            if rdcl_index is not None:
                # Extract the desired columns (1st to 6th) for that row
                row_info = df.iloc[rdcl_index, 0:6]

                # Append to output DataFrame
                output_df = output_df.append(dict(zip(output_df.columns, row_info)), ignore_index=True)

# Name csv file
csv_filename = os.path.split(base_dir)[-1] + '.csv'

# Save DataFrame to csv
output_df.to_csv(csv_filename, index=False)

print(f"Results saved to: {csv_filename}")
