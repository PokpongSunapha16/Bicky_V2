from django.shortcuts import render, redirect

from . models import dash
from . forms import elec

'''def dashboard_view(request):
    """
    View สำหรับ Dashboard
    """
    return render(request, 'dashboard.html')
    
def dashboard_view(request):
    Elec = dash.objects.all()

    if request.method == 'POST':
        form = elec(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = elec()        

    context = {
        "products": Elec,
        "form": form
    }

    return render(request, 'index.html', context)'''
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib
import base64

def dashboard_view(request):
    # โหลดข้อมูล
    df = pd.read_csv('data/Electric_Vehicle_Population_Data.csv')

    # สร้างกราฟ
    fig, ax = plt.subplots(figsize=(6, 6))
    df['Electric Vehicle Type'].value_counts().plot(
        kind='pie', 
        autopct='%1.1f%%', 
        ax=ax,
        fontsize=12
    )
    plt.title("Electric Vehicle Type Distribution")
    plt.ylabel('')  # ซ่อน Y-axis label
    plt.xlabel('')  # ซ่อน X-axis label
    plt.tight_layout()

    # แปลงกราฟเป็นรูปภาพ
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # แปลงภาพเป็น base64
    graph = base64.b64encode(image_png).decode('utf-8')

    # ส่งกราฟไปยัง template
    return render(request, 'dash1.html', {'graph': graph})
