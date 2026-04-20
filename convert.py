import pandas as pd
import json

# Read ndjson file
data = []
with open('3.ndjson', 'r') as f:
    for line in f:
        data.append(json.loads(line))

# Convert to dataframe
df = pd.json_normalize(data)

# Extract just the useful columns
df_clean = df[['data.legacy.full_text', 
               'data.core.user_results.result.core.screen_name',
               'data.legacy.created_at',
               'data.legacy.favorite_count',
               'data.legacy.reply_count']]

# Rename columns
df_clean.columns = ['reply_text', 'username', 'date', 'likes', 'replies']

# Save as CSV
df_clean.to_csv('replies3.csv', index=False)
print("Done! Check replies.csv")