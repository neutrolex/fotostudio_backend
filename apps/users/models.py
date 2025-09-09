from django.db import models

# Create your models here.

class DocumentTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'document_types'

    def __str__(self):
        return self.name

class AuthGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'

    def __str__(self):
        return self.name

class AuthPermission(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'

    def __str__(self):
        return self.name

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    document_number = models.CharField(unique=True, max_length=255)
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    paternal_lastname = models.CharField(max_length=255)
    maternal_lastname = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    sex = models.CharField(max_length=1, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=150)
    password_change = models.BooleanField(default=False)
    last_session = models.DateTimeField(auto_now=True)
    account_statement = models.CharField(max_length=1, choices=[('A', 'A'), ('I', 'I')], default='A')
    email_verified_at = models.DateTimeField(blank=True, null=True)
    document_type_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return f"{self.name} {self.paternal_lastname}"

class UsersGroups(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    group_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'users_groups'
        unique_together = (('user_id', 'group_id'),)

class UsersUserPermissions(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    permission_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'users_user_permissions'
        unique_together = (('user_id', 'permission_id'),)

class UsersVerificationCode(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    expires_at = models.DateTimeField()
    failed_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'users_verification_code'
        unique_together = (('user_id',),)