from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Ad(models.Model):
    STATUS_CHOICES = [
        ("draft", "Черновик"),
        ("published", "Опубликовано"),
        ("archived", "Архив"),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField(max_length=5000)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="ads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at", "-id"]
