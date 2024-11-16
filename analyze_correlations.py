import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('fund_prices.csv')

# Convert date column to datetime
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Calculate correlation matrix
correlation_matrix = df.corr()

# Find highly correlated pairs (absolute correlation > 0.8)
high_correlations = []
for i in range(len(correlation_matrix.columns)):
    for j in range(i+1, len(correlation_matrix.columns)):
        correlation = correlation_matrix.iloc[i, j]
        if abs(correlation) > 0.8:  # You can adjust this threshold
            high_correlations.append({
                'Fund1': correlation_matrix.columns[i],
                'Fund2': correlation_matrix.columns[j],
                'Correlation': correlation
            })

# Sort by absolute correlation value
high_correlations.sort(key=lambda x: abs(x['Correlation']), reverse=True)

# Print top correlations
print("\nTop highly correlated pairs:")
for pair in high_correlations[:10]:  # Show top 10 pairs
    print(f"{pair['Fund1']} - {pair['Fund2']}: {pair['Correlation']:.3f}")

# Create a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, cmap='RdBu', center=0)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')

# Calculate and print some summary statistics
print("\nCorrelation Summary Statistics:")
correlations_flat = correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)]
print(f"Average correlation: {correlations_flat.mean():.3f}")
print(f"Median correlation: {np.median(correlations_flat):.3f}")
print(f"Std deviation of correlations: {correlations_flat.std():.3f}")
print(f"Number of highly correlated pairs (>0.8): {len(high_correlations)}") 