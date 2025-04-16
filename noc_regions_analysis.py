import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('data/noc_regions.csv') 

# Fix: Check if path exists and it's not a file
if not os.path.exists('output/plots'):
    os.makedirs('output/plots')
elif os.path.isfile('output/plots'):
    print("'output/plots' exists as a file. Please delete or rename it.")
    exit()

# Clean data
df['region'] = df['region'].str.strip().str.title()
df['notes'] = df['notes'].str.strip().str.title()

# Fill missing regions with 'Unknown'
df['region'].fillna('Unknown', inplace=True)

# Summary stats
print("Total NOCs:", df['NOC'].nunique())
print("Missing regions:", df['region'].isnull().sum())
print("NOCs with notes:", df['notes'].notnull().sum())

# Save cleaned data
df.to_csv('output/cleaned_noc_regions.csv', index=False)

# Analysis: Top regions by NOC count
top_regions = df['region'].value_counts().head(10)
print("\nTop 10 regions with most NOCs:\n", top_regions)

# Plot: Bar chart of top regions
plt.figure(figsize=(10,6))
sns.barplot(x=top_regions.values, y=top_regions.index, palette="viridis")
plt.title("Top 10 Regions by Number of NOCs")
plt.xlabel("Number of NOCs")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig("output/plots/top_10_regions.png")
plt.show()

# Plot: Pie chart of region proportions
region_counts = df['region'].value_counts().head(10)
plt.figure(figsize=(8,8))
plt.pie(region_counts, labels=region_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Top 10 Region Distribution (Pie Chart)")
plt.savefig("output/plots/region_pie_chart.png")
plt.show()

# Display NOCs with historical notes
notes_df = df[df['notes'].notnull()]
print("\nNOCs with notes (historical or alternative names):")
print(notes_df[['NOC', 'region', 'notes']])

# Save filtered data
notes_df.to_csv('output/noc_with_notes.csv', index=False)

# Optional: Heatmap of missing values
plt.figure(figsize=(6, 3))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title("Missing Values Heatmap")
plt.savefig("output/plots/missing_values_heatmap.png")
plt.show()
