from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('main__page')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def authenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('main__page')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def authenticated_redirect_login_page(view_func):
	def wrapper_func(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return redirect('sign__in__page')
		else:
			return view_func(self, request, *args, **kwargs)

	return wrapper_func

'''
def super_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_superuser:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('main__page')

	return wrapper_func

def staff(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_staff:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('main__page')

	return wrapper_func
'''