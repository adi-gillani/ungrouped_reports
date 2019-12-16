import requests
import csv
from csv import DictWriter
from datetime import datetime


# Function to loop over the API to get results
def api_request_generator(api_endpoint, auth_credentials, count=0):
    endpoint_request = requests.get(api_endpoint, auth=auth_credentials)
    endpoint_json = endpoint_request.json()
    next_url = endpoint_json['next']
    results = [item['serialized_data'] for item in endpoint_json['results'] if item['serialized_data'] != {}]
    if next_url is None:
        print("url number", count)
        return results
    return results + api_request_generator(next_url, auth_credentials, count + 1)


# Function to extract data from the API
def gather_data(questionnaire_id, unix_start_date, unix_end_date):
    # group = group_id
    questionnaire = questionnaire_id  # 25,14,124,
    start = unix_start_date  # UNIX Timestamp
    end = unix_end_date  # UNIX Timestamp
    api_key = "1551c8fd-88df-411f-b7e4-493d7ff2bc58"  # API Key
    authentication_credentials = ("metro.sentimeter", "arbisoft")  # Authentication Credentials
    main_url = "https://apistg.sentimeter.io/api/organizations/2/feedback/detail-list/?" \
               "questionnaire={}&api_key={}&start_date={}&end_date={}". \
        format(
            questionnaire, api_key, start, end
                )
    total_data = api_request_generator(main_url, authentication_credentials)
    return total_data

# We use api_request_generator inside the gather_data function to extract data from the API ###


# Function for converting string timestamp into datetime format
def get_date_time(datetime_string):
    string_date = datetime_string
    first_split = string_date.split("T")
    stripped_time = first_split[1][:8]
    clean_datetime_string = first_split[0] + " " + stripped_time
    converted_date_time = datetime.strptime(clean_datetime_string, '%Y-%m-%d %H:%M:%S')
    return converted_date_time


def get_timestamp(unix_timestamp):
    first = unix_timestamp.split("T")
    second = first[1][:8]
    final = first[0] + " " + second
    return final


def get_month(unix_timestamp):
    first = unix_timestamp.split("T")
    second = first[0][5:7]
    return second


# Function for exporting data to csv
def export_to_csv(data_list, file_name, headers):
    with open(file_name + ".csv", "w", newline="") as my_csv_file:
        wr = csv.writer(my_csv_file)
        wr.writerow(headers)
        wr.writerows(data_list)


# Function to export dictionary as a CSV
def dict_to_csv(data_list, file_name):
    with open(file_name + '.csv', 'w', newline='', encoding='utf-8') as output_file:
        header_keys = data_list[0].keys()
        writer = DictWriter(output_file, header_keys)
        writer.writeheader()
        writer.writerows(data_list)