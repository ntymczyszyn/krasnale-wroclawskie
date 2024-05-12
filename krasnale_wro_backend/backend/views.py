from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def hello_world(request):
    return HttpResponse("Welcome to our mobile application!")

@csrf_exempt
def image_upload(request):
    if request.method == 'POST':
        try:
            if 'file' not in request.FILES:
                return JsonResponse({'message': 'File not uploaded'}, status=400)

            uploaded_file = request.FILES['file']

            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                return JsonResponse({'message': 'Invalid file extension'}, status=400)
            
            allowed_content_types = ['image/jpeg', 'image/png', 'image/gif']
            if uploaded_file.content_type not in allowed_content_types:
                return JsonResponse({'message': 'Invalid file content type'}, status=400)
            
            print({'message': 'Image uploaded successfully'})
            return JsonResponse({'message': 'Image uploaded successfully!'}, status=200)
        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
