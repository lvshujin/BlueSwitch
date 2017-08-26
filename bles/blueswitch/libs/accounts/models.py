"""
Provide model user and user-account related models.
"""
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Store User account details.
    """
    email = models.EmailField(_('email address'), max_length=255, unique=True, db_index=True,)
    username = models.CharField(_('username'), max_length=255, unique=True, db_index=True,)
    name = models.CharField(_('name'), max_length=255)
    paired_users = models.ManyToManyField('self', symmetrical=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active.  Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Social accounts
    facebook_uid = models.CharField(max_length=32, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['name', 'email']

    def __str__(self):
        return '{name} <{email}>'.format(
            name=self.name,
            email=self.email,
        )

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class TempToken(models.Model):
    """
    Store token  of user in case of forgot password.
    """
    user = models.ForeignKey(User, verbose_name=_('user'), related_name="temp_token")
    token = models.CharField(_('activation key'), max_length=40)
    created_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.name


# class EmailVerification(models.Model):
#     """
#     Store token of user to verify user email.
#     """
#     user = models.ForeignKey(User, verbose_name=_('user'), related_name="email_verification_token")
#     token = models.CharField(_('activation key'), max_length=40)
#     is_expired = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.name
