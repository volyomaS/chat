from django.shortcuts import render


def room(request):
    """
    Chat room rendering
    """
    return render(request, 'chat/room.html')
