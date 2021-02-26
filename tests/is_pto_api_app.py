"""
API tests to check accuracy for is pto app

"""

import requests
import csv

def read_csv():
    "Reading the CSV file"
    pto_text = []
    with open('pto-reasons-with-label.csv') as pto_file:
        for each_row in pto_file:
            pto_text.append(each_row.split(','))
    with open('pto-reasons-with-label.csv') as pto_file:
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


def calucalte_precision(pto_text, url):
    "Precision calculation"
    total_positive_predicted_message_correctly = 0
    total_positive_predicted_message = 0
    total_positive_message_not_predicted_correctly = 0
    total_false_positive = 0
    for each_precision_text in pto_text:
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
    precision = round(total_positive_predicted_message_correctly/(total_positive_predicted_message_correctly + total_false_positive),2)

    return precision, total_positive_message_not_predicted_correctly, total_positive_predicted_message_correctly


if __name__ == "__main__":
    pto_text,message_length = read_csv()
    url = "https://practice-testing-ai-ml.qxf2.com/is-pto"
    response = requests.get(url)
    #Accuracy calculation
    accuracy = round(calculate_accuracy(pto_text, url, message_length),2)
    print(f'accuracy: {accuracy}')
    #Precision calculation
    precision,false_negative, true_positive = calucalte_precision(pto_text, url)
    print(f'Precision:{precision}')
    #Recall Calculation
    recall = round(true_positive/(true_positive+false_negative),2)
    print(f'Recall:{recall}')
    f1_score = round(2 *((precision*recall)/(precision+recall)),2)
    print(f'F1 Score:{f1_score}')
