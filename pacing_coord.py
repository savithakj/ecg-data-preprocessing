from data_cleaning_complete_set import compute
from data_cleaning_record import check_quality


class Pacing_Coord:
    def __init__(self, pacing_site, pacing_site_samples, coord_filename_mapping, case_number, case_coord_data_list,
                 location_list):
        # print('there')
        # print(pacing_site in location_list.keys())
        self.pacingSite = self.find_serial_numbers(pacing_site, case_coord_data_list)
        incorrect_record_list = compute(pacing_site_samples)
        self.stats = round((len(incorrect_record_list) / len(pacing_site_samples)) * 100, 3)
        self.samples = pacing_site_samples

        result = []
        for pacing_site_sample in pacing_site_samples:
            status = check_quality(pacing_site_sample)
            result.append(status)
        self.samples_stat = result
        # print(location_list)
        self.samples_index = location_list[pacing_site]

        self.file_name = self.find_filename(coord_filename_mapping, pacing_site, case_number)

    def find_filename(self, coord_filename_mapping, pacing_site, case_number):

        return coord_filename_mapping[case_number][tuple(pacing_site)]

    def find_serial_numbers(self, pacing_site, case_coord_data_list):
        serial = []
        # print(case_coord_data_list)
        for data in case_coord_data_list.keys():
            # print(type(pacing_site),type(case_coord_data_list[data]))
            if pacing_site == tuple(case_coord_data_list[data]):
                serial.append(data)
        # print(pacing_site,serial)
        return serial
