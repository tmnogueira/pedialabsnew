# -*- coding: utf-8 -*-
# flake8: noqa
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RstPlotBlock'
        db.create_table(u'rstplot_rstplotblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'rstplot', ['RstPlotBlock'])


    def backwards(self, orm):
        # Deleting model 'RstPlotBlock'
        db.delete_table(u'rstplot_rstplotblock')


    models = {
        u'rstplot.rstplotblock': {
            'Meta': {'object_name': 'RstPlotBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['rstplot']
