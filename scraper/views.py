from django.shortcuts import render, render_to_response ,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

from estudiantes.models import Estudiante
from materias.models import Materia
from timeline.models import Comentario
from .forms import PensumForm
from .parser import save_record, save_inscrito, save_horarios, save_pensum

import urllib2
import json
from bs4 import BeautifulSoup

def config_pensum(request):
    if request.method == 'POST':
        form = PensumForm(request.POST)
        if form.is_valid():
            for x in form:
                save_pensum(x.value())
            return redirect('login')
    else:
        form = PensumForm()
        return render_to_response('config_pensum.html',{'form':form} ,context_instance=RequestContext(request))

@login_required
def config(request):
    estudiante = Estudiante.objects.get(uid=request.user)
    if estudiante.is_config:
        return redirect('home')
    else:
        url_prueba = 'http://sia.informatica.edu.bo'
        page = urllib2.urlopen(url_prueba)
        siaurl = 'http://sia.informatica.edu.bo//sia/www/'+page.geturl().split('/')[5]+'/presentacion.php'
        return render(request, 'config.html',{
            'siaurl':siaurl})

@login_required
def scraper(request):
    if request.is_ajax() and request.POST['siaurl']:
        siaurl = request.POST['siaurl']
        print siaurl
        estudiante = Estudiante.objects.get(uid=request.user)
        return function_scrap(siaurl, estudiante)
    else:
        raise Http404

@login_required
def update(request):
    estudiante = Estudiante.objects.get(uid=request.user)
    url_prueba = 'http://sia.informatica.edu.bo'
    page = urllib2.urlopen(url_prueba)
    siaurl = 'http://sia.informatica.edu.bo/sia/www/'+page.geturl().split('/')[5]+'/indice.php'
    return render(request, 'update.html',{
        'siaurl':siaurl})

@login_required
def update_scraper(request):
    if request.is_ajax() and request.POST['siaurl']:
        siaurl = request.POST['siaurl']
        estudiante = Estudiante.objects.get(uid=request.user)
        return function_scrap(siaurl, estudiante)
    else:
        raise Http404

def function_scrap(siaurl, estudiante):
    print 'token'
    print siaurl.split('/')[5]
    base_url = 'http://sia.informatica.edu.bo/sia/www/'

    page = urllib2.urlopen(
        base_url
        +siaurl.split('/')[5]
        +'/mostrar_informe_materias_a_cursar.php')
    url_compare = page.geturl().split('/')[6]
    print 'url_compare'
    print url_compare
    if 'mostrar_informe_materias_a_cursar.php' == url_compare:
        token = page.geturl().split('/')[5]
        print token

        page_record = urllib2.urlopen(base_url+token+'/mostrar_informe_record_academico_segun_pensum.php')
        record = BeautifulSoup(page_record.read())

        page_inscrito = urllib2.urlopen(base_url+token+'/mostrar_informe_inscripcion.php')
        inscrito = BeautifulSoup(page_inscrito.read())

        page_horario = urllib2.urlopen(base_url+token+'/mostrar_informe_horario_estudiante.php')
        horarios = BeautifulSoup(page_horario.read())
        print 'SCRAP OK'
        save_record(record, estudiante)
        save_inscrito(inscrito, estudiante)
        save_horarios(horarios, estudiante)
        estudiante.is_config = True
        estudiante.save()
        return HttpResponse(
            json.dumps({'save':True}),
            content_type="application/json; charset=uft8"
        )
    else:
        return HttpResponse(
            json.dumps({'save':False}),
            content_type="application/json; charset=uft8"
        )