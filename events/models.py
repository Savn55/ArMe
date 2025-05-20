from django.db import models

# Create your models here.

class Event(models.Model):

  # Define category choices
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('SALES', 'Sales'),
        ('SPORTS', 'Sports'),
        ('EDUCATION', 'Education'),
        ('TECHNOLOGY', 'Technology'),
        ('HEALTH', 'Health'),
        ('OTHER', 'Other'),
    ]


    name = models.CharField(max_length=255)
    description = models.TextField()

    # Add the category field
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='OTHER'
    )
    
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def full_address(self):
        return f"{self.street}, {self.city}, {self.state} {self.zipcode}"
