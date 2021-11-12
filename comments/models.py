from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.BooleanField()
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField()

    def __str__(self):
        return self.content[:50]
