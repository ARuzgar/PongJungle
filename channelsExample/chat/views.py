from django.shortcuts import render, redirect
from django.views import View

class ChatPageView(View):
    template_name = "ChatPage.html"
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login-user")
        context = {}
        return render(request, self.template_name, context)
