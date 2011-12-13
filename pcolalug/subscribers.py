from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.security import has_permission

def my_has_permission(request, perm):
    return has_permission(perm, request.context, request)

@subscriber(BeforeRender)
def add_global(event):
    event['has_permission'] = my_has_permission
