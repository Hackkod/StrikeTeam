from django.contrib.auth.models import User
from django.db import models

class Teams(models.Model):
    teamname = models.CharField(max_length=255, verbose_name='Название команды')
    # teamamount = models.IntegerField(default=0, verbose_name='Количество участников')

    def __str__(self):
        return self.teamname

class Teammates(models.Model):
    team = models.ForeignKey('Teams', on_delete=models.CASCADE, verbose_name='Команда')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Пользователь')
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='children', verbose_name='Вышестоящий')
    
    name = models.CharField(max_length=255)    
    
    RIGHTS = [
        ('admin', 'Администратор'),
        ('editor', 'Редактор'),
        ('reader', 'Читатель'),
    ]
    rights = models.CharField(choices=RIGHTS, default='reader', max_length=255)
    
    rank = models.CharField(blank=True, default='-', max_length=255, null=True)
    parentname = models.CharField(blank=True, default='-', max_length=255, null=True)
    invite_time = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.rank:
            self.rank = '-'
        
        if self.parent:
            self.parentname = self.parent.name
        else:
            self.parentname = '-'
            
        super().save(*args, **kwargs)
    
class Inventory(models.Model):
    team = models.ForeignKey('Teams', on_delete=models.CASCADE, verbose_name='Команда')
    teammate = models.ForeignKey('Teammates', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Владелец')
    
    inventname = models.CharField(max_length=255, verbose_name='Наименование')
    amount = models.IntegerField(default=1, verbose_name='Количество')
    teammate_name = models.CharField(max_length=255, verbose_name='Имя владельца')
    
    CATEGORIES = [
        ('pyrotechnics', 'Пиротехника'),
        ('guns', 'Привода'),
        ('food', 'Продовольствие'),
        ('consumables', 'Расходники'),
        ('Props', 'Реквизит'),
        ('sleepeng_gear', 'Спальное снаряжение'),
        ('equipment', 'Экипировка'),
        ('other', 'Прочее'),
    ]
    category = models.CharField(choices=CATEGORIES, max_length=255, verbose_name='Категория')
    
    def __str__(self):
        return self.inventname
    
    def save(self, *args, **kwargs):
        if self.teammate:
            self.teammate_name = self.teammate.name
        else:
            self.teammate_name = '-'
            
        super().save(*args, **kwargs)
    