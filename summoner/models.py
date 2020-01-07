from django.db import models

class Champion_Id(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=50)
    # champion = models.ForeignKey(Champion, on_delete=models.CASCADE)

    def __str__(self):
        return self.id