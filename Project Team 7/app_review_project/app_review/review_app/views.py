from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from textblob import TextBlob
from .models import allAppData
from sklearn.cluster import KMeans
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
from django.contrib.auth.decorators import login_required
from datetime import datetime


import numpy as np
import re

import os
import csv



# Create your views here.
def login_page(request):
    if request.method == 'GET':
        return render(request, "login.html", {'error_message': ''})
        
    else:
        #pass #validate the login cred and log in the super user into our system
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})

@login_required(login_url='/')
def home_page(request):
    app_list = get_all_file_names("csv_files")
    dict_data = read_csv_data_dict("csv_files/play.csv")
    app_categories = allAppData.objects.exclude(app_category__isnull=True).exclude(app_category='null').values_list('app_category').distinct()
    context = {
        "app_list": app_list,
        "app_categoris": app_categories[1:],
        "dict_data": dict_data,
        "user": request.user.username,
        "error_message":'',
    }
    return render(request, 'home.html', context)

@login_required(login_url='/')
def get_app_data(request):
    if request.method == "POST":
        app_name = request.POST["app_name"]
        create_file_path = "csv_files/"+app_name+".csv"

        print("FILE PATH : {}".format(create_file_path))

        try:
            app_review_data, positive_review_count, negative_review_count = read_csv_data_dict(create_file_path)
        except FileNotFoundError as e:
            print("NEW ERR1 : {}".format(e))

            context = {
                'error_message' : "File Not Found!"
            }
            return render(request, 'app_info.html', context)

        try:
            app_related_data = allAppData.objects.filter(app_name = app_name)[0]
        except Exception as e:
            print("NEW ERR : {}".format(e))
            context = {
                'error_message' : "File Not Found!"
            }
            return render(request, 'app_info.html', context)
        try:
            app_rating_count = convert_million_and_thousand(app_related_data.app_rating_count.split(' ')[0])
        except ValueError:
            app_rating_count = 0
        try:
            app_rating = float(app_related_data.app_rating.split('star')[0])
        except ValueError:
            app_rating = 0.0

        try:
            number_of_downloads = convert_million_and_thousand(app_related_data.number_of_downloads.split("+")[0])
        except (ValueError ,AttributeError):
            number_of_downloads = 0

        app_decision = decision_tree_helper(app_rating_count, app_rating, number_of_downloads, positive_review_count, negative_review_count)
        try:
            print("----------------------")
            app_date = datetime.strptime(app_related_data.last_update, '%Y-%m-%d %H:%M:%S')

            # new latest app logic
            today_date = datetime.today()
            get_the_date_diff = today_date - app_date
            print("DATE DIFF : {}".format(get_the_date_diff.days))
            if get_the_date_diff.days <= 165:
                new_app_msg = "We are not sure about the result (This app is latest)"
            else:
                new_app_msg = ""
        except:
                new_app_msg = ""


        context = {
            "new_app_msg": new_app_msg,
            "app_review_data":app_review_data,
            "app_name": app_related_data.app_name,
            "total_downloads": app_related_data.number_of_downloads,
            "app_rating":app_related_data.app_rating_count.split(' ')[0],
            "app_category":app_related_data.app_category,
            "app_decision": app_decision,
            "data1":[['Status', "Value"],['Positive Reviews',positive_review_count],['Negative Reviews',negative_review_count]],
            "error_message":'',

        }
        return render(request, 'app_info.html', context)

def get_category_wise_data(request):
    if request.method == "POST":
        category_name = request.POST["category_name"]
        get_category_wise_apps = allAppData.objects.filter(app_category = category_name).order_by("-app_rating")

        rating_list = []
        app_name_list = []
        temp_list = []
        for rating in get_category_wise_apps:
            try:
                match = re.findall(r"[-+]?(?:\d*\.*\d+)", rating.app_rating)
                app_rating_in_int = float(match[0])
                rating_list.append(app_rating_in_int)
                app_name_list.append(rating.app_name)
                temp_dict = {
                    "app_name": rating.app_name,
                    "app_rating": app_rating_in_int
                }
                temp_list.append(temp_dict)
            except:
                continue
        try:
            uppar_range_data, lower_range_data, centroid = kmeans_cluster(rating_list, app_name_list)
            column_wise_range_data = zip(uppar_range_data, lower_range_data)


            context = {
                "app_category": category_name,
                "column_wise_range_data": column_wise_range_data,
                "upper_centroid": round(centroid[0],2),
                "lower_centroid": round(centroid[1],2)

            }
            return render(request, 'category_info.html', context)
       
        except:
            context = {
                'error_message' : 'Category name is not valid or it has only one app for this category'
            }
            return render(request, 'app_info.html', context)

        # return HttpResponse("done")


