import pandas as pd
import os

data_dir = "data"
output_file = "formatted_sales_data.csv"

csv_files = [
    os.path.join(data_dir, "daily_sales_data_0.csv"),
    os.path.join(data_dir, "daily_sales_data_1.csv"),
    os.path.join(data_dir, "daily_sales_data_2.csv"),
]

dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

pink_morsel_df = combined_df[combined_df["product"] == "pink morsel"].copy()

pink_morsel_df["price"] = pink_morsel_df["price"].str.replace("$", "", regex=False).astype(float)

pink_morsel_df["sales"] = pink_morsel_df["quantity"] * pink_morsel_df["price"]

output_df = pink_morsel_df[["sales", "date", "region"]]

output_df.to_csv(output_file, index=False)

print(f"Processed {len(combined_df)} total rows")
print(f"Filtered to {len(pink_morsel_df)} pink morsel rows")
print(f"Output saved to {output_file}")
