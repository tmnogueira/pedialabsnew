# -*- coding: utf-8 -*-
# flake8: noqa
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lab'
        db.create_table(u'exercises_lab', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('assessment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sickvisit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('correct_actionplan', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
        ))
        db.send_create_signal(u'exercises', ['Lab'])

        # Adding model 'Test'
        db.create_table(u'exercises_test', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Lab'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('ordinality', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('normal_range', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('result_level', self.gf('django.db.models.fields.CharField')(default='normal', max_length=256)),
            ('abnormality', self.gf('django.db.models.fields.CharField')(default='none', max_length=256)),
        ))
        db.send_create_signal(u'exercises', ['Test'])

        # Adding model 'TestResponse'
        db.create_table(u'exercises_testresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Test'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('result_level', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('abnormality', self.gf('django.db.models.fields.CharField')(default='none', max_length=256)),
        ))
        db.send_create_signal(u'exercises', ['TestResponse'])

        # Adding model 'ActionPlanResponse'
        db.create_table(u'exercises_actionplanresponse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exercises.Lab'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('action_plan', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
            ('assessment', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'exercises', ['ActionPlanResponse'])


    def backwards(self, orm):
        # Deleting model 'Lab'
        db.delete_table(u'exercises_lab')

        # Deleting model 'Test'
        db.delete_table(u'exercises_test')

        # Deleting model 'TestResponse'
        db.delete_table(u'exercises_testresponse')

        # Deleting model 'ActionPlanResponse'
        db.delete_table(u'exercises_actionplanresponse')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'exercises.actionplanresponse': {
            'Meta': {'object_name': 'ActionPlanResponse'},
            'action_plan': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'assessment': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Lab']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'exercises.lab': {
            'Meta': {'object_name': 'Lab'},
            'assessment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'correct_actionplan': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sickvisit': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'exercises.test': {
            'Meta': {'ordering': "('lab', 'ordinality')", 'object_name': 'Test'},
            'abnormality': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Lab']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'normal_range': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'ordinality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'result_level': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '256'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'exercises.testresponse': {
            'Meta': {'object_name': 'TestResponse'},
            'abnormality': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result_level': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exercises.Test']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'pagetree.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'base_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'pagetree.pageblock': {
            'Meta': {'ordering': "('section', 'ordinality')", 'object_name': 'PageBlock'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'css_extra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ordinality': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pagetree.Section']"})
        },
        u'pagetree.section': {
            'Meta': {'object_name': 'Section'},
            'deep_toc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hierarchy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pagetree.Hierarchy']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'show_toc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['exercises']
