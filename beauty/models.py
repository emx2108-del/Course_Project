from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность (мин.)")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


class Master(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя мастера")
    specialization = models.CharField(max_length=200, blank=True, verbose_name="Специализация")
    photo = models.ImageField(upload_to='masters/', blank=True, null=True, verbose_name="Фото")
    bio = models.TextField(blank=True, verbose_name="Биография")  # ← ДОБАВЬТЕ ЭТУ СТРОКУ
    services = models.ManyToManyField(
        Service,
        related_name='masters',
        verbose_name="Предоставляемые услуги"
    )

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Appointment(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_CONFIRMED, 'Подтверждена'),
        (STATUS_COMPLETED, 'Выполнена'),
        (STATUS_CANCELLED, 'Отменена'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name="Клиент"
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name="Мастер"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name="Услуга"
    )
    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name="Статус"
    )
    comment = models.TextField(blank=True, verbose_name="Комментарий клиента")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ['start_time']

    def __str__(self):
        return f"Запись #{self.pk}: {self.client.name} - {self.service.name}"