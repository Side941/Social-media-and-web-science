import pandas as pd
import glob

# Find all CSV files in the same folder
all_files = glob.glob('*.csv')

# Merge them all together
df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)

# Save as one file
df.to_csv('all_comments.csv', index=False)

print(f"Done! Total rows: {len(df)}")