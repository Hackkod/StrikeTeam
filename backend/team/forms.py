from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

    def save_m2m(self):
        pass
    
    def save(self, commit=True):
        self.clean()
        # Получение данных из формы
        team = self.cleaned_data['team']
        teammate = self.cleaned_data['teammate']
        inventname = self.cleaned_data['inventname']
        amount = self.cleaned_data['amount']
        
        # Поиск существующего инвентаря с такими же team, teammate и inventname
        existing_inventory = Inventory.objects.filter(team=team, teammate=teammate, inventname=inventname).first()

        if existing_inventory:
            # Если инвентарь существует, обновляем его значение amount
            existing_inventory.amount += amount
            if commit:
                existing_inventory.save()
            return existing_inventory
        else:
            # Если инвентарь не существует, создаем новый объект инвентаря
            return super().save(commit=commit)
    
    def clean(self):
        cleaned_data = super().clean()
        team = cleaned_data.get("team")
        teammate = cleaned_data.get("teammate")

        if team and teammate:
            if teammate.team != team:
                raise forms.ValidationError("Selected teammate is not in the chosen team.")
        return cleaned_data
