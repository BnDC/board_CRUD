from django.db import models
from core.models import TimeStampModel 

class Posting(TimeStampModel):
    title = models.CharField(max_length = 100, unique = True)
    content = models.TextField()
    user = models.ForeignKey('user.User',on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'postings'

    def __str__(self):
        return self.title