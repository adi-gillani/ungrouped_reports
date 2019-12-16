from useful_functions import gather_data
from useful_functions import get_date_time
from useful_functions import get_timestamp
from useful_functions import get_month
from useful_functions import dict_to_csv

# Using the questionnaire ID and timestamps to extract required data
b2b_fsd = gather_data("124", 1572566400000, 1575072000000)

# To check how many results are returned
print(len(b2b_fsd))

# Creating a list of dictionaries to store Key:Value data pairs for each required attribute
final_list = []
for i in b2b_fsd:
    fb_creation_date = (get_date_time(i['feedback_action']['created_at'])) if i['feedback_action'] is not None else \
        get_date_time("2019-11-26T10:01:28.003024Z")
    survey_creation_date = get_date_time(i['created_at']) if i['feedback_action'] is not None else get_date_time(
        "2019-11-26T10:01:28.003024Z")
    neg_param = [b['option']['text'] for a in i['detail'] if a['id'] == 1815
                 for b in a['options'] if i['questionnaire'] == 124]
    #     neg_drill = [c['option']['text'] for a in i['detail'] if a['id'] in [2013, 190, 137, 133, 127, 116, 109]
    #                  for b in a['options'] for c in b['option']['sub_options'] if i['questionnaire'] in
    #                  [15, 17, 19, 20, 21, 31, 173]]
    neg_detail = [b['other_text'] for a in i['detail'] if a['id'] == 1815
                  for b in a['options'] if i['questionnaire'] == 124]
    prod_not_received = [b['other_text'] for a in i['detail'] if a['id'] == 1818
                         for b in a['options'] if i['questionnaire'] == 124]
    on_time_delivery = [b['option']['text'] for a in i['detail'] if a['id'] == 1816
                        for b in a['options'] if i['questionnaire'] == 124]
    in_full_delivery = [b['option']['text'] for a in i['detail'] if a['id'] == 1817
                        for b in a['options'] if i['questionnaire'] == 124]
    continue_business = [b['option']['text'] for a in i['detail'] if a['id'] == 1819
                         for b in a['options'] if i['questionnaire'] == 124]
    employee_first_name = [a['user']['first_name'] for a in i['feedback_remark'] if i['feedback_remark'] is not None]
    employee_last_name = [a['user']['last_name'] for a in i['feedback_remark'] if i['feedback_remark'] is not None]
    data_dict = {
        "Feedback ID": i['id'],
        "Customer ID": i['customer']['id'] if i['customer']['id'] is not None else "",
        "Date": i['created_at'][:10],
        "Timestamp": get_timestamp(i['created_at']),
        "Month": get_month(i['created_at']),
        "Research Module": i['group']['title'],
        "Store": i['division']['primary']['title'],
        "Department": i['division']['feedback_division']['title'] if
        i['division']['feedback_division'] is not None else "",
        "Respondent Name": i['customer']['name'],
        "Company ID": i['company']['id'] if i['company'] is not None else "",
        "Company Name": i['company']['name'] if i['company'] is not None else "",
        "Respondent Phone Number": i['customer']['cell_phone'],
        "Customer Manager": i['invite']['manager'] if i['invite'] is not None else "",
        "NPS Score": i['score'],
        "NPS Segment": i['score_label'],
        "Recovery Status": i['feedback_action']['type'] if i['feedback_action'] is not None else "",
        "Recovery Time (Hrs.)": round(((fb_creation_date - survey_creation_date).total_seconds()) / 3600, 3),
        "Negative Parameter": ', '.join(neg_param) if neg_param is not None else "",
        "Negative Detail": str(', '.join(filter(None, neg_detail))) if neg_detail is not None else "",
        "Was your last order delivered on time": ", ".join(on_time_delivery) if on_time_delivery is not None else "",
        "Was your last order delivered in full": ", ".join(in_full_delivery) if in_full_delivery is not None else "",
        "Please mention the name of product not received": ', '.join(prod_not_received) if prod_not_received is not None
        else "",
        "Would you like to buy from METRO again": ", ".join(continue_business) if continue_business is not None else "",
        "Respondent Comment": i['comment'],
        "Employee Comment": i['feedback_remark'][0]['text'] if i['feedback_remark'] != [] else "",
        "Employee Name": ', '.join(employee_first_name) + " " + ', '.join(employee_last_name) if
        ', '.join(employee_first_name) != "" and ', '.join(employee_last_name) != "" else "",
        "Feedback Transaction": i['feedback_transaction']
    }
    final_list.append(data_dict)

dict_to_csv(final_list, "B2B - FSD Ungrouped Report")
