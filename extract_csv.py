import csv
import json


def convert_csv_to_json(csv_file, json_file, batch_size=10000):
    with open(csv_file, 'r') as file:
        csv_data = csv.DictReader(file)
        data = []
        counter = 0

        for row in csv_data:
            data.append(row)
            counter += 1

            # Menulis data ke file JSON dalam batch
            if counter % batch_size == 0:
                write_batch_to_json(data, json_file, append=True)
                data = []

        # Menulis sisa data yang belum terproses dalam batch terakhir
        if data:
            write_batch_to_json(data, json_file, append=True)


def write_batch_to_json(data, json_file, append=False):
    mode = 'a' if append else 'w'
    with open(json_file, mode) as file:
        for item in data:
            json.dump(item, file)
            file.write('\n')


# Contoh penggunaan
# Ganti dengan path file CSV Anda
csv_file = '/Users/gerryasrillinsandy/Documents/data-dump/dump_homepass_20230530_.csv'
# Ganti dengan nama file JSON yang diinginkan
json_file = '/Users/gerryasrillinsandy/Documents/data-dump/dump_homepass_data_.json'

convert_csv_to_json(csv_file, json_file, batch_size=100)
