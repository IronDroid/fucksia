from materias.models import Materia, Modulo, RecordAcademico, Paralelo, Periodo

import urllib2
import datetime
from bs4 import BeautifulSoup

# guarda el pensum B
def save_pensum(urltext):
	print urltext
	page = urllib2.urlopen(urltext)
	soup = BeautifulSoup(page.read())
	tables= soup('table')
	n = 0
	for x in tables:
		n = n + 1
		modulo = Modulo()
		if n > 3:
			# nombre del modulo
			modulo.nombre = x.find('th').get_text()
			modulo.save()
			materia = Materia()
			materias = [x.get_text() for x in x.find_all('td')]
			for y in xrange(0, len(materias), 3):
				materia.sigla = materias[y]
				materia.nombre = materias[y + 1]
				materia.modulo = modulo
				materia.save()
				if len(materias[y + 2].split(' ', 1)) > 0 and materias[y + 2].split(' ', 1)[0] != '':
					mats = [Materia.objects.get(sigla=sig) for sig in materias[y + 2].split(' ', 1)]
					materia.pre_requisito = mats

def save_record(soup, estudiante):
	tables= soup('table')
	print tables
	n = 0
	for x in tables:
		n = n + 1
		if n == 2:
			credentials = [y.get_text() for y in x.find_all('td')]
			estudiante.cod_estudiante = credentials[0]
			print credentials[0]
			print credentials[1]
			estudiante.name = credentials[1]
			estudiante.save()
		if n > 4 and n < len(tables):
			for y in x.find_all('tr'):
				if y.get('class') != None:
					# materias y notas
					notas = [td.get_text() for td in y.find_all('td')]
					for linea in xrange(0, len(notas), 4):
						materia = notas[linea:linea + 4]
						record, boo = RecordAcademico.objects.get_or_create(
							estudiante=estudiante, 
							materia=Materia.objects.get(sigla=materia[0][:7]))
						record.nota = materia[2]
						record.gestion = materia[3]
						record.save()

def save_inscrito(soup, estudiante):
	tables= soup('table')
	n = 0
	for x in tables:
		n = n + 1
		if n == 3:
			gestion_actual = x.find('td').get_text()
		if n == 4:
			for y in x.find_all('tr'):
				if y.get('class') != None:
					# materias inscritas
					materias = [z.get_text() for z in y.find_all('td')]
					for c in xrange(0,len(materias), 3):
						materi = materias[c:c+3]
						record, _ = RecordAcademico.objects.get_or_create(
							estudiante=estudiante, 
							materia=Materia.objects.get(sigla=materi[0][:7]))
						record.sigla_paralelo = materi[1]
						record.nota = 0
						record.gestion = gestion_actual
						record.save()

def save_horarios(soup, estudiante):
	tables= soup('table')
	n = 0
	materias = list()
	for x in tables:
		n = n + 1
		if n > 3 :
			materia = Materia()
			gm = False
			for tr in x.find_all('tr'):
				if len(tr.find_all('th')) == 1:
					th = tr.find('th')
					th = th.get_text().split(' ', 1)[0]
					if len(th) > 8:
						materia = Materia.objects.get(sigla=th[len(th)-7:])
						materias.append(materia)
						if not materia.is_save_paralelo:
							materia.is_save_paralelo = True
							materia.save()
							gm = True
						else:
							gm = False
				else:
					if gm:
						paralelo = Paralelo()
						for td in tr.find_all('td'):
							if td.find_all('br') != None:
								horas = [tdx for tdx in td if len(tdx) > 6]
								if len(horas) == 1:
									paralelo.nombre_docente = horas[0]
								if len(td.get_text()) == 1:
									paralelo.sigla_paralelo = td.get_text()
								if len(horas) == 2:
									paralelo.id_materia = materia
									paralelo.save()
									for per in horas:
										periodo = Periodo()
										periodo.dia = per.split(' ', 1)[0]
										hi = per.split(' ')[1].split(':')
										periodo.hora_inicio = datetime.time(int(hi[0]),int(hi[1]),0)
										hf = per.split(' ')[3].split(':')
										periodo.hora_final = datetime.time(int(hf[0]),int(hf[1]),0)
										periodo.aula = per.split(' ', 4)[4]
										periodo.id_paralelo = paralelo
										periodo.save()
									paralelo = Paralelo()
	estudiante.inscripcion = materias