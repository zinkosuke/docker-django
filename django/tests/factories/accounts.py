from django.contrib.auth import get_user_model

User = get_user_model()


def superuser():
    user, c = User.objects.get_or_create(
        username="admin",
        email="admin@example.com",
        is_superuser=True,
        is_staff=True,
        is_active=True,
    )
    if c:
        user.set_password("admin")
        user.save()
    return user
