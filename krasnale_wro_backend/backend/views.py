from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
import os
import tempfile

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

            with tempfile.NamedTemporaryFile(delete=False, suffix='.' + file_extension) as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            predicted_classes = processImage(temp_file_path)
            os.unlink(temp_file_path)

            print({'message': predicted_classes})
            return JsonResponse({'message': predicted_classes}, status=200)
        
        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


def processImage(image):
    path =  os.path.join(os.path.dirname(__file__), "krasnaleModel_v1.pt")
    model = YOLO(path)
    
    result = model(source=image, show=False, conf=0.3, save=True)
    predicted_classes = []

    for i, r in enumerate(result):
        predicted_classes.extend([model.names[int(cls)] for cls in r.boxes.cls])

    return predicted_classes
