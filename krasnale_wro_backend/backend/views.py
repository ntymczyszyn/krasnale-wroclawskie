from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def hello_world(request):
    return HttpResponse("Zapraszamy do naszej aplikacji mobilnej!")

@csrf_exempt
def image_upload(request):
    if request.method == 'POST':

        if 'image' not in request.FILES:
            return JsonResponse({'error': 'Nie przesłano pliku'}, status=400)
        
        uploaded_image = request.FILES['image']
        
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
        file_extension = uploaded_image.name.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            return JsonResponse({'error': 'Niewłaściwe rozszerzenie pliku'}, status=400)
        
        allowed_content_types = ['image/jpeg', 'image/png', 'image/gif']
        if uploaded_image.content_type not in allowed_content_types:
            return JsonResponse({'error': 'Niewłaściwy typ zawartości pliku'}, status=400)
        
        return JsonResponse({'success': True, 'message': 'Zdjęcie przesłane pomyślnie'}, status=200)
    else:
        return JsonResponse({'error': 'Metoda nieobsługiwana'}, status=405)