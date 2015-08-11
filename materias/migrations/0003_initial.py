# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Modulo'
        db.create_table(u'materias_modulo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'materias', ['Modulo'])

        # Adding model 'Materia'
        db.create_table(u'materias_materia', (
            ('sigla', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('is_save_paralelo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('modulo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['materias.Modulo'])),
        ))
        db.send_create_signal(u'materias', ['Materia'])

        # Adding M2M table for field pre_requisito on 'Materia'
        m2m_table_name = db.shorten_name(u'materias_materia_pre_requisito')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_materia', models.ForeignKey(orm[u'materias.materia'], null=False)),
            ('to_materia', models.ForeignKey(orm[u'materias.materia'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_materia_id', 'to_materia_id'])

        # Adding M2M table for field materias_inscritas on 'Materia'
        m2m_table_name = db.shorten_name(u'materias_materia_materias_inscritas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('materia', models.ForeignKey(orm[u'materias.materia'], null=False)),
            ('estudiante', models.ForeignKey(orm[u'estudiantes.estudiante'], null=False))
        ))
        db.create_unique(m2m_table_name, ['materia_id', 'estudiante_id'])

        # Adding model 'Paralelo'
        db.create_table(u'materias_paralelo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre_docente', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('sigla_paralelo', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id_materia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['materias.Materia'])),
        ))
        db.send_create_signal(u'materias', ['Paralelo'])

        # Adding model 'Periodo'
        db.create_table(u'materias_periodo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dia', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('hora_inicio', self.gf('django.db.models.fields.TimeField')(max_length=6)),
            ('hora_final', self.gf('django.db.models.fields.TimeField')(max_length=6)),
            ('aula', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('id_paralelo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['materias.Paralelo'])),
        ))
        db.send_create_signal(u'materias', ['Periodo'])

        # Adding model 'RecordAcademico'
        db.create_table(u'materias_recordacademico', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estudiante', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['estudiantes.Estudiante'])),
            ('materia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['materias.Materia'])),
            ('sigla_paralelo', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('nota', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=5, decimal_places=2)),
            ('gestion', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal(u'materias', ['RecordAcademico'])

        # Adding unique constraint on 'RecordAcademico', fields ['estudiante', 'materia']
        db.create_unique(u'materias_recordacademico', ['estudiante_id', 'materia_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'RecordAcademico', fields ['estudiante', 'materia']
        db.delete_unique(u'materias_recordacademico', ['estudiante_id', 'materia_id'])

        # Deleting model 'Modulo'
        db.delete_table(u'materias_modulo')

        # Deleting model 'Materia'
        db.delete_table(u'materias_materia')

        # Removing M2M table for field pre_requisito on 'Materia'
        db.delete_table(db.shorten_name(u'materias_materia_pre_requisito'))

        # Removing M2M table for field materias_inscritas on 'Materia'
        db.delete_table(db.shorten_name(u'materias_materia_materias_inscritas'))

        # Deleting model 'Paralelo'
        db.delete_table(u'materias_paralelo')

        # Deleting model 'Periodo'
        db.delete_table(u'materias_periodo')

        # Deleting model 'RecordAcademico'
        db.delete_table(u'materias_recordacademico')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'estudiantes.estudiante': {
            'Meta': {'object_name': 'Estudiante'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'cod_estudiante': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_config': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'social_network': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'social_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'uid': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'materias.materia': {
            'Meta': {'object_name': 'Materia'},
            'is_save_paralelo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'materias_inscritas': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'inscripcion'", 'symmetrical': 'False', 'to': u"orm['estudiantes.Estudiante']"}),
            'modulo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['materias.Modulo']"}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'pre_requisito': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['materias.Materia']", 'null': 'True', 'blank': 'True'}),
            'record_academico': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['estudiantes.Estudiante']", 'through': u"orm['materias.RecordAcademico']", 'symmetrical': 'False'}),
            'sigla': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'})
        },
        u'materias.modulo': {
            'Meta': {'object_name': 'Modulo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'materias.paralelo': {
            'Meta': {'object_name': 'Paralelo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_materia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['materias.Materia']"}),
            'nombre_docente': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'sigla_paralelo': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'materias.periodo': {
            'Meta': {'object_name': 'Periodo'},
            'aula': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'dia': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hora_final': ('django.db.models.fields.TimeField', [], {'max_length': '6'}),
            'hora_inicio': ('django.db.models.fields.TimeField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_paralelo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['materias.Paralelo']"})
        },
        u'materias.recordacademico': {
            'Meta': {'unique_together': "(('estudiante', 'materia'),)", 'object_name': 'RecordAcademico'},
            'estudiante': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['estudiantes.Estudiante']"}),
            'gestion': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['materias.Materia']"}),
            'nota': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'}),
            'sigla_paralelo': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['materias']