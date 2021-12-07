from django.test import TestCase
from decimal import Decimal
from main import models
from django.core.files.images import ImageFile
import logging
from django.core.files.images import get_image_dimensions
import os
from PIL import Image
logger = logging.getLogger(__name__)
from main import factories

# Using factory_boy

class TestModel(TestCase):
    def test_active_manager_works(self):
        factories.ProductFactory.create_batch(2, active=True)
        factories.ProductFactory(active=False)
        self.assertEqual(len(models.Product.objects.active()), 2)
    
    def test_create_order_works(self):
        p1 = factories.ProductFactory()
        p2 = factories.ProductFactory()
        user1 = factories.UserFactory()
        billing = factories.AddressFactory(user=user1)
        shipping = factories.AddressFactory(user=user1)

        basket = models.Basket.objects.create(user=user1)
        models.BasketLine.objects.create(basket=basket, product=p1)
        models.BasketLine.objects.create(basket=basket, product=p2)
        with self.assertLogs('main.models', level='INFO') as cm:
            order = basket.create_order(billing, shipping)
        self.assertGreaterEqual(len(cm.output), 1)
        order.refresh_from_db()

        self.assertEquals(order.user, user1)
        self.assertEquals(
            order.billing_address1, billing.address1 
        )
        self.assertEquals(
            order.shipping_address1, shipping.address1 
        )
        self.assertEquals(order.lines.all().count(), 2)
        lines = order.lines.all()
        self.assertEquals(lines[0].product, p1)
        self.assertEquals(lines[1].product, p2)

'''
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

    def test_create_order_works(self):
        p1 = models.Product.objects.create(
            name='Harry Potter',
            price=Decimal('50.00'),
        )
        p2 = models.Product.objects.create(
            name='The wife between us',
            price=Decimal('20.00'),
        )
        user1 = models.User.objects.create_user('user1', 'abcabcabc')
        billing = models.Address.objects.create(
            user=user1,
            name='John Smith',
            address1 = "Boston",
            city="MA",
            country="us",
        )
        shipping = models.Address.objects.create(
            user=user1,
            name='John Smith',
            address1 = "Boston",
            city="MA",
            country="us",
        )
        basket = models.Basket.objects.create(user=user1)
        models.BasketLine.objects.create(basket=basket, product=p1)
        models.BasketLine.objects.create(basket=basket, product=p2)

        with self.assertLogs('main.models', level='INFO') as cm:
            order = basket.create_order(billing, shipping)

        self.assertGreaterEqual(len(cm.output), 1)    
        order.refresh_from_db()
        self.assertEquals(order.user, user1)
        self.assertEquals(order.billing_address1, 'Boston')
        self.assertEquals(order.shipping_address1, 'Boston')
        self.assertEquals(order.lines.all().count(), 2)
        lines = order.lines.all()
        self.assertEquals(lines[0].product, p1)
        self.assertEquals(lines[1].product, p2)


'''