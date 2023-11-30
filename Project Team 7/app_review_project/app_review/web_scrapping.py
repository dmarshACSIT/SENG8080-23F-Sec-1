from app_store_scraper import AppStore
import pandas as pd

def get_app_info(app_id):
    app_data = AppStore(country="us", app_name=app_id)
    app_data.review(how_many=1)  
    print("-------------------------")
    print(app_data.reviews[0]['developerResponse']['rating'])
    return {
        'App Name': app_data.app_name,
        'App Rating': app_data.reviews[0]['developerResponse']['rating'], 
        'Rating Count': app_data.reviews,
        'Downloads': app_data.app_id,
    }

def get_user_reviews(app_id, num_reviews=40):
    app_data = AppStore(country="us", app_name=app_id)
    app_data.review(how_many=num_reviews)
    reviews = [{'User Review': review.get('review')} for review in app_data.reviews]
    return reviews

def main():
    # App ID to scrape
    app_id = '835599320'

    app_info_dataframe = pd.DataFrame()
    user_reviews_dataframe = pd.DataFrame()

    app_info = get_app_info(app_id)

    app_info_dataframe = app_info_dataframe._append(app_info, ignore_index=True)

    user_reviews = get_user_reviews(app_id)

    user_reviews_dataframe = user_reviews_dataframe._append(user_reviews, ignore_index=True)

    # Export data to Excel
    app_info_dataframe.to_excel('c:/Users/nileshpandey/Desktop/nilesh/Big_data_study/midterm-ass/app_info.xlsx', index=False)
    user_reviews_dataframe.to_csv('c:/Users/nileshpandey/Desktop/nilesh/Big_data_study/midterm-ass/user_reviews.csv', index=False)

if __name__ == "__main__":
    main()

