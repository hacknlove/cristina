import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.stats import pearsonr
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class CorrelationAnalyzer:
    def __init__(self, csv_path, correlation_threshold=0.8):
        self.correlation_threshold = correlation_threshold
        # Read and prepare data
        self.df = pd.read_csv(csv_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df.set_index('Date', inplace=True)
        
    def static_correlation_analysis(self):
        """Basic correlation analysis"""
        print("\n=== Static Correlation Analysis ===")
        
        # Calculate correlation matrix
        self.correlation_matrix = self.df.corr()
        
        # Find highly correlated pairs
        high_correlations = []
        for i in range(len(self.correlation_matrix.columns)):
            for j in range(i+1, len(self.correlation_matrix.columns)):
                correlation = self.correlation_matrix.iloc[i, j]
                pvalue = pearsonr(self.df.iloc[:,i], self.df.iloc[:,j])[1]
                if abs(correlation) > self.correlation_threshold:
                    high_correlations.append({
                        'Fund1': self.correlation_matrix.columns[i],
                        'Fund2': self.correlation_matrix.columns[j],
                        'Correlation': correlation,
                        'P-value': pvalue
                    })
        
        # Sort and print results
        high_correlations.sort(key=lambda x: abs(x['Correlation']), reverse=True)
        print("\nTop 10 highly correlated pairs:")
        for pair in high_correlations[:10]:
            print(f"{pair['Fund1']} - {pair['Fund2']}: {pair['Correlation']:.3f} (p-value: {pair['P-value']:.3e})")
        
        return high_correlations

    def rolling_correlation_analysis(self, window=60):
        """Time-varying correlation analysis"""
        print(f"\n=== Rolling Correlation Analysis (Window: {window} days) ===")
        
        # Calculate rolling correlations for highly correlated pairs
        high_correlations = self.static_correlation_analysis()
        top_pairs = high_correlations[:5]  # Analyze top 5 pairs
        
        plt.figure(figsize=(15, 8))
        for pair in top_pairs:
            rolling_corr = self.df[pair['Fund1']].rolling(window).corr(self.df[pair['Fund2']])
            plt.plot(rolling_corr.index, rolling_corr.values, label=f"{pair['Fund1']} - {pair['Fund2']}")
        
        plt.title(f'Rolling Correlations (Window: {window} days)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('rolling_correlations.png')
        plt.close()

    def cluster_analysis(self, n_clusters=5):
        """Perform cluster analysis"""
        print(f"\n=== Cluster Analysis (K-means, {n_clusters} clusters) ===")
        
        # Hierarchical Clustering
        linkage_matrix = hierarchy.linkage(self.correlation_matrix, method='ward')
        plt.figure(figsize=(15, 10))
        hierarchy.dendrogram(linkage_matrix, labels=self.correlation_matrix.columns)
        plt.title('Hierarchical Clustering Dendrogram')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('dendrogram.png')
        plt.close()

        # K-means Clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(self.df.T)
        
        # Print cluster members
        for i in range(n_clusters):
            cluster_members = self.df.columns[clusters == i]
            print(f"\nCluster {i+1} members:")
            print(', '.join(cluster_members))

    def create_heatmap(self):
        """Create and save correlation heatmap"""
        plt.figure(figsize=(15, 12))
        sns.heatmap(self.correlation_matrix, cmap='RdBu', center=0, annot=False)
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.savefig('correlation_heatmap.png')
        plt.close()

    def correlation_statistics(self):
        """Calculate and print correlation statistics"""
        print("\n=== Correlation Statistics ===")
        
        # Get upper triangle of correlation matrix
        correlations_flat = self.correlation_matrix.values[np.triu_indices_from(self.correlation_matrix.values, k=1)]
        
        stats = {
            'Mean': np.mean(correlations_flat),
            'Median': np.median(correlations_flat),
            'Std Dev': np.std(correlations_flat),
            'Min': np.min(correlations_flat),
            'Max': np.max(correlations_flat),
            'Skewness': pd.Series(correlations_flat).skew(),
            'Kurtosis': pd.Series(correlations_flat).kurtosis()
        }
        
        for stat, value in stats.items():
            print(f"{stat}: {value:.3f}")

def main():
    # Initialize analyzer
    analyzer = CorrelationAnalyzer('fund_prices.csv')
    
    # Run all analyses
    analyzer.static_correlation_analysis()
    analyzer.rolling_correlation_analysis(window=60)  # 60-day rolling window
    analyzer.cluster_analysis(n_clusters=5)
    analyzer.create_heatmap()
    analyzer.correlation_statistics()

if __name__ == "__main__":
    main()