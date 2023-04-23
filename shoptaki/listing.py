import csv
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Listing

def import_listings_from_csv(file_path):
    with open(file_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # photo_main = SimpleUploadedFile(row['photo_main'], open(row['photo_main'], 'rb').read(), content_type='image/jpeg')
            # photo_1 = SimpleUploadedFile(row['photo_1'], open(row['photo_1'], 'rb').read(), content_type='image/jpeg') if row['photo_1'] else None
            # photo_2 = SimpleUploadedFile(row['photo_2'], open(row['photo_2'], 'rb').read(), content_type='image/jpeg') if row['photo_2'] else None
            # photo_3 = SimpleUploadedFile(row['photo_3'], open(row['photo_3'], 'rb').read(), content_type='image/jpeg') if row['photo_3'] else None
            # photo_4 = SimpleUploadedFile(row['photo_4'], open(row['photo_4'], 'rb').read(), content_type='image/jpeg') if row['photo_4'] else None
            # photo_5 = SimpleUploadedFile(row['photo_5'], open(row['photo_5'], 'rb').read(), content_type='image/jpeg') if row['photo_5'] else None
            # photo_6 = SimpleUploadedFile(row['photo_6'], open(row['photo_6'], 'rb').read(), content_type='image/jpeg') if row['photo_6'] else None
            listing = Listing(
                title=row['title'],
                address=row['address'],
                city=row['city'],
                state=row['state'],
                zipcode=row['zipcode'],
                description=row['description'],
                price=int(row['price']),
                bedrooms=int(row['bedrooms']),
                bathrooms=float(row['bathrooms']),
                garage=int(row['garage']),
                sqft=int(row['sqft']),
                lot_size=float(row['lot_size']),
                # photo_main=photo_main,
                # photo_1=photo_1,
                # photo_2=photo_2,
                # photo_3=photo_3,
                # photo_4=photo_4,
                # photo_5=photo_5,
                # photo_6=photo_6,
                is_published=bool(row['is_published']),
                # list_date=datetime.strptime(row['list_date'], '%Y-%m-%d %H:%M'),
            )
            listing.save()
