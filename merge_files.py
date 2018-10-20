import scipy.io
import numpy as np
from collections import defaultdict
import pyexcel
from patient import Patient
import pickle
import numpy as np
import csv
import sys


def compute(filename_master, filename_corrected, filename_xlsx):
    data_mat, location_master = readfile_qrsData(filename_master, filename_corrected)

    data_xlsx, case_coord_data = readfile_xlsx(filename_xlsx)

    # find_correlation(data_mat, data_xlsx)
    coorelation = mapping(data_mat, data_xlsx)
    patient_objects = []
    keyset = data_mat.keys()
    with open('persons.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        # filewriter.writerow(['PatientID','PacingID','Record','Status','Action'])
        for patient_id in sorted(keyset):
            object = Patient(patient_id, list(data_mat[patient_id].keys()), list(data_mat[patient_id].values()),
                             coorelation[patient_id], data_mat[patient_id], data_xlsx,
                             case_coord_data[coorelation[patient_id]], location_master, filewriter)
            patient_objects.append(object)

    with open("data.pickle", "wb") as f:
        pickle.dump(patient_objects, f)
    f.close()

    return patient_objects


def find_correlation(data_mat, data_xlsx):
    correlation = {}
    for patient_id in data_mat.keys():
        samples_count = len(data_mat[patient_id])
        for case_number in data_xlsx.keys():
            case_count = len(data_xlsx[case_number])
            if case_count == samples_count:
                if patient_id in correlation.keys():
                    temp_list = correlation[patient_id]
                    temp_list.append(case_number)
                    correlation[patient_id] = temp_list
                else:
                    correlation[patient_id] = [case_number]
    # for key in correlation.keys():
    #     print(key,correlation[key])
    for patient_id in correlation.keys():
        if len(correlation[patient_id]) > 2:
            # print(patient_id)
            correlated_list = correlation[patient_id]
            for case_number in correlated_list:
                matching = compare_pacingid(data_mat[patient_id], data_xlsx[case_number])
                print(patient_id, case_number, matching)


def compare_pacingid(mat_data, xlsx_data):
    matching = 0

    for pacing_id in mat_data.keys():
        for case_pace in xlsx_data.keys():
            pacing_id = [round(elem, 4) for elem in pacing_id]
            # print(case_pace,pacing_id)
            if case_pace == pacing_id:
                matching + 1
    return matching


def mapping(data_mat, data_xlsx):
    correlation = {}
    final = {}
    for patient_id in data_mat.keys():
        for pacing_coord in data_mat[patient_id].keys():
            for case_number in data_xlsx.keys():
                for case_coord in data_xlsx[case_number].keys():
                    if case_coord == pacing_coord:
                        # print('{} ==== {}'.format(patient_id, case_number))
                        if patient_id in correlation.keys():
                            if case_number in correlation[patient_id].keys():
                                count = correlation[patient_id][case_number]
                                correlation[patient_id][case_number] = count + 1
                            else:
                                correlation[patient_id][case_number] = 1
                        else:
                            correlation[patient_id] = {case_number: 1}
    for patient_id in correlation.keys():
        for case_number in correlation[patient_id].keys():

            if len(data_mat[patient_id]) == correlation[patient_id][case_number]:
                # print('{} {} {}=={} '.format(patient_id, case_number, correlation[patient_id][case_number],
                #                              len(data_mat[patient_id])))
                final[patient_id] = case_number

    return final


def readfile_xlsx(filename_xlsx):
    patient_data = {}
    case_coord_data = {}

    my_array = pyexcel.get_array(file_name=filename_xlsx)
    for record in my_array[2:1014]:
        case_number = record[2]
        # print(i)
        file_name = record[1]
        coord = [round(record[9], 4), round(record[10], 4), round(record[11], 4)]
        if case_number in patient_data.keys():
            patient_data[case_number][tuple(coord)] = file_name
            case_coord_data[case_number][file_name] = coord

        else:
            patient_data[case_number] = {tuple(coord): file_name}
            case_coord_data[case_number] = {file_name: coord}

    return patient_data, case_coord_data


def readfile_qrsData(filename_master, filename_corrected):
    mat = scipy.io.loadmat(filename_master)

    train_x = mat['train_x']
    train_y = mat['train_y']
    train_coord = mat['train_coord']
    val_x = mat['val_x']
    val_y = mat['val_y']
    val_coord = mat['val_coord']
    test_x = mat['test_x']
    test_y = mat['test_y']
    test_coord = mat['test_coord']
    mean_x = mat['mean_x']
    std_x = mat['std_x']

    coord_corrected = scipy.io.loadmat(filename_corrected)
    size_test = 0
    data_coord_corrected = coord_corrected['data_coord']
    size_train = len(train_x)
    size_test = len(test_x)
    size_val = len(val_x)

    data_coord_train = data_coord_corrected[size_val + size_test:size_val + size_test + size_train]
    data_coord_test = data_coord_corrected[size_val:size_val + size_test]
    data_coord_val = data_coord_corrected[:size_val]

    master_data_x = np.concatenate((train_x, test_x, val_x), axis=0)
    master_data_y = np.concatenate((train_y, test_y, val_y), axis=0)
    master_data_coord = np.concatenate((data_coord_train, data_coord_test, data_coord_val), axis=0)
    scipy.io.savemat("master_data.mat",
                     {'x': master_data_x, 'y': master_data_y, 'coord': master_data_coord, 'mean': mean_x, 'std': std_x})

    location_master = defaultdict(list)
    master_index = 0
    patient_data = defaultdict(list)
    patient_data, master_index, location_master = group_by_patientID(train_x, train_y, train_coord, data_coord_train,
                                                                     patient_data, master_index, location_master)
    patient_data, master_index, location_master = group_by_patientID(test_x, test_y, test_coord, data_coord_test,
                                                                     patient_data, master_index, location_master)
    patient_data, master_index, location_master = group_by_patientID(val_x, val_y, val_coord, data_coord_val,
                                                                     patient_data, master_index, location_master)

    # for data in patient_data.keys():
    #     print(data,len(location_master[data].keys()),len(patient_data[data].keys()))

    return patient_data, location_master


def group_by_patientID(X, Y, coord, corrected_coord, patient_data, master_index, location_master):
    pacing_site = {}
    for i in range(len(X)):
        pacing_coord_raw = corrected_coord[i].tolist()
        pacing_coord = tuple([round(elem, 8) for elem in pacing_coord_raw])
        if Y[i][1] in patient_data.keys():
            if pacing_coord in patient_data[Y[i][1]].keys():
                pacing_site_samples = patient_data[Y[i][1]][(pacing_coord)]
                sample_x = X[i].tolist()
                if len(pacing_site_samples) == 1200:
                    merge = [pacing_site_samples, sample_x]
                    patient_data[Y[i][1]][pacing_coord] = merge
                else:
                    pacing_site_samples.append(sample_x)
                    patient_data[Y[i][1]][pacing_coord] = pacing_site_samples

                if pacing_coord in location_master[Y[i][1]].keys():
                    # print('pacing present')
                    index_list = location_master[Y[i][1]][pacing_coord]
                    index_list.append(master_index)
                    master_index += 1
                    location_master[Y[i][1]][pacing_coord] = index_list
                else:
                    # print('pacing not present')
                    location_master[Y[i][1]][pacing_coord] = [master_index]
                    master_index += 1

            else:

                samples = X[i].tolist()
                # pacing_site={(pacing_coord): samples}
                patient_data[Y[i][1]][pacing_coord] = samples

                # location_master[Y[i][1]] = {pacing_coord: [master_index]}
                # master_index += 1

        else:
            # print('patient present')
            samples = X[i].tolist()

            patient_data[Y[i][1]] = {pacing_coord: samples}

            location_master[Y[i][1]] = {pacing_coord: [master_index]}
            master_index += 1

    return patient_data, master_index, location_master


if __name__ == '__main__':
    filename_master = sys.argv[1]
    filename_corrected = sys.argv[2]
    filename_xlsx = sys.argv[3]

    compute(filename_master, filename_corrected, filename_xlsx)
