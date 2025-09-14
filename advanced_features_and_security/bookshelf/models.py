from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_edit", "Can edit book"),
        ]

    def __str__(self):
        return self.title
