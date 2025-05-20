from django.db import models


class Payment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    amount = models.FloatField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} for Order #{self.order.id}"
