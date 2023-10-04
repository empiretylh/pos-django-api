from reportlab.lib.units import mm
from django.test import TestCase, RequestFactory
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
from .models import Product, User, Category
import os
import io
import ast

from django.conf import settings


import io
import base64
import barcode
from barcode.writer import ImageWriter


def generate_barcode(product_id):

    product_id = str(product_id).zfill(12)
    # Generate a unique barcode value using the EAN13 format
    ean = barcode.get_barcode_class('ean13')
    barcode_value = ean(str(product_id), writer=ImageWriter())

    # Convert the barcode image to a base64-encoded string
    buffer = io.BytesIO()
    barcode_value.write(buffer)
    barcode_image = Image.open(buffer)
    return barcode_image


# Export BarCode for


class ExportBarcodeTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass')

    def test_export_barcode(self):
        # Create some test products
        category = Category.objects.create(
            user=self.user, title='Category 1')

        Product.objects.create(
            user=self.user, name='သခွားသီး', price=10.0, qty=10, category=category)
        Product.objects.create(
            user=self.user, name='om', price=20.0, qty=5, category=category)

        Product.objects.create(
            user=self.user, name='Product 1', price=20.0, qty=5, category=category)

        Product.objects.create(
            user=self.user, name='Product 2', price=20.0, qty=8, category=category)

        products = Product.objects.all()

       # Create a buffer to hold the PDF file
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # Set the column and row dimensions
        col_width = 40 * mm
        row_height = 20 * mm
        margin = 10 * mm
        x = margin
        y = A4[1] - margin


        current_product_name = None

        for i in products:
            for j in range(int(i.qty)):
                barcode_image = generate_barcode(i.pk)

                # Resize the barcode image to fit in the cell
                # barcode_image = barcode_image.resize((int(col_width), int(row_height)))

                # Convert the barcode image to a format that can be added to the PDF
                img_data = io.BytesIO()
                barcode_image.save(img_data, format='PNG')
                img_data.seek(0)

                # c.rect(x, y - row_height - 15 * mm, col_width, row_height, stroke=1, fill=0)


                # Add the barcode image to the PDF
                c.drawImage(ImageReader(img_data), x, y - row_height, width=col_width, height=row_height)

                # Move to the next cell
                x += col_width + 10 * mm

                # If we reach the end of the row, move to the next row
                if x >= A4[0] - margin:
                    x = margin
                    y -= row_height + 10 * mm

                # If we reach the end of the page, start a new page
                if y <= margin:
                    c.showPage()
                    y = A4[1] - margin
                    current_product_name = None

        c.save()

        # Write the PDF file to a file on the server
        filename = 'Products_BarCode.pdf'
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        with open(filepath, 'wb') as f:
            f.write(buffer.getbuffer())
