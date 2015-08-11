from .models import Estudiante
from social.pipeline.partial import partial

@partial
def get_user_avatar(strategy, backend, details, response, uid, user=None, is_new=False, *args, **kwargs):
    url = None
    username_url = None
    print '*' * 30
    print details
    print uid
    print '*' * 30

    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % uid
        social_url = 'http://facebook.com/%s' % details['username']
 
    elif backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
        social_url = 'http://twitter.com/%s' % details['username']

    if url:
        est, created = Estudiante.objects.get_or_create(uid=user)
        if created:
            est.name = details['fullname']
            est.avatar = url
            est.social_network = backend.name
            est.social_url = social_url
            est.email = details['email']
            est.save()

