
import matplotlib.pyplot as plt
import pandas as pd

# Assuming 'df' is your DataFrame with the movie data
df = pd.read_csv("../extractedFiles/movies_data_20231128165632.csv")

# 1. Success Correlation Analysis
def success_correlation_analysis(df):
    plt.scatter(df['budget'], df['gross'])
    plt.title('Budget vs Gross Revenue')
    plt.xlabel('Budget')
    plt.ylabel('Gross Revenue')
    plt.show()

# 2. Genre Popularity Trends
def genre_popularity_trends(df):
    genre_counts = df['genre'].value_counts()
    genre_counts.plot(kind='bar')
    plt.title('Genre Popularity Trends')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.show()

# 3. Rating Analysis
def rating_analysis(df):
    avg_rating_by_genre = df.groupby('rating')['score'].mean()
    avg_rating_by_genre.plot(kind='bar')
    plt.title('Average Rating by Genre')
    plt.xlabel('Rating')
    plt.ylabel('Average Score')
    plt.show()

# 4. Directorial Impact
def directorial_impact(df):
    avg_rating_by_director = df.groupby('director')['score'].mean()
    avg_rating_by_director.plot(kind='bar', figsize=(10, 5))
    plt.title('Average Rating by Director')
    plt.xlabel('Director')
    plt.ylabel('Average Score')
    plt.show()

# 5. Regional Success Patterns
def regional_success_patterns(df):
    country_counts = df['country'].value_counts()
    country_counts.plot(kind='bar', figsize=(12, 6))
    plt.title('Number of Movies by Country')
    plt.xlabel('Country')
    plt.ylabel('Number of Movies')
    plt.show()

# 6. Profitability Analysis
def profitability_analysis(df):
    df['ROI'] = (df['gross'] - df['budget']) / df['budget']
    avg_roi_by_genre = df.groupby('genre')['ROI'].mean()
    avg_roi_by_genre.plot(kind='bar')
    plt.title('Average ROI by Genre')
    plt.xlabel('Genre')
    plt.ylabel('Average ROI')
    plt.show()

# 7. Performance of Franchises and Sequels
def franchise_performance(df):
    franchise_counts = df['company'].value_counts()
    franchise_counts.plot(kind='bar', color='purple')
    plt.title('Number of Movies by company')
    plt.xlabel('company')
    plt.ylabel('Number of Movies')
    plt.show()

# 8. Audience Preferences
# For sentiment analysis, you would typically use a natural language processing library, like NLTK or TextBlob.

# 9. Impact of Release Timing
def release_timing_analysis(df):
    avg_gross_by_month = df.groupby('year')['gross'].mean()
    avg_gross_by_month.plot(kind='line', marker='o', linestyle='-', color='green')
    plt.title('Average Gross Revenue by Release Year')
    plt.xlabel('Year')
    plt.ylabel('Average Gross Revenue')
    plt.show()

# 10. Runtime Relevance
def runtime_relevance(df):
    df['runtime_category'] = pd.cut(df['runtime'], bins=[0, 90, 120, float('inf')], labels=['Short', 'Medium', 'Long'])
    runtime_counts = df['runtime_category'].value_counts()
    runtime_counts.plot(kind='bar', color='orange')
    plt.title('Number of Movies by Runtime Category')
    plt.xlabel('Runtime Category')
    plt.ylabel('Number of Movies')
    plt.show()

# Example usage:
# success_correlation_analysis(df)
# genre_popularity_trends(df)
# rating_analysis(df)
# directorial_impact(df)
# regional_success_patterns(df)
# profitability_analysis(df)
#franchise_performance(df)
release_timing_analysis(df)
runtime_relevance(df)
