import csv
import glob
from datetime import datetime


def process_file():
    data = []
    for filename in glob.glob("csse_covid_19_data/csse_covid_19_daily_reports/*.csv"):
        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            reader.next()  # skip header
            data.extend(list(reader))

    for row in data:
        if len(row) <= 8:
            row[2] = format_date(row[2])
            del row[6:]  # some files have lat/long
            row.append('')
        else: # change of format on March 23rd
            admin = row[1]
            row[0], row[1] = row[2], row[3]
            row[2] = format_date(row[4])
            row[3], row[4], row[5] = row[7], row[8], row[9]
            row[6] = admin
            del row[7:]

    with open("data.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def format_date(date_field):
    try:
        update_dt = datetime.strptime(date_field, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            update_dt = datetime.strptime(date_field, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # month day without padding zeroes not supported in Linux
            padded = "/".join(
                [part if len(part) >= 2 else "0" + part for part in date_field.split("/")]
            )
            try:
                update_dt = datetime.strptime(padded, "%m/%d/%Y %H:%M")
            except ValueError:
                update_dt = datetime.strptime(padded, "%m/%d/%y %H:%M")
    return update_dt.strftime("%Y-%m-%d")


if __name__ == "__main__":
    process_file()
