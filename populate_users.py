# myapp/management/commands/populate_users.py

from django.core.management.base import BaseCommand
from accounts.models import CustomUser
import json

class Command(BaseCommand):
    help = 'Populate users data'

    def handle(self, *args, **kwargs):
        with open('data.json', 'r') as file:
            data = json.load(file)
        
        investors_data = data.get('investors', [])
        investees_data = data.get('investees', [])
        
        for investor_data in investors_data:
            CustomUser.objects.create(**investor_data, user_type=CustomUser.INVESTOR)
        
        for investee_data in investees_data:
            CustomUser.objects.create(**investee_data, user_type=CustomUser.INVESTEE)
        
        self.stdout.write(self.style.SUCCESS('Users data populated successfully'))
