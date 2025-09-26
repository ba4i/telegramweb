from django.db import models

class Ticket(models.Model):
    number = models.IntegerField()
    question = models.TextField()
    answer = models.TextField()
    theme = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Билет {self.number}: {self.question[:50]}"
