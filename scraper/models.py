from django.db import models

class ScrapingLog(models.Model):
    source = models.CharField(max_length=100, choices=[
        ('constitution', 'Constitution of Kenya'),
        ('mp_list', 'MPs List'),
        ('mp_details', 'MP Details')
    ])
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ])
    items_scraped = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.source} - {self.status} - {self.started_at}"
