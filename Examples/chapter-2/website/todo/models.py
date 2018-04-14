from django.db import models


class ToDoItem(models.Model):

    text = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField()
    
    def __str__(self):
        return self.text
