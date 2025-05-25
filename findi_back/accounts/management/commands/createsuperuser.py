# accounts/management/commands/createsuperuser.py

from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand

UserModel = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)

        # 가장 최근 생성된 superuser를 기준으로 role 설정
        user = UserModel.objects.filter(is_superuser=True).order_by('-date_joined').first()
        if user:
            user.role = 'admin'
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Superuser '{user.email}'의 role을 'admin'으로 설정했습니다."))
        else:
            self.stdout.write(self.style.ERROR("Superuser를 찾을 수 없습니다."))
