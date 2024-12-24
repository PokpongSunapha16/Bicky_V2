from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def dashboard_view(request):
    try:
        # โหลดข้อมูล
        df = pd.read_csv('data/Electric_Vehicle_Population_Data.csv')

        # ตรวจสอบว่ามีคอลัมน์ 'Electric Vehicle Type' หรือไม่
        if 'Electric Vehicle Type' not in df.columns:
            return HttpResponse("The required column 'Electric Vehicle Type' is missing.")

        # สร้างกราฟ Pie Chart
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        df['Electric Vehicle Type'].value_counts().plot(
            kind='pie', 
            autopct='%1.1f%%', 
            ax=ax1,
            fontsize=12
        )
        plt.title("Electric Vehicle Type Distribution")
        plt.ylabel('')  # ซ่อน Y-axis label
        plt.xlabel('')  # ซ่อน X-axis label
        plt.tight_layout()

        # แปลง Pie Chart เป็น Base64
        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='png')
        buffer1.seek(0)
        pie_chart_png = buffer1.getvalue()
        buffer1.close()
        plt.close(fig1)  # ปิด Pie Chart

        # สร้างกราฟ Bar Chart
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        df['Electric Vehicle Type'].value_counts().plot(kind='bar', ax=ax2)
        plt.title('Count of Electric Vehicle Types')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # แปลง Bar Chart เป็น Base64
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)
        bar_chart_png = buffer2.getvalue()
        buffer2.close()
        plt.close(fig2)  # ปิด Bar Chart

        # แปลงภาพเป็น Base64
        pie_chart = base64.b64encode(pie_chart_png).decode('utf-8')
        bar_chart = base64.b64encode(bar_chart_png).decode('utf-8')

        # ส่งกราฟไปยัง template
        return render(request, 'dash1.html', {
            'pie_chart': pie_chart,
            'bar_chart': bar_chart
        })
    except FileNotFoundError:
        return HttpResponse("Data file not found.")
    except pd.errors.EmptyDataError:
        return HttpResponse("Data file is empty.")
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {str(e)}")
