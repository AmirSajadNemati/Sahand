from django.db import models


class ContactUs(models.Model):
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='contact_us_content')

    class Meta:
        db_table = 'front_contact_us'


class Rule(models.Model):
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='rule_content')

    class Meta:
        db_table = 'front_rule'


class AboutUs(models.Model):
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='about_us_content')

    class Meta:
        db_table = 'front_about_uss'


class Privacy(models.Model):
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='privacy_content')

    class Meta:
        db_table = 'front_privacy'


class Bug(models.Model):
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='bug_content')

    class Meta:
        db_table = 'front_bug'


class Criticism(models.Model):
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='criticism_content')

    class Meta:
        db_table = 'front_criticism'


class Suggestion(models.Model):
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='suggestion_content')

    class Meta:
        db_table = 'front_suggestion'


class Complaint(models.Model):
    content = models.ForeignKey('content_manager.ContentManager', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='complaint_content')

    class Meta:
        db_table = 'front_complaint'
