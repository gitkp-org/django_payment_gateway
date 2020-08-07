from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ammount = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=150, default=0)
    remarks = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.transaction_id
