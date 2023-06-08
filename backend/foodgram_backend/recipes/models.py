from django.core.validators import MinValueValidator, RegexValidator

from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    """
    .
    """
    name = models.CharField(
        'Название',
        max_length=200
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        null=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Поле должно содержать HEX-код выбранного цвета.'
            )
        ]

    )
    slug = models.SlugField(
        'слаг',
        max_length=200,
        unique=True,
        null=True
    )

    class Meta:
        """
        .
        """
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return str(self.name)


class Ingredient(models.Model):
    """
    .
    """
    name = models.CharField(
        'Название',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )

    class Meta:
        """
        .
        """
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """
    .
    """
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор"
    )
    name = models.CharField(
        "Название",
        max_length=200
    )
    image = models.ImageField(
        "Картинка",
        upload_to="recipes/",
        blank=True
    )
    text = models.TextField(
        "Описание"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        through_fields=("recipe", "ingredient"),
        verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги"
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления, мин",
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True
    )


class RecipeIngredient(models.Model):
    """
    .
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.SmallIntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )
