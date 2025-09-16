import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
import os

def load_and_explore_data():
    """Load and explore the Iris dataset."""
    try:
        # Load Iris dataset from sklearn
        iris = load_iris()
        df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
        df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
        
        print("=== Data Exploration ===")
        print("\nFirst 5 rows of the dataset:")
        print(df.head())
        
        print("\nDataset Info:")
        print(df.info())
        
        print("\nMissing Values:")
        print(df.isnull().sum())
        
        # Since Iris dataset is clean, no need for cleaning, but included for completeness
        if df.isnull().any().any():
            print("\nCleaning missing values by dropping rows with NaN...")
            df = df.dropna()
        
        return df
    
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        return None

def analyze_data(df):
    """Perform basic data analysis on the Iris dataset."""
    print("\n=== Data Analysis ===")
    
    # Basic statistics
    print("\nBasic Statistics:")
    print(df.describe())
    
    # Group by species and compute mean for numerical columns
    group_means = df.groupby('species').mean()
    print("\nMean values by species:")
    print(group_means)
    
    # Observations
    print("\n=== Observations ===")
    print("- The dataset contains measurements for 150 iris flowers across three species.")
    print("- Numerical columns: sepal length, sepal width, petal length, petal width (all in cm).")
    print(f"- {group_means.index[0]} has the smallest average petal length ({group_means['petal length (cm)'][0]:.2f} cm).")
    print(f"- {group_means.index[2]} has the largest average sepal length ({group_means['sepal length (cm)'][2]:.2f} cm).")
    
    return group_means

def create_visualizations(df):
    """Create four different visualizations for the Iris dataset."""
    # Set seaborn style for better visuals
    sns.set_style("whitegrid")
    
    # Create directory for saving plots
    os.makedirs("Fetched_Images", exist_ok=True)
    
    # 1. Line chart (simulating petal length trend across ordered samples per species)
    plt.figure(figsize=(10, 6))
    for species in df['species'].unique():
        species_data = df[df['species'] == species]['petal length (cm)']
        plt.plot(species_data.index, species_data, label=species)
    plt.title('Petal Length Trend Across Ordered Samples by Species')
    plt.xlabel('Sample Index')
    plt.ylabel('Petal Length (cm)')
    plt.legend()
    plt.savefig('Fetched_Images/petal_length_trend.png')
    plt.close()
    
    # 2. Bar chart of average petal length by species
    group_means = df.groupby('species').mean()
    plt.figure(figsize=(10, 6))
    group_means['petal length (cm)'].plot(kind='bar', color=['#FF9999', '#66B2FF', '#99FF99'])
    plt.title('Average Petal Length by Species')
    plt.xlabel('Species')
    plt.ylabel('Average Petal Length (cm)')
    plt.xticks(rotation=45)
    plt.savefig('Fetched_Images/avg_petal_length_bar.png')
    plt.close()
    
    # 3. Histogram of sepal length
    plt.figure(figsize=(10, 6))
    plt.hist(df['sepal length (cm)'], bins=15, color='skyblue', edgecolor='black')
    plt.title('Distribution of Sepal Length')
    plt.xlabel('Sepal Length (cm)')
    plt.ylabel('Frequency')
    plt.savefig('Fetched_Images/sepal_length_histogram.png')
    plt.close()
    
    # 4. Scatter plot of sepal length vs petal length
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='sepal length (cm)', y='petal length (cm)', hue='species', palette='deep')
    plt.title('Sepal Length vs Petal Length by Species')
    plt.xlabel('Sepal Length (cm)')
    plt.ylabel('Petal Length (cm)')
    plt.legend()
    plt.savefig('Fetched_Images/sepal_vs_petal_scatter.png')
    plt.close()

def main():
    # Load and explore data
    df = load_and_explore_data()
    if df is None:
        return
    
    # Analyze data
    analyze_data(df)
    
    # Create visualizations
    create_visualizations(df)
    
    print("\n=== Final Notes ===")
    print("- Visualizations are saved in the 'Fetched_Images' directory.")
    print("- The line chart shows petal length trends, though not time-based, it highlights species differences.")
    print("- The bar chart confirms setosa has the shortest average petal length.")
    print("- The histogram shows sepal length is roughly normally distributed.")
    print("- The scatter plot reveals clear separation between species based on sepal and petal lengths.")

if __name__ == "__main__":
    main()