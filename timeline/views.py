from django.shortcuts import render, render_to_response ,redirect
from django.template import Template, Context
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.utils.dateformat import DateFormat, TimeFormat
from django.utils.formats import get_format
from django.utils.timezone import localtime
from django.core import serializers

from .models import Comentario, Respuesta
from estudiantes.models import Estudiante
from materias.models import Materia, Paralelo, RecordAcademico

import json
from datetime import datetime

@login_required
def home(request):
    estudiante = Estudiante.objects.get(uid=request.user)
    if estudiante.is_config:
        data = list()
        for mat in estudiante.inscripcion.all():
            comentario = Comentario.objects.filter(materia=mat)
            for comentario in comentario:
                data.append({ 
                    'titulo': comentario.comentario, 
                    'materia': comentario.materia, 
                    'estudiante': comentario.estudiante, 
                    'fecha': localtime(comentario.fecha) 
                })
        data = sorted(data, key=lambda x: x['fecha'], reverse=True)
        materias = [x.sigla for x in estudiante.inscripcion.all()]
        return render(request, 'home.html', 
            {'comentarios':data, 'materias':materias})
    else:
        return redirect('config')

@login_required
def guardar_comentario(request):
    if request.is_ajax():
        estudiante = Estudiante.objects.get(uid=request.user)

        if request.POST['comentario']:
            materia = Materia.objects.get(sigla=request.POST['sigla'])
            comentario = Comentario(comentario=request.POST['comentario'], estudiante=estudiante, materia=materia)
            comentario.save()

        data = list()
        for mat in estudiante.inscripcion.all():
            comentario = Comentario.objects.filter(materia=mat)
            for comentario in comentario:
                data.append({ 
                    'titulo': comentario.comentario, 
                    'materia': comentario.materia, 
                    'estudiante': comentario.estudiante, 
                    'fecha': localtime(comentario.fecha) 
                })
        data = sorted(data, key=lambda x: x['fecha'], reverse=True)
        raw_t = '''
        <div class="comm">
            <div class="header-comm">
                <div class="av">
                    <a href="{{ estudiante.social_url }}">
                    <img title="{{ estudiante.name }}" src="{{ estudiante.avatar }}" alt="avatar">
                    </a>
                </div>
                <div class="desc">
                    <h4>{{ estudiante.name }}</h4>
                    <span title="{{ fecha }}">{{ fecha|date }}</span>
                </div>
                <span class="sigla-comm">{{ materia.sigla }}</span>
            </div>
            <div class="text-comm">{{ titulo }}</div>
        </div>
        '''
        t = Template(raw_t)
        data_render = list()
        for x in data:
            c = Context({
                'estudiante':x['estudiante'],
                'materia':x['materia'],
                'titulo': x['titulo'],
                'fecha':x['fecha']
            })
            data_render.append(t.render(c))

        return HttpResponse(
            json.dumps({ 'comentarios': data_render }),
            content_type="application/json; charset=uft8"
            )
    else:
        raise Http404

@login_required
def cargar_respuestas(request, id):
    if request.is_ajax():
        respuestas = Respuesta.objects.filter(comentario__id=id).order_by('-id')

        data = list()
        for respuesta in respuestas:
            data.append(respuesta.titulo)

        return HttpResponse(
            json.dumps({'respuestas': data, 'comentario': id}),
            content_type="application/json; charset=uft8"
            )
    else:
        raise Http404

@login_required
def guardar_respuesta(request):
    if request.is_ajax():
        if request.POST['respuesta']:
            respuesta = Respuesta(titulo=request.POST['respuesta'], comentario_id=request.POST['comentario'])
            respuesta.save()
        return cargar_respuestas(request, request.POST['comentario'])
    else:
        raise Http404

@login_required
def conocidos(request):
    from materias.utils import gestion_actual
    estudiante = Estudiante.objects.get(uid=request.user)
    mis_materias = estudiante.inscripcion.all()
    data = list()
    for mat in mis_materias:
        paralelo = list()
        for par_mat in Paralelo.objects.filter(id_materia=mat):
            ests_in_mat = mat.materias_inscritas.all()
            ests = list()
            for est in ests_in_mat:
                mats_ests = RecordAcademico.objects.filter(estudiante=est, materia=mat, gestion=gestion_actual())
                if mats_ests and mats_ests[0].sigla_paralelo == par_mat.sigla_paralelo:
                    ests.append(est)
            paralelo.append([par_mat, ests])
        data.append({
            'materia':mat, 
            'paralelo': paralelo})

    return render(request, 'conocidos.html', {'data':data})