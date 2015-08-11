from django.shortcuts import render, render_to_response ,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as social_logout
from django.http import HttpResponse, Http404

from .models import Estudiante
from .forms import EstudianteForm
from materias.models import Materia, Modulo, RecordAcademico
from materias.utils import gestion_actual

import json

def login(request):
	if not request.user.is_authenticated():
		return render_to_response('login.html', context_instance=RequestContext(request))
	else:
		return redirect('home')

@login_required
def logout(request):
	social_logout(request)
	return redirect('login')

@login_required
def perfil(request):
	estudiante = Estudiante.objects.get(uid=request.user)
	if request.method == 'POST':
		form = EstudianteForm(request.POST, instance=estudiante)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = EstudianteForm(instance=estudiante)

	return render_to_response('perfil.html', context_instance=RequestContext(request, locals()))


@login_required
def record(request):
	import json
	list_materias = list()
	semestres = Modulo.objects.exclude(nombre='OPTATIVAS')
	for count, semestre in enumerate(semestres):
		materias = Materia.objects.filter(modulo=semestre)
		materias = [{'sigla':m.sigla, 'row':count,'col':c} for c,m in enumerate(materias)]
		list_materias.append(materias)
	return render(request, 'record.html', {'data':list_materias})

def record_grafo(request):
	if request.is_ajax():
		sigla = request.GET['sigla']
		estudiante = Estudiante.objects.get(uid=request.user)
		mat = Materia.objects.get(sigla=sigla)
		mats_habilitadas = [x.sigla for x in Materia.objects.filter(pre_requisito=mat)]
		mat = [m.sigla for m in mat.pre_requisito.all()]
		mat = mat + mats_habilitadas
		mat.append(Materia.objects.get(sigla=sigla).sigla)
		return HttpResponse(
			json.dumps({'sigla_mat':mat}),
			content_type='application/json; charset=uft-8')
	else:
		raise Http404