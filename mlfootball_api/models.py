# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
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
    id = models.BigAutoField(primary_key=True)
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


class Stats(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.CharField(max_length=4, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    league_id = models.IntegerField(blank=True, null=True)
    league = models.CharField(max_length=40, blank=True, null=True)
    team1 = models.CharField(max_length=40, blank=True, null=True)
    team2 = models.CharField(max_length=40, blank=True, null=True)
    spi1 = models.FloatField(blank=True, null=True)
    spi2 = models.FloatField(blank=True, null=True)
    prob1 = models.FloatField(blank=True, null=True)
    prob2 = models.FloatField(blank=True, null=True)
    probtie = models.FloatField(blank=True, null=True)
    proj_score1 = models.FloatField(blank=True, null=True)
    proj_score2 = models.FloatField(blank=True, null=True)
    importance1 = models.FloatField(blank=True, null=True)
    importance2 = models.FloatField(blank=True, null=True)
    score1 = models.FloatField(blank=True, null=True)
    score2 = models.FloatField(blank=True, null=True)
    xg1 = models.FloatField(blank=True, null=True)
    xg2 = models.FloatField(blank=True, null=True)
    nsxg1 = models.FloatField(blank=True, null=True)
    nsxg2 = models.FloatField(blank=True, null=True)
    adj_score1 = models.FloatField(blank=True, null=True)
    adj_score2 = models.FloatField(blank=True, null=True)
    hometeam = models.CharField(db_column='HomeTeam', max_length=24, blank=True, null=True)  # Field name made lowercase.
    awayteam = models.CharField(db_column='AwayTeam', max_length=24, blank=True, null=True)  # Field name made lowercase.
    ftr = models.CharField(db_column='FTR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shots1 = models.FloatField(blank=True, null=True)
    shots2 = models.FloatField(blank=True, null=True)
    shotsot1 = models.FloatField(blank=True, null=True)
    shotsot2 = models.FloatField(blank=True, null=True)
    fouls1 = models.FloatField(blank=True, null=True)
    fouls2 = models.FloatField(blank=True, null=True)
    corners1 = models.FloatField(blank=True, null=True)
    corners2 = models.FloatField(blank=True, null=True)
    yellow1 = models.FloatField(blank=True, null=True)
    yellow2 = models.FloatField(blank=True, null=True)
    red1 = models.FloatField(blank=True, null=True)
    red2 = models.FloatField(blank=True, null=True)
    maxh = models.FloatField(db_column='MaxH', blank=True, null=True)  # Field name made lowercase.
    maxd = models.FloatField(db_column='MaxD', blank=True, null=True)  # Field name made lowercase.
    maxa = models.FloatField(db_column='MaxA', blank=True, null=True)  # Field name made lowercase.
    avgh = models.FloatField(db_column='AvgH', blank=True, null=True)  # Field name made lowercase.
    avgd = models.FloatField(db_column='AvgD', blank=True, null=True)  # Field name made lowercase.
    avga = models.FloatField(db_column='AvgA', blank=True, null=True)  # Field name made lowercase.
    max_over25 = models.FloatField(db_column='Max_over25', blank=True, null=True)  # Field name made lowercase.
    max_under25 = models.FloatField(db_column='Max_under25', blank=True, null=True)  # Field name made lowercase.
    avg_over25 = models.FloatField(db_column='Avg_over25', blank=True, null=True)  # Field name made lowercase.
    avg_under25 = models.FloatField(db_column='Avg_under25', blank=True, null=True)  # Field name made lowercase.
    avg_xg1 = models.FloatField(blank=True, null=True)
    avg_xg2 = models.FloatField(blank=True, null=True)
    adj_avg_xg1 = models.FloatField(blank=True, null=True)
    adj_avg_xg2 = models.FloatField(blank=True, null=True)
    pts1 = models.IntegerField(blank=True, null=True)
    pts2 = models.IntegerField(blank=True, null=True)
    xwin1 = models.FloatField(blank=True, null=True)
    xdraw = models.FloatField(blank=True, null=True)
    xwin2 = models.FloatField(blank=True, null=True)
    xpts1 = models.FloatField(blank=True, null=True)
    xpts2 = models.FloatField(blank=True, null=True)
    xgshot1 = models.FloatField(blank=True, null=True)
    xgshot2 = models.FloatField(blank=True, null=True)
    convrate1 = models.FloatField(blank=True, null=True)
    convrate2 = models.FloatField(blank=True, null=True)
    cards1 = models.FloatField(blank=True, null=True)
    cards2 = models.FloatField(blank=True, null=True)
    matchday = models.FloatField(blank=True, null=True)
    matchday_away = models.FloatField(blank=True, null=True)


    def __str__(self):
        return f'{self.team1} v {self.team2} @ {self.date}'


    class Meta:
        managed = False
        db_table = 'stats'
