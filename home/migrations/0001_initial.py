# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table('home_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('garage', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('space', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('home', ['Location'])

        # Adding model 'Pub_Transaction'
        db.create_table('home_pub_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(default='CASH', max_length=4)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('loc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Location'])),
        ))
        db.send_create_signal('home', ['Pub_Transaction'])

        # Adding model 'UID_Transaction'
        db.create_table('home_uid_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('loc', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Location'])),
            ('rate', self.gf('django.db.models.fields.CharField')(default='REGULAR', max_length=7)),
        ))
        db.send_create_signal('home', ['UID_Transaction'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table('home_location')

        # Deleting model 'Pub_Transaction'
        db.delete_table('home_pub_transaction')

        # Deleting model 'UID_Transaction'
        db.delete_table('home_uid_transaction')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'home.location': {
            'Meta': {'object_name': 'Location'},
            'garage': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'space': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'home.pub_transaction': {
            'Meta': {'object_name': 'Pub_Transaction'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.Location']"}),
            'method': ('django.db.models.fields.CharField', [], {'default': "'CASH'", 'max_length': '4'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'home.uid_transaction': {
            'Meta': {'object_name': 'UID_Transaction'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loc': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.Location']"}),
            'rate': ('django.db.models.fields.CharField', [], {'default': "'REGULAR'", 'max_length': '7'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['home']