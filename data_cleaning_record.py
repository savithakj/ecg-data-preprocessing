"""
author: Varun Rajiv Mantri
"""

from matplotlib import pyplot as plt


def file_reader(file_name):
    '''
    This method reads in the data from a csv file
    :param file_name:name of the input file
    :return:
    '''
    complete_data = []
    with open(file_name) as file:
        for row in file:
            row = row.strip()
            row = row.split(",")
            complete_data.append(row)
    return complete_data


def peak_finder(row, mean):
    '''
    This method finds the peaks
    :param row: record under consideration
    :param mean: mean value for that record
    :return: peaks
    '''
    peaks = []
    previous = abs(float(row[0]))
    current = abs(float(row[1]))
    next_item = abs(float(row[2]))
    biggest_peak = 0
    for index in range(3, len(row) - 1):
        if current > previous and current > next_item and current > (mean + 5):
            peaks.append(index)
        previous = current
        current = abs(float(row[index]))
        if current > biggest_peak:
            biggest_peak = current
        next_item = abs(float(row[index + 1]))
    return peaks, biggest_peak


def mean_calculator(row):
    mean = 0
    for value in row:
        mean = mean + float(value)
    mean = round(mean / len(row), 3)
    return mean


def rejection_condition_two(row):
    '''
    This method looks for peaks and counts only those peaks that have sudden falls at precisely same location
    across more than 5 leads
    :param complete_data: Complete input data
    :return: Bad data list
    '''
    lower_limit = 0
    upper_limit = 100
    leads = 0
    location_recorder = [False for _ in range(12)]
    index_recorder = [False for _ in range(12)]
    while leads < 12:
        max_peak = float("-inf")
        for index in range(lower_limit, upper_limit):
            if float(row[index]) > max_peak:
                max_peak = float(row[index])
                location = index
        lower_limit = upper_limit
        upper_limit = upper_limit + 100

        mean = mean_calculator(row)
        # checking if the next value is the biggest
        if location + 1 < 1200:
            if float(row[location + 1]) < (mean + 5):
                location_recorder[leads] = True
                index_recorder[leads] = location - lower_limit
        if location - 1 >= 0:
            if float(row[location - 1]) < (mean + 5):
                location_recorder[leads] = True
                index_recorder[leads] = location - lower_limit
        leads = leads + 1
    max_count = 0
    for index in range(len(index_recorder) - 1):
        current = index_recorder[index]
        counter = 0
        for index_1 in range(index, len(index_recorder)):
            if current == index_recorder[index_1]:
                counter = counter + 1
        if max_count < counter:
            max_count = counter
            value = current
    counter = 0
    for index in range(len(index_recorder)):
        if index_recorder[index] == value:
            if location_recorder[index] == True:
                counter = counter + 1
    if counter >= 5:
        return True
    return False


def rejection_condition_one(row):
    '''
    This method rejects the records
    :param complete_data:
    :return: correct and incorrect records list
    '''
    flag = False
    mean = 0
    for value in row:
        mean = mean + float(value)
    mean = round(mean / len(row), 3)
    count = 0
    upper_limit = 100
    lower_limit = 0
    # finding peaks
    peaks, biggest_peak = peak_finder(row, mean)
    mid_value = (mean + biggest_peak) / 2
    while (count < 12):
        for i in range(lower_limit, lower_limit + 9):
            # cheking first five
            if abs(float(row[i])) >= mean + mid_value:
                flag = True
                break
        for i in range(upper_limit - 1, upper_limit - 10, -1):
            # cheking first five
            # print(upper_limit)
            if abs(float(row[i])) >= mean + mid_value:
                flag = True
                break
        if flag == True:
            break
        count = count + 1
        lower_limit = upper_limit
        upper_limit = upper_limit + 100
    for index in peaks:
        if round(float(row[index + 1])) == 0:
            flag = True
        elif round(float(row[index - 1])) == 0:
            flag = True
    if flag == True:
        return True
    return False


def plotter(data, fig):
    lower_limit = 0
    upper_limit = 100
    figure_count = 1
    plt.figure(fig)
    row = 1
    col = 1
    for _ in range(12):
        temp = []
        for index in range(lower_limit, upper_limit):
            temp.append(float(data[index]))
        plt.subplot(4, 3, figure_count)
        plt.plot(temp)
        plt.title("Lead" + str(figure_count))
        lower_limit = upper_limit
        upper_limit = upper_limit + 100
        figure_count = figure_count + 1


def combine(incorrect_record_list, bad_list):
    dicto = {}
    for item in incorrect_record_list:
        dicto[item] = True
    for item in bad_list:
        if item not in dicto.keys():
            dicto[item] = True
    complete_list = []
    for item in dicto.keys():
        complete_list.append(item)
    return complete_list


def check_quality(record):
    status = rejection_condition_one(record)
    if status == False:
        status = rejection_condition_two(record)
    if status == False:
        return 'good'
    else:
        return 'bad'


'''
def main():
    complete_data=file_reader("train_x.csv")
    check_quality(record)
    incorrect_record_list,correct_records=rejection_condition_one(complete_data)
    bad_list=rejection_condition_two(complete_data)
    incorrect_record_list=combine(incorrect_record_list,bad_list)
    print("-----------------------------------")
    print("Incorrect record ID's: ")
    print(incorrect_record_list)
    print("Correct record ID's:")
    print(correct_records)
    print("\n\nPercentage of records that are wrong:"+str(round((len(incorrect_record_list)/len(complete_data))*100,3))+"%")
    print("-----------------------------------")
    plotter(complete_data[correct_records[8]],0)
    plt.title("Good Records")
    plotter(complete_data[incorrect_record_list[8]], 1)
    plt.title("Bad Records")
    plt.show()
'''


# main()
