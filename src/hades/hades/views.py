import os

from django.http import HttpResponse, JsonResponse, FileResponse
from django.template.response import TemplateResponse 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from . import settings
from . import models

# default settings
background_color = "ffffff"
animation_in     = "fadeInDown"
timespan_in      = "1000"
timespan_out     = "1000"
animation_out    = "fadeOutDown"

@require_http_methods(['GET','POST'])
def page_login(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			if request.GET.get('next') is not None:
				return redirect(request.GET.get('next'))
			return redirect('/pages')

		return TemplateResponse(request,'login.html')

	user = authenticate(
		username=request.POST['username'],
		password=request.POST['password'])

	if user is None:
		return TemplateResponse(request,'login.html')
	
	login(request,user)

	if request.GET.get('next') is not None:
		return redirect(request.GET.get('next'))
	return redirect('/pages')

@require_http_methods(['GET'])
@login_required(login_url='/login')
def page_logout(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('/')

@require_http_methods(['GET'])
def page_index(request):
	return TemplateResponse(request,'index.html')

@require_http_methods(['POST'])
def page_next(request):

	if len(models.Page.objects.all()) == 0:
		data = {}
		data['status'] = 'failed'
		return JsonResponse(data)

	pages = models.Page.objects.all().order_by('order')

	if 'index' in request.session:
		index = int(request.session['index'])
		index = index + 1
	else:
		index = 0

	request.session['index'] = index
	index = index % len(pages)
	page = pages[index]

	data = {}
	if page is None:
		data['status'] = 'failed'
	else:
		data['status'] = 'success'
		data['uuid'] = page.uuid
		data['span'] = page.span
		data['background_color'] = '#' + background_color
		data['animation_in']     = 'animated ' + animation_in
		data['timespan_in']      = timespan_in
		data['animation_out']    = 'animated ' + animation_out
		data['timespan_out']     = timespan_out
	return JsonResponse(data)

@require_http_methods(['GET'])
def page_image(request,uuid):
	path = os.path.join(settings.IMAGES_PATH, uuid+".jpg")
	if not os.path.isfile(path):
		return FileResponse(open(settings.DEFAULT_IMAGE_PATH,'rb'),content_type='image/jpeg')
	return FileResponse(open(path,'rb'),content_type='image/jpeg')

@require_http_methods(['GET','POST'])
@login_required(login_url='/login')
def page_pages(request):
	if request.method == 'POST':
		page = models.Page.objects.filter(uuid=request.POST['uuid']).first()
		if page is not None:
			if 'order' in request.POST:
				if len(request.POST['order']) > 0:
					page.order = request.POST['order']
			if 'span' in request.POST:
				if len(request.POST['span']) > 0:
					page.span  = request.POST['span']
			page.save()
			if len(request.FILES.getlist('file')) != 0:
				path = os.path.join(settings.IMAGES_PATH,str(page.uuid)+'.jpg')
				if os.path.isfile(path):
					os.remove(path)
				with open(path,'wb+') as file:
					for chunk in request.FILES.getlist('file')[0].chunks():
						file.write(chunk)

	pages = models.Page.objects.all().order_by('order')
	return TemplateResponse(request,'pages.html',{
		'pages':pages,
		'background_color':background_color,
		'animation_in':animation_in,
		'timespan_in':timespan_in,
		'animation_out':animation_out,
		'timespan_out':timespan_out,
		})

@require_http_methods(['POST'])
@login_required(login_url='/login')
def page_pages_new(request):
	if len(request.FILES.getlist('files')) == 0:
		page = models.Page()
		page.order = request.POST['order']
		page.span  = request.POST['span']
		page.save()
	else:
		for item in request.FILES.getlist('files'):
			page = models.Page()
			page.order = request.POST['order']
			page.span  = request.POST['span']
			page.save()

			# save image
			path = os.path.join(settings.IMAGES_PATH,str(page.uuid)+'.jpg')
			if os.path.isfile(path):
				os.remove(path)
			with open(path,'wb+') as file:
				for chunk in item.chunks():
					file.write(chunk)

	return redirect('/pages')

@require_http_methods(['GET'])
@login_required(login_url='/login')
def page_page_delete(request,uuid):
	page = models.Page.objects.filter(uuid=uuid).first()
	if page is not None:
		page.delete()
		path = os.path.join(settings.IMAGES_PATH,str(page.uuid)+'.jpg')
		if os.path.isfile(path):
			os.remove(path)
	return redirect('/pages')

@require_http_methods(['POST'])
@login_required(login_url='/login')
def	page_pages_config(request):
	global background_color
	global animation_in
	global timespan_in
	global animation_out
	global timespan_out

	if 'background_color' in request.POST:
		background_color = request.POST['background_color'].lower()

	if 'animation_in' in request.POST:
		animation_in = request.POST['animation_in']

	if 'timespan_in' in request.POST:
		timespan_in = request.POST['timespan_in']

	if 'animation_out' in request.POST:
		animation_out = request.POST['animation_out']

	if 'timespan_out' in request.POST:
		timespan_out = request.POST['timespan_out']

	print(request.POST)

	return redirect('/pages')