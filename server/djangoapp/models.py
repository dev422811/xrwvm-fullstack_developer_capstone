from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # You could add more fields here, e.g.:
    website = models.URLField(blank=True, help_text="Official website of the make")

    def __str__(self):
        return self.name


class CarModel(models.Model):
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        # Add more as needed
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CAR_TYPES, default=SEDAN)
    year = models.IntegerField(
        default=now().year,
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(now().year)
        ]
    )
    # Example extra field:
    dealer_id = models.IntegerField(help_text="ID of the dealer in Cloudant DB")

    def __str__(self):
        # shows both make and model
        return f"{self.car_make.name} {self.name} ({self.year})"
