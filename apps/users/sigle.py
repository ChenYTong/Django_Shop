from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# post_save()接受信号
# sender接受信号的model
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # 判断是否新建,在update的时候也会进行post_save
    if created:
        password = instance.password
        # instance相当于user
        instance.set_password(password)
        instance.save()
