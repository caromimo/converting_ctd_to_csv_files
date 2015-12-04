import csv
import glob

for ctd_file in glob.glob("*.ctd"):
    with open(ctd_file) as my_file:
        name_without_extention = ctd_file.split(".")[0]
        with open ("{}.csv".format(name_without_extention), "w") as csvfile:
            csv_output = csv.writer(csvfile, delimiter = ",")
            seen_header = False
            in_channels = False
            headers = []
            for line in my_file:

        #This section is to build an array of headers out Table: Channels section
                if "$TABLE: CHANNELS" in line:
                    in_channels = True
                    continue
                if "$END" in line:
                    in_channels = False
                    continue
                if in_channels:
                    column_description = line.split()
                    if column_description[0].isdigit():
                        headers.append(column_description[1])

        #This section extracts the lat, long and depth
                if "LATITUDE" in line:
                    latitude = line.split(":")[1].strip()
                if "LONGITUDE" in line:
                    longitude = line.split(":")[1].strip()
                if "WATER DEPTH" in line:
                    depth = line.split(":")[1].strip()

        #This section is to extract the data
                if "START TIME" in line:
                    date, time = line.strip().split()[-2:]
                if line.startswith("*END OF HEADER"):
                    seen_header = True
                    headers.extend(["date","time", "latitude", "longitude", "depth"])
                    csv_output.writerow(headers)
                    continue
                if seen_header:
                    entry = line.strip().split()
                    entry.extend([date, time, latitude, longitude, depth])
                    csv_output.writerow(entry)
