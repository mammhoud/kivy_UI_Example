from django.db import models


class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50)
    total = models.FloatField()
    shipping_address = models.TextField()
    items = models.JSONField()  # Assumes items are stored as a JSON structure

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    class Meta:
        unique_together = (('order', 'product'),)
