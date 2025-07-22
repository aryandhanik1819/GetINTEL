import exifread

def extract_metadata(image_file):
    important_tags = {
        'Image Make': 'Camera Make',
        'Image Model': 'Camera Model',
        'EXIF DateTimeOriginal': 'Date Taken',
        'GPS GPSLatitude': 'Latitude',
        'GPS GPSLongitude': 'Longitude',
        'GPS GPSLatitudeRef': 'Latitude Ref',
        'GPS GPSLongitudeRef': 'Longitude Ref',
        'Image Software': 'Software',
    }

    metadata = {}

    try:
        with open(image_file, 'rb') as f:
            tags = exifread.process_file(f, details=False)

        for tag in important_tags:
            if tag in tags:
                metadata[important_tags[tag]] = str(tags[tag])

        return metadata if metadata else {"Error": "No important metadata found."}
    except Exception as e:
        return {"Error": str(e)}
