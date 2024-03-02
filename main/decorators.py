from django.http import HttpResponse
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            print(request.user.role)
            if request.user.role == 'INVENTOR' or request.user.role == 'ADMIN' :
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("You are not authorized")
        return wrapper_func
    return decorator
def onlyAdmin():
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            print(request.user.role)
            if request.user.role == 'ADMIN':
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("You are not authorized")
        return wrapper_func
    return decorator