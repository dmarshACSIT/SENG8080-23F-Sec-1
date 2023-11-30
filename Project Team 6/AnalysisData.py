import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the dataset
df = pd.read_csv('ExctractedData.csv')  # Replace with the actual path to your CSV file

# Analysis 1: Number of Positions by Department
def analysis_positions_by_department():
    department_counts = df['DepartmentName'].value_counts()
    department_counts.plot(kind='bar', color='skyblue', figsize=(10, 6))
    plt.title('Number of Positions by Department')
    plt.xlabel('Department')
    plt.ylabel('Number of Positions')
    plt.tight_layout()
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.show()

# Analysis 2: Average Application Close Date
def analysis_avg_application_close_date():
    df['ApplicationCloseDate'] = pd.to_datetime(df['ApplicationCloseDate'])
    avg_close_date = df['ApplicationCloseDate'].mean()
    print(f'Average Application Close Date: {avg_close_date}')

# Analysis 3: Distribution of Job Categories
def analysis_distribution_job_categories():
    job_category_counts = df['JobCategory'].value_counts()
    job_category_counts.plot.pie(autopct='%1.1f%%', startangle=90, figsize=(8, 8))
    plt.title('Distribution of Job Categories')
    plt.tight_layout()
    plt.show()

# Analysis 4: Top Hiring Organizations
def analysis_top_hiring_organizations():
    top_organizations = df['OrganizationName'].value_counts().head(10)
    top_organizations.plot(kind='bar', color='orange', figsize=(10, 6))
    plt.title('Top Hiring Organizations')
    plt.xlabel('Organization')
    plt.ylabel('Number of Positions')
    plt.tight_layout()
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.show()

# Analysis 5: Most Common Job Grades
def analysis_most_common_job_grades():
    job_grade_counts = df['JobGrade'].value_counts()
    job_grade_counts.plot(kind='bar', color='green', figsize=(10, 6))
    plt.title('Most Common Job Grades')
    plt.xlabel('Job Grade')
    plt.ylabel('Number of Positions')
    plt.tight_layout()
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.show()

# Analysis 6: Average Position Duration
def analysis_avg_position_duration():
    df['PositionStartDate'] = pd.to_datetime(df['PositionStartDate'])
    df['PositionEndDate'] = pd.to_datetime(df['PositionEndDate'])
    df['PositionDuration'] = (df['PositionEndDate'] - df['PositionStartDate']).dt.days
    avg_duration = df['PositionDuration'].mean()
    print(f'Average Position Duration (in days): {avg_duration}')

# Analysis 7: Location of Positions
def analysis_position_location():
    location_counts = df['PositionLocationDisplay'].value_counts()
    location_counts.plot(kind='barh', color='purple', figsize=(10, 8))
    plt.title('Location of Positions')
    plt.xlabel('Number of Positions')
    plt.ylabel('Location')
    plt.tight_layout()
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.show()

# Analysis 8: Most Applied Positions
def analysis_most_applied_positions():
    applied_counts = df['ApplyURI'].value_counts().head(10)
    applied_counts.plot(kind='bar', color='red', figsize=(10, 6))
    plt.title('Most Applied Positions')
    plt.xlabel('Position Apply URI')
    plt.ylabel('Number of Applications')
    plt.tight_layout()
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.show()

# Analysis 9: Qualification Summary Word Count
def analysis_qualification_summary_word_count():
    df['QualificationSummaryWordCount'] = df['QualificationSummary'].apply(lambda x: len(str(x).split()))
    word_count_hist = df['QualificationSummaryWordCount'].plot(kind='hist', color='brown', bins=20, figsize=(10, 6))
    plt.title('Qualification Summary Word Count')
    plt.xlabel('Word Count')
    plt.ylabel('Number of Positions')
    plt.tight_layout()
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.show()

# Analysis 10: Percentage of Full-Time Positions
def analysis_percentage_full_time_positions():
    full_time_counts = df['PositionSchedule'].value_counts()
    full_time_counts.plot.pie(autopct='%1.1f%%', startangle=90, figsize=(8, 8))
    plt.title('Percentage of Full-Time Positions')
    plt.tight_layout()
    plt.show()

# Call the functions
analysis_positions_by_department()
analysis_avg_application_close_date()
analysis_distribution_job_categories()
analysis_top_hiring_organizations()
analysis_most_common_job_grades()
analysis_avg_position_duration()
analysis_position_location()
analysis_most_applied_positions()
analysis_qualification_summary_word_count()
analysis_percentage_full_time_positions()
