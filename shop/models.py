from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Model representing a product category.

    Supports nested (sub) categories through self-referencing.
    """

    sub_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='sub_categories',
        null=True,
        blank=True
    )
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        """
        Return the name of the category.
        """
        return self.name

    def get_absolute_url(self):
        """
        Return the URL to filter products by this category.
        """
        return reverse('shop:category_filter', args=[self.slug])


class Product(models.Model):
    """
    Model representing a product listed in the shop.

    Each product may belong to multiple categories.
    """

    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%b/%d/')
    description = models.TextField()
    price = models.IntegerField()
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        """
        Return the name of the product.
        """
        return self.name

    def get_absolute_url(self):
        """
        Return the URL for the product detail view.
        """
        return reverse('shop:product_detail', args=[self.slug])

