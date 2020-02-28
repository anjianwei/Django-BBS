import hashlib
from urllib.parse import urlencode

from django import template

register = template.Library()


@register.filter
def gravatar(user):
    email = user.email.lower().encode('utf-8')
    size = 256
    default = 'mm'
    return "https://www.gravatar.com/avatar/%s?%s" % (
        hashlib.md5(email).hexdigest(), urlencode({'d': default, 's': str(size)}))
