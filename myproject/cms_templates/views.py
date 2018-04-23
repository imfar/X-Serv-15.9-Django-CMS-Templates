from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from .models import Resource
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.template.loader import get_template
from django.template import Context


title = "SARO - 15.9 - CMS TEMPLATES"
url_root = "/"


@csrf_exempt
def root_page(request):
	if request.user.is_authenticated():
		logged = "Logged in as " + request.user.username + ". "
		logged_str = "Logout"
		url_logged = "/logout"
	else:
		logged = "Not logged in. "
		url_logged = "/login"
		logged_str = "Login"
	
	recursos_DB = Resource.objects.all()
	lista = "Recursos: ["
	for my_rec in recursos_DB:
		lista += my_rec.name + '; '
	lista += "]"
	
	rec_name = "MIS RECURSOS: "
	rec_cont = lista;
				
	template = get_template("I_See_New_People/index.html")
	c = Context({'title': title, 'url_root': url_root, 'logged': logged, 
				'url_logged': url_logged, 'logged_str': logged_str, 'rec_name': rec_name,
				'rec_cont': rec_cont})
	return HttpResponse(template.render(c))		


@csrf_exempt
def annotated(request, resource):
	if request.user.is_authenticated():
		logged = "Logged in as " + request.user.username + ". "
		logged_str = "Logout"
		url_logged = "/logout"
		if request.method == "PUT":
			try:  # si el recurso YA existe, SE MUESTRA el contenido.
				resource_DB = Resource.objects.get(name=resource)
				rec_name = resource_DB.name
				rec_cont = resource_DB.cont
				template = get_template("I_See_New_People/index.html")
				c = Context({'title': title, 'url_root': url_root, 'logged': logged, 
				'url_logged': url_logged, 'logged_str': logged_str, 'rec_name': rec_name,
				'rec_cont': rec_cont})
				return HttpResponse(template.render(c))					
			except Resource.DoesNotExist:  # Crea el recurso
				try:
					new_resource = Resource(name=resource, cont=request.body)
					new_resource.save()  # add recurso -- force_insert=True
					
					my_rec = Resource.objects.all().last()
					rec_name = "Nuevo recurso: " + my_rec.name + " añadido"
					rec_cont = my_rec.cont
					template = get_template("I_See_New_People/index.html")
					c = Context({'title': title, 'url_root': url_root, 'logged': logged, 
					'url_logged': url_logged, 'logged_str': logged_str, 'rec_name': rec_name,
					'rec_cont': rec_cont})
					return HttpResponse(template.render(c))
								
				except IntegrityError:
					rec_name = "ERROR AL AÑADIR EL RECURSO"
					rec_cont = "Ha habido un problema en la base de datos.\
					Por favor, vuelva a intentarlo."
					template = get_template("I_See_New_People/index.html")
					c = Context({'title': title, 'url_root': url_root, 'logged': logged, 
					'url_logged': url_logged, 'logged_str': logged_str, 'rec_name': rec_name,
					'rec_cont': rec_cont})
					return HttpResponse(template.render(c))
					
	else:
		logged = "Not logged in. "
		url_logged = "/login"
		logged_str = "Login"
		
	if request.method == "GET":
		try:
			resource_DB = Resource.objects.get(name=resource)
			rec_name = resource_DB.name
			rec_cont = resource_DB.cont
		except Resource.DoesNotExist:
			rec_name = "ERROR AL BUSCAR EL RECURSO"
			rec_cont = "ERROR!! - EL RECURSO NO EXISTE. \
			Haz un PUT a 'localhost:8000/annotated/[nombre_recurso]'\
			si deseas añadirlo."
        
		template = get_template("I_See_New_People/index.html")
		c = Context({'title': title, 'url_root': url_root, 'logged': logged, 
		'url_logged': url_logged, 'logged_str': logged_str, 'rec_name': rec_name,
		'rec_cont': rec_cont})
		return HttpResponse(template.render(c))
		
	elif request.method == "PUT":	# No logeado - No puede añadir recursos
		rec_name = "ERROR DE AUTENTICACIÓN"
		rec_cont = "Para ejecutar esta acción necesitas una cuenta. Por favor\
		inicia sesión con usuario y contraseña."
		template = get_template("I_See_New_People/index.html")
		c = Context({'title': title, 'url_root': url_root, 'logged': logged, 
		'url_logged': url_logged, 'logged_str': logged_str, 'rec_name': rec_name,
		'rec_cont': rec_cont})
		return HttpResponse(template.render(c))	

	else:  # Metodo no valido
		rec_name = "ACCIÓN NO VALIDA"
		rec_cont = "Para esta práctica los métodos válidos son PUT y GET"
		template = get_template("I_See_New_People/index.html")
		c = Context({'title': title, 'url_root': url_root, 'logged': logged, 
		'url_logged': url_logged, 'logged_str': logged_str, 'rec_name': rec_name,
		'rec_cont': rec_cont})
		return HttpResponse(template.render(c))
