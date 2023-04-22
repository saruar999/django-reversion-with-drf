from django.db import models
from reversion import register


@register()
class Blog(models.Model):

    title = models.CharField(max_length=50, help_text="A title for the blog instance.")

    description = models.CharField(
        max_length=150, null=True, help_text="An optional short description of the blog instance."
    )

    content = models.TextField(help_text="The blog instance's content body.")
