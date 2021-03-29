import pytest
import csv, requests
import os, sys

def read_csv():
    "Reading the CSV file"
    pto_text = []
    csv_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','conf/pto-reasons-with-label.csv'))
    with open(csv_file) as pto_file:
        for each_row in pto_file:
            pto_text.append(each_row.split(','))
    with open(csv_file) as pto_file:
        length_of_rows = csv.reader(pto_file)
        length_of_rows = len(list(length_of_rows))

    return pto_text, length_of_rows

def calculate_accuracy(pto_text, url, total_message_length):
    "Accuracy calculation"
    total_score = 0
    for each_text in pto_text:
        url = url
        data = {'message': each_text}
        response = requests.post(url,data=data)
        actual_score = each_text[1]
        actual_score = actual_score.strip()
        if response.json()['score'] == int(actual_score):
            total_score += 1
    accuracy = total_score/total_message_length
    return accuracy


def calcualte_true_false_val(redf_pto_text, url):
    "Calculate true positive, false negative, false positive"
    total_positive_predicted_message_correctly = 0
    total_positive_predicted_message = 0
    total_positive_message_not_predicted_correctly = 0
    total_false_positive = 0
    for each_precision_text in redf_pto_text:
        data = {'message': each_precision_text[0]}
        positive_predicited_message = each_precision_text[1]
        positive_predicited_message = positive_predicited_message.strip()
        if int(positive_predicited_message) == 1:
            total_positive_predicted_message +=1
            response = requests.post(url, data=data)
            if response.json()['score'] == int(positive_predicited_message):
                #True Positive
                total_positive_predicted_message_correctly += 1
            else:
                #False Negative
                total_positive_message_not_predicted_correctly += 1
        else:
            if response.json()['score'] == 1:
                #False Positive
                total_false_positive +=1

    return total_positive_message_not_predicted_correctly, total_positive_predicted_message_correctly,total_false_positive


def cal_score_val(redf_false_negative, redf_true_positive, redf_false_positive):
    "Calculate precision, recall, F1score"
    precision = round(redf_true_positive/(redf_true_positive + redf_false_positive),2)
    print(f'Precision:{precision}')
    #Recall Calculation
    recall = round(redf_true_positive/(redf_true_positive+redf_false_negative),2)
    print(f'Recall:{recall}')
    f1_score = round(2 *((precision*recall)/(precision+recall)),2)
    print(f'F1 Score:{f1_score}')

    return precision, recall, f1_score


def test_snapshot_accuracy(snapshot):
    len_of_args = len(sys.argv)
    pto_text,message_length = read_csv()
    if len_of_args == 4:
        app_url = sys.argv[4]
    else:
        app_url = "https://practice-testing-ai-ml.qxf2.com/is-pto"
    response = requests.get(app_url)

    accuracy = round(calculate_accuracy(pto_text,app_url,message_length),2)

    false_negative, true_positive,false_positive = calcualte_true_false_val(pto_text, app_url)

    precision,recall,f1_score = cal_score_val(false_negative, true_positive, false_positive)

    #Creating snapshot directory
    snapshot.assert_match(f"{accuracy},{precision},{recall},{f1_score}","overall_score.txt")

