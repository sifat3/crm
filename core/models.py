from django.db import models

class Client(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone = models.CharField(max_length=100, blank=False, null=False)
    def __str__(self) -> str:
        return self.name

class Completed_Project(models.Model):
    invoice = models.CharField(max_length=100, blank=False, null=False)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=False, null=True)
    bill = models.IntegerField(blank=False, null=False)
    cost = models.IntegerField(blank=False, null=False)
    profit = models.IntegerField(blank=False, null=False)
    delivery_date = models.DateField(blank=False, null=False)
    warranty = models.DateField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    freelancer_linkedIn = models.URLField(default="sifat.com")
    freelancer_email = models.EmailField(default='nothing@nothing.com')
    def __str__(self) -> str:
        return self.invoice
    
    class Meta:
        ordering = ["-created"]


class Ongoing_project(models.Model):
    invoice = models.CharField(max_length=100, blank=False, null=False)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=False, null=True)
    bill = models.IntegerField(default=0, blank=False, null=False)
    cost = models.IntegerField(default=0, blank=False, null=False)
    profit = models.IntegerField(default=0, blank=False, null=False)
    estimated_delivery_date = models.DateField(blank=False, null=False)
    first_payment = models.IntegerField(default=0, blank=False, null=False)
    second_payment = models.IntegerField(default=0, blank=False, null=False)
    third_payment = models.IntegerField(default=0, blank=False, null=False)
    due_amount = models.IntegerField(default=0, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.invoice
    



class Freelancer(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    phone = models.CharField(max_length=100, blank=False, null=False)
    linkedin = models.URLField()
    total_earned = models.IntegerField(default=0, blank=False, null=False)
    project = models.ForeignKey(Ongoing_project, on_delete=models.SET_NULL, null=True, blank=True, related_name='freelancers')
    skill = models.CharField(max_length=300, blank=False, null=False)
    due_amount = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self) -> str:
        return self.name
    

class Token(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    invoice = models.CharField(max_length=100, blank=False, null=False)
    problem = models.TextField(blank=False, null=False)
    solved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.invoice
    
    class Meta:
        ordering = ["-date"]
