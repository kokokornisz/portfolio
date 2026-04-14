#!/usr/bin/env python3

from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from pathlib import Path
import os

# === KONFIGURACJA ===
CONN_STR      = os.getenv("AZURE_STORAGE_CONNECTION_STRING") or (
    "DefaultEndpointsProtocol="
)
CONTAINER     = "photo"
LOCAL_DIR     = Path("/home/azureuser/Documents/dcm-to-csv/photo")

# === INITIALIZACJA BLOB SERVICE ===
svc  = BlobServiceClient.from_connection_string(CONN_STR)
cont = svc.get_container_client(CONTAINER)

# === ITERACJA PO PLIKACH JPG ===
for photo_path in LOCAL_DIR.glob("*.jpg"):
    blob_client = cont.get_blob_client(photo_path.name)

    # 1) Sprawdź, czy blob już istnieje
    try:
        blob_client.get_blob_properties()
        print(f"Zdjęcie pominięto {photo_path.name}, bo już jest na blobie.")
        continue
    except ResourceNotFoundError:
        # blob nie istnieje - przejdź dalej, żeby wysłać
        pass

    # 2) Upload pliku
    try:
        with open(photo_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=False)
        print(f"Wysłano zdjęcie {photo_path.name}")
    except Exception as e:
        print(f"Błąd przy wysyłce zdjęcia {photo_path.name}: {e}")
