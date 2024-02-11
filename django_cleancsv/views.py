from django.shortcuts import render, redirect
from .models import UploadedFile
from django.http import HttpResponse
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib as plt
from io import BytesIO
import base64

# https://plotly.com/python/radar-chart/
def create_radar_chart(df, variables, values):
    fig = px.line_polar(df, r=values, theta=variables, line_close=True,
                        color_discrete_sequence=['purple'], title="SCORE")
    fig.update_traces(fill='toself')
    fig.write_image("static/assets/img/score.png")


def upload_file(request):
    radar_chart_image = None
    context = None
    cleaned = None

    if request.method == 'POST':
        inconsistent_type_score = 0
        emptiness_score = 0
        duplicate_score = 0

        file = request.FILES['file']
        df = pd.read_csv(file)

        # Calculate scores
        duplicate_score = calculate_duplicate_score(df)
        emptiness_score = calculate_emptiness(df)
        inconsistent_type_score = calculate_type_inconsistency(df)
        # unique_values_score = calculate_uniqueness(df)

        # duplicate_score = 76
        # emptiness_score = 43
        # inconsistent_type_score = 22
        # unique_values_score = 48

        cleaned = clean_dataframe(df)

        duplicate_score2 = calculate_duplicate_score(cleaned)
        emptiness_score2 = calculate_emptiness(cleaned)
        inconsistent_type_score2 = calculate_type_inconsistency(cleaned)
        cleaned.to_csv('static/files/out.csv')


        # Create radar chart
        variables = ['Uniqueness', 'Completeness', 'Consistency']
        values = [duplicate_score, emptiness_score, inconsistent_type_score]

        radar_chart_image = create_radar_chart(df, variables, values)
        # radar_chart_image_cleaned = create_radar_chart(df, variables, values2)

        print("Uniqueness: " + str(duplicate_score))
        print("Comleteness: " + str(emptiness_score))
        print("Consistency: " + str(inconsistent_type_score))

        ## after cleaning
        print("After cleaning...\n")
        print("Uniqueness: " + str(duplicate_score2))
        print("Comleteness: " + str(emptiness_score2))
        # print("Consistency: " + str(inconsistent_type_score2))

        context = {
            "unique": duplicate_score,
            "complete": emptiness_score,
            "consistent": inconsistent_type_score,
            "unique2": duplicate_score2,
            "complete2": emptiness_score2,
            # "consistent2": inconsistent_type_score2,
        }

    # return render(request,'upload_file.html', context={'radar_chart_image': radar_chart_image})
    return render(request, 'upload_file.html', context=context)


def calculate_duplicate_score(df):
    duplicates = df[df.duplicated()]

    total_entries = len(df)
    duplicate_percentage = (len(duplicates) / total_entries) * 100

    duplicate_score = 100 - duplicate_percentage

    if duplicate_score == 100:
        return format(duplicate_score, ".1f")
    else:
        return format(duplicate_score, ".2f")


def calculate_emptiness(df):
    null_values = df.isnull().sum().sum()

    empty_cells = (df.applymap(lambda x: x == '') | df.applymap(lambda x: x == ' ')).sum().sum()

    total_entries = df.size
    null_percentage = (null_values / total_entries) * 100
    empty_percentage = (empty_cells / total_entries) * 100

    null_empty_score = 100 - (null_percentage + empty_percentage)
    # score = format(num, ".2f")

    if null_empty_score == 100:
        return format(null_empty_score, ".1f")
    else:
        return format(null_empty_score, ".2f")


def calculate_type_inconsistency(df):

    inconsistent_types = df.applymap(type).nunique()

    total_columns = len(df.columns)
    inconsistent_type_percentage = (sum(inconsistent_types > 1) / total_columns) * 100

    inconsistent_type_score = 100 - inconsistent_type_percentage

    if inconsistent_type_score == 100:
        return format(inconsistent_type_score, ".1f")
    else:
        return format(inconsistent_type_score, ".2f")


# # unique value count tells us if the data is variant enough for a good analysis to be performed
# def calculate_uniqueness(df):
#     # Calculate the number of unique values in each column
#     unique_values_per_column = df.nunique()
#
#     # Calculate the percentage of unique values for each column
#     total_columns = len(df.columns)
#     unique_values_percentage_per_column = (unique_values_per_column / df.shape[0]) * 100
#
#     # Calculate the average percentage across all columns
#     average_unique_values_percentage = unique_values_percentage_per_column.mean()
#
#     # Calculate the score
#     unique_values_score = average_unique_values_percentage
#
#     if unique_values_score == 100:
#         return format(unique_values_score, ".1f")
#     else:
#         return format(unique_values_score, ".2f")


# ---------------------------------- DATA CLEANING --------------------------

def clean_dataframe(df):
    # Remove duplicates
    df = df.drop_duplicates()

    # Handle null values and empty cells
    df = df.fillna(0)

    # # Determine column type based on majority type and assign all rows under that column to the same type
    # for column in df.columns:
    #     majority_type = df[column].apply(lambda x: type(x)).mode()[0]
    #     df[column] = df[column].astype(majority_type)

    return df
