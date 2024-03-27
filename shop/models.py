from datetime import timezone
from django.db import models
from web.models import *
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



# Define Client model to store guest information
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    guest_phone = models.CharField(max_length=20, null=True, blank=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.guest_name


# Define Description model
class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Name : {self.pk}"
    

# Define RoomType model with many-to-many relationships
class Item(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    disc = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    descriptions = models.ManyToManyField('Description')
    images = models.ManyToManyField('Image')
    active = models.BooleanField(default=True)
    ratings = models.ManyToManyField('Rating', related_name='items', blank=True)


    def __str__(self):
        return self.name
    
    def average_rating(self):
        # Calculate and return the average rating for the item
        total_ratings = self.ratings.count()
        print(total_ratings)
        if total_ratings > 0:
            hop = sum([rating.rating for rating in self.ratings.all()]) / total_ratings
            print(hop)
            return hop
        else:
            return 0
    
class Rating(models.Model):
    Item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField(null = True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])
    Client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)  # Assuming you have a User model
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Client.user.username}'s rating for {self.Item.name}"



# Define Description model
class Description(models.Model):
    text = models.TextField()

    def __str__(self):
        return f"Description: {self.pk}"


# Define a model to store image sizes
class ImageSize(models.Model):
    width = models.PositiveIntegerField()  # Store the width of the image
    height = models.PositiveIntegerField()  # Store the height of the image

    def __str__(self):
        return f"Image Size: {self.width}x{self.height}"
    
# Define Image model
class Image(models.Model):
    image = models.ImageField(upload_to='shop_images/')

    def __str__(self):
        return f"Image: {self.pk}"


# Define Booking model
class Order(models.Model):
    quntity = models.PositiveIntegerField(null=True)  # Store the width of the image
    Client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE) # Store the width of the image
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    sold = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.Client.user}'s booking for {self.item.name} room"


# Define Coupon model
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    text = models.TextField(null = True)
    total = models.PositiveIntegerField(null=True)  # Store the width of the image
    used = models.PositiveIntegerField(null=True)  # Store the width of the image
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)


    def is_valid(self):
        now = timezone.now()
        return self.valid_from <= now <= self.valid_to

    def __str__(self):
        return f"Coupon: {self.code} ({self.discount_amount} off)"



# Define Booking model
class Order_chart(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('waiting_for_payment', 'Waiting for Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True) # Store the width of the image
    order = models.ManyToManyField('Order')
    coupons = models.ManyToManyField(Coupon)  # Multiple coupons can be associated with one Order_chart
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)
    payid = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)
    expird = models.BooleanField(default=False)


class Bank(models.Model):
    Bank_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20, unique=True)
    # Add any other relevant fields for the bank, such as address, contact info, etc.

    def __str__(self):
        return f"{self.name} - {self.account_number}"
    

class recipt(models.Model):
    image = models.ImageField(upload_to='payment/', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=False)
    valid_from = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    Client = models.ForeignKey(Client, on_delete=models.CASCADE, null = True)
    recipts = models.ManyToManyField(recipt)  # Multiple coupons can be associated with one Order_chart
    Order_chart = models.ForeignKey(Order_chart, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    # Add any other relevant fields for the payment, such as description, status, etc.
