from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, Http404

from estudiantes.models import Estudiante
from materias.models import Paralelo, Materia, Periodo

import json
import time
from itertools import combinations
from math import factorial as f

@login_required
def generador(request):
    estudiante = Estudiante.objects.get(uid=request.user.id)
    if not estudiante.is_config:
        return redirect('estudiante:config')
    materias = serializers.serialize('json', estudiante.inscripcion.all())
    data = list()
    for ins in estudiante.inscripcion.all():
        mat = json.loads(serializers.serialize('json', [ins,]))[0]
        data.append({
            'materia':mat, 
            'paralelo':json.loads(serializers.serialize('json', Paralelo.objects.filter(id_materia=ins.pk)))})

    return render_to_response('generador.html', {'materias': data},context_instance=RequestContext(request))

def generar(request):
    if request.is_ajax():
        init = time.time()

        if request.GET['lista'] == '':
            return HttpResponse(
                json.dumps({'null': True}
                    ), content_type="application/json; charset=uft8")
        simbolos = request.GET['lista'].split(';')
        materias = []
        lmp = []
        lp = []
        m = ''
        mat = ''
        for s in simbolos:
            if m != s[:7]:
                m = s[:7]
                mat = Materia.objects.get(sigla = m)
                materias.append(mat)
                lmp.append(lp)
                lp = []
                paralelo = Paralelo.objects.get(
                    id_materia = mat, 
                    sigla_paralelo = s[7:])
                periodo = Periodo.objects.filter(
                    id_paralelo = paralelo)
                lp.append((paralelo, periodo))
            else: 
                paralelo = Paralelo.objects.get(
                    id_materia = mat, 
                    sigla_paralelo = s[7:])
                periodo = Periodo.objects.filter(
                    id_paralelo = paralelo)
                lp.append((paralelo, periodo))
        else:
            lmp.append(lp)
        del lmp[0]

        per = permutations_no_repeat(map(lambda x: len(x), lmp))

        listgen = []
        diasT = ('LUNES','MARTES','MIERCOLES','JUEVES','VIERNES','SABADO')
        horasT = (8,10,12,14,16,18,20)
        sw = True
        for combinacion in per:
            genhorario = [ [""] * 6 for x in [''] * 7]
            for pos in range(len(combinacion)):

                nombre_mat = materias[pos]
                paralelo = lmp[pos][combinacion[pos]][0]
                sigla_par = paralelo.sigla_paralelo
                periodo = lmp[pos][combinacion[pos]][1]

                sw = True
                for hora in periodo:
                    hr = horasT.index(hora.hora_inicio.hour)
                    dia = diasT.index(hora.dia)
                    if genhorario[hr][dia] == '':
                        genhorario[hr][dia] = nombre_mat.sigla + " '"+sigla_par+ "'"
                    else:
                        sw = False
                        break
                if not sw:
                    break
            if sw:
                listgen.append(genhorario)
        runtime = time.time() - init
        return HttpResponse(
            json.dumps({
                'null': False,
                'listgen':listgen, 
                'runtime': '{:.4}'.format(runtime)}), 
            content_type="application/json; charset=uft8")
    else:
        raise Http404

def permutations_no_repeat(source):
    n = len(source)
    s = reduce(lambda x,y: x*y, source)
    # print s
    pos = n - 1
    per = [0] * n
    for x in range(s):
        yield per
        if per[pos] + 1 < source[pos]:
            per[pos] += 1
        else:
            per[pos] = 0
            for y in range(1,n):
                if per[pos-y] == source[pos-y] - 1:
                    per[pos-y] = 0
                else:
                    per[pos-y] += 1
                    break