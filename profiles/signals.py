# from django.db.models.signals.post_save
# from django.dispatch import receiver
# from profiles.models import Profile
# from django.contrib.auth.models import User

# @receiver(post_save, sender=User)
# def profile_create(sender, instance,created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

