# Generated by Django 5.0.4 on 2024-05-16 09:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamname', models.CharField(max_length=255, verbose_name='Название команды')),
            ],
        ),
        migrations.CreateModel(
            name='Teammates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rights', models.CharField(choices=[('admin', 'Администратор'), ('editor', 'Редактор'), ('reader', 'Читатель')], default='reader', max_length=255)),
                ('rank', models.CharField(max_length=255)),
                ('parentname', models.CharField(default='-', max_length=255)),
                ('invite_time', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='team.teammates', verbose_name='Вышестоящий')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.teams', verbose_name='Команда')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventname', models.CharField(max_length=255, verbose_name='Наименование')),
                ('amount', models.IntegerField(default=1, verbose_name='Количество')),
                ('teammate_name', models.CharField(max_length=255, verbose_name='Имя владельца')),
                ('category', models.CharField(choices=[('pyrotechnics', 'Пиротехника'), ('guns', 'Привода'), ('food', 'Продовольствие'), ('consumables', 'Расходники'), ('Props', 'Реквизит'), ('sleepeng_gear', 'Спальное снаряжение'), ('equipment', 'Экипировка'), ('other', 'Прочее')], max_length=255, verbose_name='Категория')),
                ('teammate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='team.teammates', verbose_name='Владелец')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.teams', verbose_name='Команда')),
            ],
        ),
    ]