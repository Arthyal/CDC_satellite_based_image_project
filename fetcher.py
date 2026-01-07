import os
import pandas as pd
from dotenv import load_dotenv
import requests
from tqdm import tqdm
import time

load_dotenv()

MAPBOX_TOKEN =os.getenv("Token")

STYLE = "mapbox/streets-v11"   
ZOOM = 15
IMG_SIZE = (224, 224)

df_train= pd.read_excel('train(1).xlsx')
df_train.to_csv('train(1).csv',index=False)
df_test= pd.read_excel('test2.xlsx')
df_test.to_csv('test2.csv',index=False)

EXCEL_FILES = [
    "train(1).xlsx",
    "test2.xlsx"
]

def outer_download_image(EXCEL_PATH):
    EXCEL_PATH = EXCEL_PATH
    excel_filename = os.path.splitext(os.path.basename(EXCEL_PATH))[0]
    SAVE_DIR = f"images_{excel_filename}"
    
    os.makedirs(SAVE_DIR, exist_ok=True)
    df = pd.read_excel(EXCEL_PATH)
    
    def inner_download_image(lat, lon):

        filename = f"{lat}_{lon}.png"

        filepath = os.path.join(SAVE_DIR, filename)

   
        if os.path.exists(filepath):
            return True

        url = (
            f"https://api.mapbox.com/styles/v1/{STYLE}/static/"
            f"{lon},{lat},{ZOOM}/{IMG_SIZE[0]}x{IMG_SIZE[1]}"
            f"?access_token={MAPBOX_TOKEN}"
            )

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
                return True
        else:
            print(f"{lat},{lon} → {response.status_code}")
            return False
    
    for _, row in tqdm(df.iterrows(), total=len(df)):
        ok = inner_download_image(row["lat"], row["long"])
        time.sleep(0.1)

for path in EXCEL_FILES:
    outer_download_image(path)



   
