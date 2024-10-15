import pandas as pd
from sqlalchemy import create_engine
import requests
import time

def fetch_images_from_pexels(api_key, num_images=200, retries=3):
    url = f"https://api.pexels.com/v1/search?query=apartment&per_page={num_images}"
    headers = {
        'Authorization': api_key
    }
    images = []
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            images = [photo['src']['medium'] for photo in data['photos']]
            if len(images) >= num_images:
                return images
            else:
                print(f"Not enough images fetched. Only {len(images)} images.")
                return images
        elif response.status_code == 429:
            print(f"Rate limit exceeded. Attempt {attempt + 1} of {retries}.")
            time.sleep(10)  # Wait 10 seconds before retrying
        else:
            print(f"Failed to fetch images: {response.status_code}")
            return []

    return []

# Path to your CSV file
csv_file_path = './static/mumbai.csv'  # Replace with your actual CSV file path

# Your Pexels API Key
api_key = 'dzVL1hWFJv3RFYOD1I2fm86Hi7XEO3P3CqZCzEVfOEGtApKQ2dungIen'  # Replace with your actual Pexels API key

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Keep only the columns you need
df_filtered = df[['PRICE', 'CITY', 'BEDROOM_NUM', 'PROP_NAME', 'CLASS']].copy()

# Rename columns to match your database schema
df_filtered.columns = ['price', 'location', 'bhk', 'address', 'img_path']

# Select only the first 200 rows
df_filtered = df_filtered.iloc[800:1000]

# Fetch images from Pexels
images = fetch_images_from_pexels(api_key, num_images=200)
if not images:
    images = ['./static/img/default_image.jpg']  # Fallback image if API fails

# Assign images to properties
df_filtered['img_path'] = [images[i % len(images)] for i in range(len(df_filtered))]

# Create connection to the MySQL database
engine = create_engine('mysql+mysqlconnector://root:Anvesh1702@localhost/real_estate')

# Insert data into the Property table
df_filtered.to_sql('property', con=engine, if_exists='append', index=False)

print("Data import completed successfully.")
