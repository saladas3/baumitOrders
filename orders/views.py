from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def chat_view(request):
    """
    Display the chat page for the order manager.
    
    This view renders the chat interface where users can communicate with each other
    in real-time within the order management system.
    
    Args:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        HttpResponse: Rendered chat template with context data.
    """
    return render(request, 'orders/chat.html')
