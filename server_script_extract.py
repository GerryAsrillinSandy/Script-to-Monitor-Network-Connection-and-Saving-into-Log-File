import csv
import json
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set batas ukuran field yang lebih besar
csv.field_size_limit(1000 * 1024 * 1024)

# Counter untuk data yang sudah selesai diproses
processed_data_counter = 0


def get_api_token():
    # API endpoint URL
    url = "https://107d-sgapp.teleows.com/ws/rest/107d/wfm_pos_lead/token"

    # Request headers
    headers = {
        "Authorization": "Basic MTA3ZHxUVmxvSm1jQU0wQ3QzWDR5OTMxOTpjdmRsc0orUTV6TlR5PkoxT3JqMCpsOENQR2JKMCZQaDU0JnpkXmwwZHJBSFdINUZDIz0/P3c1Q2d4OCRZd1FZ",
    }

    # Send POST request with authorization
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        bearer = result["token_type"]
        token = result["access_token"]
        auth = f"{bearer} {token}"

        # Ganti dengan URL endpoint REST API Anda
        api_url = "https://107d-sgapp.teleows.com/ws/rest/107d/wfm_pos_lead/homepass_create"
        api_headers = {
            "Authorization": auth,
            "Content-Type": "application/json",
        }

        return api_url, api_headers
    else:
        print("Gagal mendapatkan token. Response status code:", response.status_code)
        return None, None


# Menggunakan fungsi untuk mendapatkan API URL dan headers
api_url, api_headers = get_api_token()


# Fungsi untuk mengirim permintaan REST API dengan data batch
def send_rest_api_request(url, headers, data):
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Memeriksa respons HTTP untuk kesalahan
        print(f"Data JSON berhasil dikirim ke {url}")
        print(f"Response: {response.status_code} {response.text}")
        global processed_data_counter
        processed_data_counter += 1
    except requests.exceptions.RequestException as err:
        print(f"Terjadi kesalahan saat mengirim permintaan ke {url}: {err}")


# Fungsi untuk mengubah file CSV menjadi rest API JSON
def convert_csv_to_restapi_json(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(file, delimiter="|")
        data_list = list(reader)

    total_rows = len(data_list)  # Menghitung jumlah total baris

    for data in data_list:
        send_rest_api_request(api_url, api_headers, data)

    global processed_data_counter
    processed_data_counter += len(data_list)

    if processed_data_counter >= total_rows:
        print("Semua data CSV telah diproses.")
        print(
            f"Jumlah data yang sudah selesai diproses: {processed_data_counter}")
        observer = Observer()
        observer.stop()
        print("Memantau folder lagi...")

    processed_data_counter = 0  # Reset counter
    monitor_folder(folder_path)


# Fungsi untuk menangani perubahan pada folder
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.event_type == "modified" or event.event_type == "created":
            print(f"Mengubah file {event.src_path} menjadi JSON...")
            convert_csv_to_restapi_json(event.src_path)
            # Uncomment line below if you want to remove the CSV file after converting to JSON
            # os.remove(event.src_path)


# Fungsi untuk memantau folder
def monitor_folder(folder_path):
    print(f"Memantau folder {folder_path}...")
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(timeout=1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


# Menjalankan script untuk memantau folder
folder_path = "D:\Task\AOS\script\data"
monitor_folder(folder_path)
