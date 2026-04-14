#!/usr/bin/env python3

from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from pathlib import Path
import os

# === KONFIGURACJA ===
CONN_STR      = os.getenv("AZURE_STORAGE_CONNECTION_STRING") or (
    "DefaultEndpointsProtocol="
)
CONTAINER     = "meta-csv"
LOCAL_DIR     = Path("/home/azureuser/Documents/dcm-to-csv/meta-csv")

# === INITIALIZACJA BLOB SERVICE ===
svc  = BlobServiceClient.from_connection_string(CONN_STR)
cont = svc.get_container_client(CONTAINER)

# === ITERACJA PO PLIKACH CSV ===
for csv_path in LOCAL_DIR.glob("*.csv"):
    blob_client = cont.get_blob_client(csv_path.name)

    # 1) Sprawdź, czy blob już istnieje
    try:
        blob_client.get_blob_properties()
        print(f"Pominięto {csv_path.name}, bo już jest na blobie.")
        continue
    except ResourceNotFoundError:
        # blob nie istnieje - przejdź dalej, żeby wysłać
        pass

    # 2) Upload pliku
    try:
        with open(csv_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=False)
        print(f"Wysłano {csv_path.name}")
    except Exception as e:
        print(f"Błąd przy wysyłce {csv_path.name}: {e}")
