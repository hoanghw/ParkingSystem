__author__ = 'Hoang'
from django.db import models

class Participant(models.Model):
    uid = models.BigIntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    parkingStatus = models.BooleanField(default=False)

class LicensePlate(models.Model):
    text = models.CharField(max_length=10)
    participant = models.ForeignKey(Participant)
    isActive = models.BooleanField()

class Garage(models.Model):
    garageId = models.IntegerField()
    isFPermit = models.BooleanField()
    isCPermit = models.BooleanField()
    priceDaily = models.FloatField(default=10)
    priceHourly = models.FloatField(default=2)
    priceQuarterly = models.FloatField(default=0.5)

class HistoryTransaction(models.Model):
    participant = models.ForeignKey(Participant)
    garage = models.CharField(max_length=100)
    space = models.CharField(max_length=4)
    startTime = models.BigIntegerField()
    endTime = models.BigIntegerField()
    totalCost = models.FloatField()
    granularity_choices = ((1,'Per Diem'),(2,'Per Hour'),(3,'perquarter'),)
    granularity = models.CharField(max_length=10,choices=granularity_choices,default=1)
    rate = models.FloatField()

class CurrentTransaction(models.Model):
    pointer = models.ForeignKey(HistoryTransaction)

class Garage(models.Model):
    garageId = models.IntegerField()
    isFPermit = models.BooleanField()
    isCPermit = models.BooleanField()
    priceDaily = models.FloatField(default=10)
    priceHourly = models.FloatField(default=2)
    priceQuarterly = models.FloatField(default=0.5)


