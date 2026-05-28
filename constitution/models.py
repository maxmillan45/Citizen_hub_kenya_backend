from django.db import models

class Article(models.Model):
    TOPIC_CHOICES = [
        ('rights', 'Bill of Rights'),
        ('land', 'Land and Environment'),
        ('leadership', 'Leadership and Integrity'),
        ('devolution', 'Devolution'),
        ('citizenship', 'Citizenship'),
        ('judiciary', 'Judiciary'),
        ('other', 'Other'),
    ]

    chapter = models.IntegerField()
    article_number = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=300)
    full_text = models.TextField()
    simplified_english = models.TextField(blank=True)
    simplified_swahili = models.TextField(blank=True)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES, default='other')
    audio_url = models.URLField(blank=True, null=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Article {self.article_number}: {self.title[:50]}"

