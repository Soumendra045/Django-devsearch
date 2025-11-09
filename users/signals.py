from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from .models import Profile
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.conf import settings

from threading import Thread

def send_async_mail(subject, message, recipient_email):
    Thread(
        target=send_mail,
        args=(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email]),
        kwargs={'fail_silently': False}
    ).start()
# @receiver(post_save,sender=Profile)  
def createProfile(sender,instance,created,**kwargs):
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name, 
        )

        subject = 'Welcome to devsearch'
        message = 'We are glad you are here!'

        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [profile.email],
        #     fail_silently=False,
        # )
        # ←←← CHANGED: now async → no more 500 on register
        send_async_mail(subject, message, profile.email)

def updateUser(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    if created==False:
        user.first_name = profile.name
        if profile.username:  # ✅ only set if not empty
            user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender,instance,**kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(createProfile,sender=User)
post_save.connect(updateUser,sender=Profile)
post_delete.connect(deleteUser,sender=Profile)