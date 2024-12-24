from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def dashboard_view(request):
    try:
        # Load the data
        df = pd.read_csv('data/Electric_Vehicle_Population_Data.csv')

        # Check if required columns exist
        if 'Electric Vehicle Type' not in df.columns or 'County' not in df.columns:
            return HttpResponse("The required columns are missing.")

        # Generate Pie Chart for Electric Vehicle Type Distribution
        fig1, ax1 = plt.subplots(figsize=(6, 6))
        df['Electric Vehicle Type'].value_counts().plot(
            kind='pie', 
            autopct='%1.1f%%', 
            ax=ax1,
            fontsize=12
        )
        plt.title("Electric Vehicle Type Distribution")
        plt.ylabel('')  # Hide Y-axis label
        plt.xlabel('')  # Hide X-axis label
        plt.tight_layout()

        # Convert Pie Chart to Base64
        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='png')
        buffer1.seek(0)
        pie_chart_png = buffer1.getvalue()
        buffer1.close()
        plt.close(fig1)  # Close Pie Chart

        # Generate Bar Chart for Electric Vehicle Type Counts
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        df['Electric Vehicle Type'].value_counts().plot(kind='bar', ax=ax2)
        plt.title('Count of Electric Vehicle Types')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Convert Bar Chart to Base64
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)
        bar_chart_png = buffer2.getvalue()
        buffer2.close()
        plt.close(fig2)  # Close Bar Chart

        # Group by County and Count Electric Vehicles
        county_counts = df.groupby('County').size().reset_index(name='Electric Vehicle Count')

        # Sort Counties by Count in Descending Order
        county_counts = county_counts.sort_values(by='Electric Vehicle Count', ascending=False)
        county_counts = county_counts.head(10)

        # Plot Distribution of Electric Vehicles by County
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.bar(county_counts['County'], county_counts['Electric Vehicle Count'], color='skyblue')
        ax3.set_xlabel('County')
        ax3.set_ylabel('Electric Vehicle Count')
        ax3.set_title('Distribution of Electric Vehicles by County')
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Convert County Bar Chart to Base64
        buffer3 = io.BytesIO()
        plt.savefig(buffer3, format='png')
        buffer3.seek(0)
        county_chart_png = buffer3.getvalue()
        buffer3.close()
        plt.close(fig3)  # Close County Bar Chart

        # Convert images to Base64
        pie_chart = base64.b64encode(pie_chart_png).decode('utf-8')
        bar_chart = base64.b64encode(bar_chart_png).decode('utf-8')
        county_chart = base64.b64encode(county_chart_png).decode('utf-8')

        # Send charts to the template
        return render(request, 'dash1.html', {
            'pie_chart': pie_chart,
            'bar_chart': bar_chart,
            'county_chart': county_chart
        })
    except FileNotFoundError:
        return HttpResponse("Data file not found.")
    except pd.errors.EmptyDataError:
        return HttpResponse("Data file is empty.")
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {str(e)}")

