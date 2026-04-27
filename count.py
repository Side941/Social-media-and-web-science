import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('cleaned_comments.csv', on_bad_lines='skip', encoding='utf-8')
df['perception'] = df['perception'].str.strip().str.lower()
df['sentiment'] = df['sentiment'].str.strip().str.lower()

df['post'] = df['link'].map({
    'https://x.com/BRICSinfo/status/2039119905748857198?s=20': 'Post 1\n(US Base Missile Strike)',
    'https://x.com/sentdefender/status/2027869366486732809?s=20': 'Post 2\n(Burj Al Arab on Fire)',
    'https://x.com/ug_chelsea/status/2031773354647024011?s=20': 'Post 3\n(Captured US Soldiers)'
})

colors_perception = {'believe': '#e74c3c', 'disbelieve': '#2ecc71', 'uncertain': '#f39c12'}
colors_sentiment = {'negative': '#e74c3c', 'neutral': '#95a5a6', 'positive': '#2ecc71'}

# ── Chart 1: Overall Perception Pie ──
fig1, ax1 = plt.subplots(figsize=(5, 5))
perception_counts = df['perception'].value_counts()
ax1.pie(perception_counts,
        labels=[f'{l.capitalize()}\n({v}, {v/len(df)*100:.1f}%)'
                for l, v in zip(perception_counts.index, perception_counts)],
        colors=[colors_perception[l] for l in perception_counts.index],
        startangle=90, textprops={'fontsize': 11})
ax1.set_title('Fig. 1: Overall User Perception (n=413)', fontweight='bold', fontsize=12)
plt.tight_layout()
plt.savefig('chart1_perception_pie.png', dpi=300, bbox_inches='tight')
plt.close()

# ── Chart 2: Perception by Post Bar ──
fig2, ax2 = plt.subplots(figsize=(6, 4))
perception_by_post = df.groupby(['post', 'perception']).size().unstack(fill_value=0)
perception_by_post_pct = perception_by_post.div(perception_by_post.sum(axis=1), axis=0) * 100
perception_by_post_pct[['believe', 'disbelieve', 'uncertain']].plot(
    kind='bar', ax=ax2,
    color=[colors_perception['believe'], colors_perception['disbelieve'], colors_perception['uncertain']],
    width=0.6, edgecolor='white')
ax2.set_title('Fig. 3: User Perception by Post (%)', fontweight='bold', fontsize=12)
ax2.set_ylabel('Percentage (%)')
ax2.set_xlabel('')
ax2.set_ylim(0, 100)
ax2.tick_params(axis='x', rotation=0)
ax2.legend(['Believe', 'Disbelieve', 'Uncertain'], loc='upper right')
plt.tight_layout()
plt.savefig('chart2_perception_by_post.png', dpi=300, bbox_inches='tight')
plt.close()

# ── Chart 3: Overall Sentiment Pie ──
fig3, ax3 = plt.subplots(figsize=(5, 5))
sentiment_counts = df['sentiment'].value_counts()
ax3.pie(sentiment_counts,
        labels=[f'{l.capitalize()}\n({v}, {v/len(df)*100:.1f}%)'
                for l, v in zip(sentiment_counts.index, sentiment_counts)],
        colors=[colors_sentiment[l] for l in sentiment_counts.index],
        startangle=90, textprops={'fontsize': 11})
ax3.set_title('Fig. 2: Overall User Sentiment (n=413)', fontweight='bold', fontsize=12)
plt.tight_layout()
plt.savefig('chart3_sentiment_pie.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ 3 charts saved!")
print("chart1_perception_pie.png")
print("chart2_perception_by_post.png")
print("chart3_sentiment_pie.png")