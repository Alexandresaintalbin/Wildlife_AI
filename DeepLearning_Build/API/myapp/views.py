from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .predictor import predict_species

@api_view(['GET'])
def predict(request):
    image_url = request.GET.get('image_url', None)
    image_id = request.GET.get('image_id', None)

    if image_url and image_id:
        espece_fr, espece_en = predict_species(image_url)
        return Response({
            "espece_fr": espece_fr,
            "espece_en": espece_en,
            "image_id": image_id,
            "success": True
        })
    else:
        return Response({
            "success": False,
            "message": "image_url and image_id are required."
        })
