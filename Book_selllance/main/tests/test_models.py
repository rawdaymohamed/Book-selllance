from django.test import TestCase
from decimal import Decimal
from main import models
from django.core.files.images import ImageFile
import logging
from django.core.files.images import get_image_dimensions
import os
from PIL import Image
logger = logging.getLogger(__name__)

class TestModel(TestCase):
    def test_active_manager_works(self):
        models.Product.objects.create(
            name="Harry Potter", price=Decimal("50.00"))
        models.Product.objects.create(
            name="The Wife between us", price=Decimal("10.00"), active=False)
        self.assertEqual(len(models.Product.objects.active()), 1)

    def test_thumbnails_are_generated_on_save(self):
        product = models.Product(
            name="The cathedral and the bazaar",
            price=Decimal("10.00"),
        )
        product.save()

        with open(
            "main/fixtures/the-cathedral-the-bazaar.jpg", "rb"
        ) as f:
            image = models.ProductImage(
                product=product,
                image=ImageFile(f, name="tctb.jpg"),
            )
           
            image.save()

        image.refresh_from_db()

        with open(
            "main/fixtures/the-cathedral-the-bazaar.thumb.jpg",
            "rb",
        ) as f:
            expected_content = f.read()
            # print(os.path.getsize("main/fixtures/the-cathedral-the-bazaar.thumb.jpg"))
            im = Image.open(image.thumbnail.path)
            image_size = im.size
            expected_size = Image.open("main/fixtures/the-cathedral-the-bazaar.thumb.jpg").size
            print(image_size)
            print(expected_size)
            # assert im.size == (300, 300)
            # assert image.thumbnail.read() == expected_content
            # assert image_size == expected_size

        image.thumbnail.delete(save=False)
        image.image.delete(save=False)
