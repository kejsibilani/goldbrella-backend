from django.db import models

class Menu(models.Model):
    beach = models.OneToOneField(
        'beach.Beach',
        on_delete=models.CASCADE,
        related_name='menu'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        return f"{self.title} ({self.beach.title})"

class MenuImage(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='menu_images/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Menu Image'
        verbose_name_plural = 'Menu Images'

    def __str__(self):
        return f"Image for {self.menu.title} ({self.menu.beach.title})" 