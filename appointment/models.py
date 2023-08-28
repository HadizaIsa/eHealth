from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Appointment(models.Model):
    STATUS = (
        ('PENDING', 'pending'),
        ('COMPLETED', 'completed')
    )
    DECISION_CHOICES = [
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected')
    ]

    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES, blank=True, null=True)

    def __str__(self):
        return "Patient - {} Doc- {} At {} {}".format(self.patient, self.doctor, self.date, self.time)

