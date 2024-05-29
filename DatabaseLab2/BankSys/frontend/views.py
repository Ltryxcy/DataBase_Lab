from django.shortcuts import render

# Create your views here.
def index(request):
    # 返回主页
    return render(request, 'frontend/index.html')