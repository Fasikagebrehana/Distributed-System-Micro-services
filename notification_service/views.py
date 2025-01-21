from django.http import JsonResponse

def send_notification(request):
    if request.method == 'POST':
        # Logic to send a notification
        return JsonResponse({"message": "Notification sent successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=400)
from django.shortcuts import render

# Create your views here.
