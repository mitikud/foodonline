 # Signals
from  django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import User, UserProfile
    # method one
    # def post_save_profile_receiver(sender, instance, created,**Kwargs):
    #     pass

    # post_save.connect(post_save_profile_receiver, sender=User)

    # method two
@receiver(post_save, sender=User)
def post_save_profile_receiver(sender, instance, created,**Kwargs):
    print(created,instance)
    if created:
        UserProfile.objects.create(user = instance)
        print("created the user profile")
    else:
        try:
            profile =  UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create a UserProfile ifnot exists
            UserProfile.objects.create(user = instance)
            print("prfile was not exist and I created one")
        print("updated the user profile")


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **Kwargs):
    print(instance.username, "this is being saved")