def get_all_file_names(folder_path):   #call the function like this get_all_file_names("csv_files")
    """
    Returns a list of all file names in the given folder.
    """
    # Get a list of all files in the folder
    file_names = os.listdir(folder_path)
    
    # Filter out non-files (directories, hidden files, etc.)
    file_names = [f.rsplit(".",1)[0] for f in file_names if os.path.isfile(os.path.join(folder_path, f))]
    
    return file_names

# list reader function to read specific dataset
def read_csv_data_list(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            # Create a dictionary with only the desired columns
            data.append({'column2': row['column2'], 'column3': row['column3']})
    return data

#dict reader function to reader specific dataset
def read_csv_data_dict(csv_file_path):
    positive_review_count = 0
    negative_review_count = 0
    with open(csv_file_path, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            review_status = get_sentiment(row['review'])
            if review_status == 'positive':
                positive_review_count += 1
            else:
                negative_review_count += 1

            # Create a dictionary with only the desired columns
            data.append({'username': row['username'], 'review': row['review'], 'status': review_status})
    return data, positive_review_count, negative_review_count

def get_sentiment(text):
    """
    Returns 'positive' or 'negative' sentiment for a given text review.
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return 'positive'
    else:
        return 'negative'
    

def kmeans_cluster(data_list, app_name_list):

    # Create a list of 10 numbers
    # data = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # Convert the list to a numpy array
    X = np.array(data_list).reshape(-1, 1)

    # Specify the number of clusters
    kmeans = KMeans(n_clusters=2, random_state=0)

    # Fit the data to the k-means model
    kmeans.fit(X)

    # Print the cluster labels, centroid values, and point values
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    upper_range_values = []
    lower_range_values = []
    for i in range(len(labels)):
        if labels[0] == 1:
            if labels[i] == 0:
                # upper range centroids
                temp_dict = {
                    "app_msg": app_name_list[i]+" ("+str(X[i][0])+")",
                }
                lower_range_values.append(temp_dict)
            else:
                # lower range
                temp_dict = {
                    "app_msg": app_name_list[i]+" ("+str(X[i][0])+")",
                }
                upper_range_values.append(temp_dict)
        else:
            if labels[i] == 0:
                # upper range centroids
                temp_dict = {
                    "app_msg": app_name_list[i]+" ("+str(X[i][0])+")",
                }
                upper_range_values.append(temp_dict)
            else:
                # lower range
                temp_dict = {
                    "app_msg": app_name_list[i]+" ("+str(X[i][0])+")",
                }
                lower_range_values.append(temp_dict)

    ascending_centrodis = -np.sort(-centroids[:, 0])

    return upper_range_values, lower_range_values, ascending_centrodis

def decision_tree_helper(app_rating_count, app_rating, number_of_downloads, positive_review_count, negative_review_count):
    decision_list = []

    if app_rating >= settings.APP_RATING_THRESHOLD:
        decision_list.append(1)
    else:
        decision_list.append(0)

    
    if app_rating_count >= settings.APP_RATING_COUNT_THRESHOLD:
        decision_list.append(1)
    else:
        decision_list.append(0)

    if number_of_downloads >= settings.NUMER_OF_DOWNLOAD_THRESHOLD:
        decision_list.append(1)
    else:
        decision_list.append(0)

    if positive_review_count >= negative_review_count:
        decision_list.append(1)
    else:
        decision_list.append(0)

    predication = train_decision_tree([decision_list])

    return predication[0]


def train_decision_tree(decision_list):
    # Example dataset

    # 1st col: app_rating(star), 
    # 2nd col: app_rating_count,
    # 3rd col: number of downloads,
    # 4th col: app review count
    dataset = [
        [1,1,1,1, "Genuine"],
        [1,1,1,0, "Genuine"],
        [1,1,0,0, "Fake"],
        [1,0,0,0, "Fake"],
        [0,0,0,0, "Fake"]
    ]
    # Separate features and labels
    X = [row[:-1] for row in dataset]
    y = [row[-1] for row in dataset]

    # Create decision tree classifier
    clf = tree.DecisionTreeClassifier()

    # Fit the decision tree classifier to the data
    clf.fit(X, y)


    prediction = clf.predict(decision_list)
    return prediction

# app_rating , app_rating_count, number of downloads
def convert_million_and_thousand(a):
    if "K" in a:
        num = float(a.split("K")[0])
        num = num * 1000
    elif "M" in a:
        num = float(a.split("M")[0])
        num = num * 1000000
    elif "B" in a:
        num = float(a.split("B")[0])
        num = num * 100000000      
    else:
        num = int(a)
    return int(num)


def logout_page(request):
    logout(request)
    return redirect('/')