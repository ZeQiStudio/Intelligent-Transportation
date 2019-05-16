# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import sys
from importlib import reload

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    default_encoding

from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Carmessage(models.Model):
    licensenumber = models.CharField(db_column='licenseNumber', unique=True, max_length=20)  # Field name made lowercase.
    ownername = models.CharField(db_column='ownerName', max_length=10)  # Field name made lowercase.
    ownerid = models.CharField(db_column='ownerID', max_length=20)  # Field name made lowercase.
    isillegal = models.IntegerField(db_column='isIllegal')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'carmessage'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Iillegalmessage(models.Model):
    licensenumber = models.CharField(db_column='licenseNumber', max_length=20)  # Field name made lowercase.
    type = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    time = models.DateTimeField()
    site = models.CharField(max_length=255)
    illegalbehavior = models.CharField(db_column='illegalBehavior', max_length=20)  # Field name made lowercase.
    isdelete = models.IntegerField(db_column='isDelete')  # Field name made lowercase.
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        managed = False
        db_table = 'iillegalmessage'


class Test2(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'test2'


class Test3(models.Model):
    licensenumber = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    time = models.DateTimeField()
    site = models.CharField(max_length=20)
    illegalbehavior = models.CharField(max_length=20)
    carid = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'test3'


class Test4(models.Model):
    name = models.CharField(max_length=20)
    carid = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'test4'


class TestmodelTest2(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'testmodel_test2'


class TestmodelTest3(models.Model):
    licensenumber = models.CharField(db_column='LicenseNumber', max_length=11)  # Field name made lowercase.
    type = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    time = models.DateTimeField()
    site = models.CharField(max_length=20)
    illegalbehavior = models.CharField(db_column='illegalBehavior', max_length=20)  # Field name made lowercase.
    carid = models.CharField(db_column='carID', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'testmodel_test3'


class TestmodelTest4(models.Model):
    name = models.CharField(max_length=20)
    carid = models.CharField(db_column='carID', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'testmodel_test4'
