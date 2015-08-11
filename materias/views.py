from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, Http404

from .utils import gestion_actual
from estudiantes.models import Estudiante
from materias.models import Paralelo, Periodo, Materia, RecordAcademico

import json

@login_required
def horario(request):
	estudiante = Estudiante.objects.get(uid=request.user)
	materias = serializers.serialize('json', estudiante.inscripcion.all())
	data = list()
	for ins in estudiante.inscripcion.all():
		mat = json.loads(serializers.serialize('json', [ins,]))[0]
		data.append({
			'materia':mat, 
			'paralelo':(p.sigla_paralelo for p in Paralelo.objects.filter(id_materia=ins.pk))})

	return render(request, 'horario.html', {'materias': data, 'gestion_actual':gestion_actual()})

def inscripcion(request):
	if request.is_ajax():
		estudiante = Estudiante.objects.get(uid=request.user)
		mats = RecordAcademico.objects.filter(estudiante=estudiante, gestion=gestion_actual())
		list_periodo = list()
		for m in mats:
			list_periodo += periodos_materia(m.materia.sigla+m.sigla_paralelo)
		return HttpResponse(
			json.dumps({'periodos':list_periodo}),
			content_type='application/json; charset=uft-8')
	else:
		raise Http404

def materia(request):
	if request.is_ajax():
		value = request.GET['materia']
		mat = value[:-1]
		return HttpResponse(
			json.dumps({'periodos':periodos_materia(value), 'mat':mat}), 
			content_type='application/json; charset=utf-8')
	else:
		raise Http404

def periodos_materia(sigla_materia):
	mat = sigla_materia[:-1]
	par = sigla_materia[-1:]
	materia = Materia.objects.get(sigla=mat)
	paralelo = Paralelo.objects.get(id_materia=materia, sigla_paralelo=par)
	periodo = Periodo.objects.filter(id_paralelo = paralelo)
	list_periodo = list()
	for pe in periodo:
		list_periodo.append({
			'per':'{}{}-{}'.format(pe.dia[:2], pe.hora_inicio.hour, pe.hora_final.hour),
			'nombre_materia': materia.nombre,
			'nombre_docente': paralelo.nombre_docente,
			'aula': pe.aula,
			'sigla':mat})
	return list_periodo