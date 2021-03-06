import csv

def change_date_format(raw_day_of_service):

    raw_day_of_service = raw_day_of_service.split()[0]
    date_split = raw_day_of_service.split("-")

    month_dict = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

    yyyy = "20"+date_split[2]
    mm = month_dict[date_split[1]]
    dd = date_split[0]

    day_of_service = str(yyyy) + "-" + str(mm) + "-" + str(dd)

    return day_of_service


with open("/home/stephen/Documents/College/Group_project/Sample_data/sorted_10000_rt_vehicles_DB_2018.csv", "r") as read_file:
    with open('reformatted_sorted_10000_rt_vehicles_DB_2018.csv','w') as write_file:
        reader = csv.reader(read_file, delimiter=';')
        writer = csv.writer(write_file, delimiter=',',lineterminator='\n',)
        header = next(reader, None)
        #writer.writerow(header)

        for row in reader:

            raw_day_of_service = row[1]
            day_of_service = change_date_format(raw_day_of_service)

            raw_last_update = row[5]
            raw_last_update_date = raw_last_update.split()[0]

            last_update_time = raw_last_update.split()[1]
            last_update_date = change_date_format(raw_last_update_date)

            last_update = str(last_update_date) + " " + str(last_update_time)
            print(raw_last_update, last_update)

            if row[6]:
                note = row[6]
            else:
                note = ''

            writer.writerow([row[0],day_of_service,row[2],row[3],row[4],last_update,row[6]])
