import pandas as pd
import re

# Read the CSV file
df = pd.read_csv('all_comments.csv')

# Function to clean comment text
def clean_comment(text):
    if pd.isna(text):
        return ""
    text = str(text)
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing spaces
    text = text.strip()
    # Remove quotes that wrap the whole text
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text

# Function to remove root mentions (@BRICSinfo, @sentdefender, @ug_chelsea)
def remove_root_mentions(text):
    # Remove these mentions (case insensitive)
    text = re.sub(r'@BRICSinfo\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'@sentdefender\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'@ug_chelsea\s*', '', text, flags=re.IGNORECASE)
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to remove URLs from text
def remove_urls(text):
    # Remove https://t.co/... URLs
    text = re.sub(r'https?://t\.co/\w+', '', text)
    # Remove any remaining URLs (just in case)
    text = re.sub(r'https?://\S+', '', text)
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Define root posts with your actual links
root_links = {
    'BRICSinfo': 'https://x.com/BRICSinfo/status/2039119905748857198?s=20',
    'sentdefender': 'https://x.com/sentdefender/status/2027869366486732809?s=20',
    'ug_chelsea': 'https://x.com/ug_chelsea/status/2031773354647024011?s=20'
}

# Clean all comments
df['cleaned_comment'] = df['reply_text'].apply(clean_comment)

# Remove root mentions from the comment
df['cleaned_comment'] = df['cleaned_comment'].apply(remove_root_mentions)

# Remove URLs from the comment
df['cleaned_comment'] = df['cleaned_comment'].apply(remove_urls)

# Determine which root post each comment belongs to
def get_root_post(row):
    original = row['reply_text'].lower() if pd.notna(row['reply_text']) else ''
    if '@bricsinfo' in original:
        return 'BRICSinfo'
    elif '@sentdefender' in original:
        return 'sentdefender'
    elif '@ug_chelsea' in original:
        return 'ug_chelsea'
    else:
        return 'Unknown'

df['root_post'] = df.apply(get_root_post, axis=1)

# Add post link based on root post
df['post_link'] = df['root_post'].map(root_links)

# Filter out the root posts themselves (keep only comments/replies)
comments_df = df[~df['username'].isin(['BRICSinfo', 'sentdefender', 'ug_chelsea'])].copy()

# ========== CLEANING ==========

# Remove comments that become empty after cleaning (e.g., only URL, only mention)
comments_df = comments_df[comments_df['cleaned_comment'].str.len() >= 3]

# Optional: Keep only comments with at least 10 meaningful characters (after removal)
def get_meaningful_length(text):
    # Remove any remaining mentions for length check
    text_clean = re.sub(r'@\w+', '', text)
    return len(text_clean.strip())

comments_df['meaningful_len'] = comments_df['cleaned_comment'].apply(get_meaningful_length)
comments_df = comments_df[comments_df['meaningful_len'] >= 10]

# Create final output with exactly 4 columns: link, comment, perception, sentiment
output_df = pd.DataFrame({
    'link': comments_df['post_link'],
    'comment': comments_df['cleaned_comment'],
    'perception': '',
    'sentiment': ''
})

# Save to CSV
output_df.to_csv('cleaned_comments.csv', index=False)

# Print summary
print("=" * 60)
print("FINAL CLEANING SUMMARY")
print("=" * 60)
print(f"Total comments after cleaning: {len(comments_df)}")
print("\nComments per root post:")
print(comments_df['root_post'].value_counts())
print("\n" + "=" * 60)
print("File saved as: cleaned_comments.csv")
print("=" * 60)

# Show preview of first 10 comments
print("\nPREVIEW (first 10 comments):")
preview_df = output_df[['link', 'comment']].head(10)
for i, row in preview_df.iterrows():
    comment_preview = row['comment'][:80] + "..." if len(row['comment']) > 80 else row['comment']
    print(f"\n{i+1}. Link: {row['link']}")
    print(f"   Comment: {comment_preview}")