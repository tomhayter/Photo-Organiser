import yaml
from os import listdir, rename
from pathlib import Path
from PIL import Image
from datetime import datetime, date

month_folder_names = {1: "01 - January",
                      2: "02 - February",
                      3: "03 - March",
                      4: "04 - April",
                      5: "05 - May",
                      6: "06 - June",
                      7: "07 - July",
                      8: "08 - August",
                      9: "09 - September",
                      10: "10 - October",
                      11: "11 - November",
                      12: "12 - December"}

photos_by_date = {}

def get_date_taken(path):
    exif = Image.open(path)._getexif()
    if not exif:
        raise Exception('Image {0} does not have EXIF data.'.format(path))
    return exif[36867]

# Get config
config = yaml.safe_load(open("config.yml"))

input_folder = config["inputFolder"]
photos = listdir(input_folder)
for photo in photos:
    if '.mp4' in photo:
        continue
    photo_path = f"{input_folder}/{photo}"
    try:
        timestamp = get_date_taken(photo_path)
    except Exception:
        continue

    dt = datetime.strptime(timestamp, '%Y:%m:%d %H:%M:%S')
    d = date(dt.year, dt.month, dt.day)
    if d in photos_by_date.keys():
        photos_by_date[d].append(photo)
    else:
        photos_by_date[d] = [photo]

# print(photos_by_date)

output_folder = config["outputFolder"]
for index, photos in photos_by_date.items():
    if len(photos) >= config["folderMin"]:
        if index.day < 10:
            path = f"{output_folder}/{index.year}/{month_folder_names[index.month]}/0{index.day}"
        else:
            path = f"{output_folder}/{index.year}/{month_folder_names[index.month]}/{index.day}"
    else:
        path = f"{output_folder}/{index.year}/{month_folder_names[index.month]}"
    print(path)
    Path(path).mkdir(parents=True, exist_ok=True)
    for pic in photos:
        old_file_path = f"{input_folder}/{pic}"
        new_file_path = f"{path}/{pic}"
        rename(old_file_path, new_file_path)
