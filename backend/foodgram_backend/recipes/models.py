from colorfield.fields import ColorField

from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    )
from django.contrib.auth import get_user_model
from django.db import models

from foodgram_backend.settings import (MIN_VALUE_AMOUNT_AND_COOKING_TIME,
                                       MAX_VALUE_AMOUNT,
                                       MAX_VALUE_COOKING_TIME)

User = get_user_model()


class Tag(models.Model):
    """Класс описания модели Тега."""

    name = models.CharField(
        'Название',
        max_length=100,
        unique=True,
    )
    color = ColorField(
        'Цвет в HEX',
        max_length=7,
        unique=True,
        default='#FF0000',
    )
    slug = models.SlugField(
        'слаг',
        max_length=200,
        unique=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color', 'slug', ],
                name='unique_tag'
            )
        ]
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        self.color = self.color.upper()
        return super(Tag, self).save(force_insert,
                                     force_update,
                                     using,
                                     update_fields)


class Ingredient(models.Model):
    """Класс описания модели Ингридиента."""

    name = models.CharField(
        'Название',
        max_length=70,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=50,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', ],
                name='unique_ingredient'
            )
        ]
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
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления, мин',
        default=MIN_VALUE_AMOUNT_AND_COOKING_TIME,
        validators=(MinValueValidator(MIN_VALUE_AMOUNT_AND_COOKING_TIME),
                    MaxValueValidator(MAX_VALUE_COOKING_TIME)),
    )
    pub_date = models.DateTimeField('дата создания рецепта',
                                    auto_now_add=True, )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name', ],
                name='unique_recipe'
            )
        ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Доп таблица для ингридиентов в рецепте."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        'количество',
        default=MIN_VALUE_AMOUNT_AND_COOKING_TIME,
        validators=(MinValueValidator(MIN_VALUE_AMOUNT_AND_COOKING_TIME),
                    MaxValueValidator(MAX_VALUE_AMOUNT)),
    )

    class Meta:
        verbose_name = 'Ингредиенты в Рецептах'
        verbose_name_plural = 'Ингредиенты в Рецептах'

    def __str__(self):
        return (f'Игредиент {self.ingredient.name}'
                f'добавлен в рецепт {self.recipe.name}'
                f'в количестве {self.amount}')


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
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'),
        ]
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
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_shopping_cart'),
        ]
        verbose_name = 'рецепт в списке покупок'
        verbose_name_plural = 'рецепты в списке покупок'

    def __str__(self):
        return (f'Пользователь {self.user} добавил рецепт'
                f'{self.recipe} в список покупок')
# class SelectedRecipe(models.Model):
#     """Класс описания родительского класса для Избранного и Корзины."""
#
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='selected_recipe',
#         verbose_name='выбранный рецепт',
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='selected_user',
#         verbose_name='выбрал рецепт',
#     )
#
#     class Meta:
#         abstract = True
#
#
# class Favorite(SelectedRecipe):
#     """Класс описания модели Избранного."""
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['recipe', 'user'],
#                 name='unique_favorite'),
#         ]
#         verbose_name = 'рецепт в избранном'
#         verbose_name_plural = 'рецепты в избранном'
#
#     def __str__(self):
#         return f'Пользователю {self.user} понравился рецепт {self.recipe}'
#
#
# class ShoppingCart(SelectedRecipe):
#     """Класс описания модели Списка Покупок."""
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['recipe', 'user'],
#                 name='unique_shopping_cart'),
#         ]
#         verbose_name = 'рецепт в списке покупок'
#         verbose_name_plural = 'рецепты в списке покупок'
#
#     def __str__(self):
#         return (f'Пользователь {self.user} добавил рецепт'
#                 f'{self.recipe} в список покупок')
# При такой реализации с одинаковыми related_name
# при миграциях выдает ошибки типа:
# HINT: Add or change a related_name argument to the definition
# for 'recipes.Favorite.user' or 'recipes.ShoppingCart.user'.
