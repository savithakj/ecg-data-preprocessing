from data_cleaning_complete_set import compute
import itertools
from pacing_coord import Pacing_Coord
import csv


class Patient:
    def __init__(self, patient_id, pacing_coord, pacing_samples, casenumber, pacing_coord_sample,
                 xlsx_data, case_coord_data_list, location_master, filewriter):
        # print('here')
        self.id = patient_id
        pacing_samples = list(itertools.chain.from_iterable(pacing_samples))

        self.pacing_samples = pacing_samples
        self.case_number = casenumber

        self.pacing_coord_samples = pacing_coord_sample

        incorrect_record_list = compute(pacing_samples)
        self.stat = round((len(incorrect_record_list) / len(pacing_samples)) * 100, 3)

        coords = []
        for pacing_sample in pacing_coord:
            coords.append(Pacing_Coord(pacing_sample, pacing_coord_sample[pacing_sample], xlsx_data, casenumber,
                                       case_coord_data_list, location_master[patient_id]))
        self.pacing_coord = coords

        for coord in coords:
            for i in range(len(coord.samples_index)):
                filewriter.writerow(
                    [patient_id, coord.pacingSite, coord.samples_index[i], coord.samples_stat[i], 'No Action'])
