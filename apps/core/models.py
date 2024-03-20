from django.db import models



class CustomErrors(models.Model):
    code = models.CharField(max_length=122)
    status_code = models.IntegerField()
    detail = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    count = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.code}"
    
    def increase_count(self):
        self.count += 1
        self.save()

