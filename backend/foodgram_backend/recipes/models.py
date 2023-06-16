from django.core.validators import MinValueValidator

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    """Класс описания модели Тега."""

    name = models.CharField(
        'Название',
        max_length=100,
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=16,
        null=True,
    )
    slug = models.SlugField(
        'слаг',
        max_length=200,
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return str(self.name)


class Ingredient(models.Model):
    """Класс описания модели Ингридиента."""

    name = models.CharField(
        'Название',
        max_length=70,
    )
    amount = models.PositiveSmallIntegerField(
        'количество',
        default=1,
        validators=[MinValueValidator(1)],
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=50,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Класс описания модели Рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название',
        max_length=200,
    )
    # image = models.ImageField(
    #     'Картинка',
    #     upload_to='recipes/',
    #     blank=True,
    # )
    text = models.TextField(
        'Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления, мин',
        default=1,
        validators=[MinValueValidator(1)],
    )


class Favorite(models.Model):
    """Класс описания модели Избранного."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='понравившийся рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='добавил в избранное',
    )

    class Meta:
        verbose_name = 'рецепт в избранном'
        verbose_name_plural = 'рецепты в избранном'

    def __str__(self):
        return f'Пользователю {self.user} понравился рецепт {self.recipe}'


class ShoppingCart(models.Model):
    """Класс описания модели Списка Покупок."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart_recipe',
        verbose_name='рецепт добавленный в список покупок',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_user',
        verbose_name='добавил в список покупок',
    )

    class Meta:
        verbose_name = 'рецепт в списке покупок'
        verbose_name_plural = 'рецепты в списке покупок'

    def __str__(self):
        return f'Пользователь {self.user} добавил рецепт ' \
               f'{self.recipe} в список покупок'
