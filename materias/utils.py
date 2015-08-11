from django.utils import timezone

def gestion_actual():
	current_date = timezone.now()
	year = current_date.year
	month =  current_date.month
	# month =  5
	if month == 1:
		return 'Ver/%s' % str(year)[2:]

	if month < 7:
		return '1/%s' % str(year)[2:]

	if month == 7:
		return 'Inv/%s' % str(year)[2:]
	else:
		return '2/%s' % str(year)[2:]