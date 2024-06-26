from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

VENDORS = (
    ('V', 'Virgin Galactic'),
    ('S', 'SpaceX'),
    ('B', 'Blue Origin'),
)

DESTINATIONS = (
    ('Mo', 'Moon'),
    ('Ma', 'Mars'),
    ('Pl', 'Pluto'),
    ('Is', 'International Space Station (ISS)'),
    ('Ne', 'Neptune'),
)

RATING = (
    ('On', '1'),
    ('Tw', '2'),
    ('Th', '3'),
    ('Fo', '4'),
    ('Fi', '5'),
    ('Si', '6'),
    ('Se', '7'),
    ('Ei', '8'),
    ('Ni', '9'),
    ('Te', '10'),
)


class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.CharField(
        max_length=2, choices=DESTINATIONS, default=[0][0])
    experiences = models.TextField(max_length=1000)
    vendor = models.CharField(max_length=1, choices=VENDORS, default=[0][0])
    users = models.ManyToManyField(User, through="Ticket")  # lazy
    max_tickets = models.IntegerField(default=15)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_num_tickets_avail_for_date(self, date):
        ticket_count = self.ticket_set.filter(
            date=date).aggregate(models.Sum('qty'))['qty__sum']

        return self.max_tickets - ticket_count if ticket_count else self.max_tickets


class Ticket(models.Model):
    date = models.DateField('Departure Date')
    qty = models.IntegerField(default=1)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)


class Review(models.Model):
    content = models.TextField(max_length=1000)
    rating = models.CharField(max_length=2, choices=RATING, default=[0][0])
    likes = models.ManyToManyField(
        User, related_name='liked_reviews', default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.user}: {self.content}')

    def get_absolute_url(self):
        return reverse('reviews_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-id']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']