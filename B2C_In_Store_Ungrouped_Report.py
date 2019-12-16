from useful_functions import gather_data
from useful_functions import get_date_time
from useful_functions import get_timestamp
from useful_functions import get_month
from useful_functions import dict_to_csv

# Using the questionnaire ID and timestamps to extract required data
b2c_in_store = gather_data("15|17|19|20|21|31|173", 1572566400000, 1575072000000)

# To check how many results are returned
print(len(b2c_in_store))

# Creating a list of dictionaries to store Key:Value data pairs for each required attribute
final_list = []
for i in b2c_in_store:
    fb_creation_date = (get_date_time(i['feedback_action']['created_at'])) if i['feedback_action'] is not None else \
        get_date_time("2019-11-26T10:01:28.003024Z")
    survey_creation_date = get_date_time(i['created_at']) if i['feedback_action'] is not None else get_date_time(
        "2019-11-26T10:01:28.003024Z")
    pos_param = [b['option']['text'] for a in i['detail'] if a['id'] in [110, 134, 117, 128, 138, 189]
                 for b in a['options'] if i['questionnaire'] in [15, 17, 19, 20, 21, 31, 173] and
                 b['option']['text'] is not None and i['score'] is not None or i['score'] in [9, 10]]
    neg_param = [b['option']['text'] for a in i['detail'] if a['id'] in [2013, 190, 137, 133, 127, 116, 109]
                 for b in a['options'] if i['questionnaire'] in [15, 17, 19, 20, 21, 31, 173]]
    neg_drill = [c['option']['text'] for a in i['detail'] if a['id'] in [2013, 190, 137, 133, 127, 116, 109]
                 for b in a['options'] for c in b['option']['sub_options'] if i['questionnaire'] in
                 [15, 17, 19, 20, 21, 31, 173]]
    neg_detail = [c['other_text'] for a in i['detail'] if a['id'] in [2013, 190, 137, 133, 127, 116, 109]
                  for b in a['options'] for c in b['option']['sub_options'] if i['questionnaire'] in
                  [15, 17, 19, 20, 21, 31, 173]]
    employee_first_name = [a['user']['first_name'] for a in i['feedback_remark'] if i['feedback_remark'] is not None]
    employee_last_name = [a['user']['last_name'] for a in i['feedback_remark'] if i['feedback_remark'] is not None]
    data_dict = {
        "Feedback ID": i['id'],
        "Customer ID": i['customer']['id'] if i['customer']['id'] is not None else "",
        "Date": i['created_at'][:10],
        "Timestamp": get_timestamp(i['created_at']),
        "Month": get_month(i['created_at']),
        "Research Module": i['group']['title'],
        "Division|Primary": i['division']['primary']['title'],
        "Feedback Division": i['division']['feedback_division']['title'] if
        i['division']['feedback_division'] is not None else "",
        "Respondent Name": i['customer']['name'],
        "Respondent Phone Number": i['customer']['cell_phone'],
        "Gender": i['gender'],
        "Age": i['age'],
        "NPS Score": i['score'],
        "NPS Segment": i['score_label'],
        "Recovery Status": i['feedback_action']['type'] if i['feedback_action'] is not None else "",
        "Recovery Time (Hrs.)": round(((fb_creation_date - survey_creation_date).total_seconds()) / 3600, 3),
        "Loop": i['loop'],
        "Respondent Comment": i['comment'],
        "Employee Comment": i['feedback_remark'][0]['text'] if i['feedback_remark'] != [] else "",
        "Positive Parameter": ', '.join(pos_param) if pos_param is not None else "",
        "Negative Parameter": ', '.join(neg_param) if neg_param is not None else "",
        "Negative Drill Down": ', '.join(neg_drill) if neg_drill is not None else "",
        "Negative Detail": str(', '.join(filter(None, neg_detail))) if neg_detail is not None else "",
        "Taker": i['taker']['type'],
        "Reachable Customer": i['customer']['is_reachable'],
        "Employee Name": ', '.join(employee_first_name) + " " + ', '.join(employee_last_name) if
        ', '.join(employee_first_name) != "" and ', '.join(employee_last_name) != "" else ""
    }
    final_list.append(data_dict)
print(final_list[0])

# exporting to csv using DictWriter
dict_to_csv(final_list, "B2C In Store Ungrouped Report")
