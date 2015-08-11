from estudiantes.models import Estudiante

def est(request):
	if request.user.is_authenticated():
		try:
			estudiante = Estudiante.objects.get(uid=request.user)
		except:
			return {}
		return {'estudiante': estudiante}
	else:
		return {}
