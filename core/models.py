from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class MedicineLog(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    date = models.DateField(auto_now_add=True)
    alert_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.status

class Caregiver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name
    
    

