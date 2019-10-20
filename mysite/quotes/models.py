from django.db import models


# Create your models here.

class Author(models.Model):
    first_name = models.CharField(
        max_length=25,
        blank=False,
        verbose_name='First name')

    last_name = models.CharField(
        max_length=25,
        blank=False,
        verbose_name='Last name')

    slug = models.CharField(max_length=255, unique=True)

    born_date = models.CharField(
        max_length=50,
        verbose_name='Born date')

    dead_date = models.CharField(
        max_length=50,
        verbose_name='Dead date')

    profesion = models.CharField(
        max_length=25,
        verbose_name='Profesion')

    nationality = models.CharField(
        max_length=25,
        verbose_name='Nationality')

    description = models.CharField(
        max_length=1000,
        verbose_name='Description')

    foto = models.ImageField(
        verbose_name='Foto',
        blank=True,
        upload_to='authors'
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Topic(models.Model):
    topic = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Topic',
        unique=True)

    slug = models.CharField(
        max_length=255,
        unique=True)

    foto = models.ImageField(
        verbose_name='Foto',
        upload_to='topics'
    )

    def __str__(self):
        return self.topic


class Quote(models.Model):
    quote = models.CharField(
        max_length=500,
        blank=False,
        verbose_name='Quote',
        unique=True)

    slug = models.CharField(
        max_length=255,
        unique=True)

    author = models.ForeignKey(
        Author,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Autor'
    )

    topic = models.ForeignKey(
        Topic,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Topic'
    )

    def __str__(self):
        return str(self.author) + ' ' + str(self.topic)


class MessagesToAdmin(models.Model):
    from_email = models.EmailField(
        verbose_name='Your email')
    subject = models.CharField(
        verbose_name='Subject',
        max_length=128)
    message = models.CharField(
        verbose_name='Text of message',
        max_length=10000)
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Received date')

    def __str__(self):
        return str(self.subject) + ' ' + str(self.pub_date)
