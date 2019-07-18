import csv

with open("../csvs/weather2018.csv", "r") as read_file:
    with open('../csvs/reformatted_weather2018.csv','w') as write_file:
        reader = csv.reader(read_file, delimiter=',')
        writer = csv.writer(write_file, delimiter=',',lineterminator='\n',)
        header = next(reader, None)
        #writer.writerow(header)

        for row in reader:
            writer.writerow([row[0],row[2],row[4],row[6],row[7],row[8],row[9],row[10]])
