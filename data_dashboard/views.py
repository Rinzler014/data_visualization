from django.shortcuts import render
from django.http import HttpResponse
import pymssql as msql
from plotly import express as px
import pandas as pd
from utils import *

# Create your views here.

cursor = get_connection()

def dashboard(request):
    
    if request.method == 'POST':
        
        query = """
                SELECT * FROM [dbo].[birds];
                """
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        df = pd.DataFrame(rows, columns=column_names)
        
        plot = request.POST['graph']
        
        print(plot)
        
        context = {
            "plot" : None,
            "plot_title" : None
        }
        

        if plot == 'bar':
            
            
            df_avg_altitude = df.groupby('date').size().reset_index(name='Count')
            
            fig = px.bar(df_avg_altitude,
                        x="date",
                        y='Count',
                        title=f'Count of registers by date')
            
            fig.update_layout(
                    font=dict(size=13, family="Lato"),
                    title_font=dict(size=22),
                    title_y=0.93,
                    plot_bgcolor="#fbfaf5",
                    paper_bgcolor="#fbfaf5",
                    font_color="#333",
                    width=1000,
                    height=470,
                )
            
            fig.update_xaxes(
                    tickangle=35,
                    title_text="Fecha",
                    tickmode="linear",
                    gridcolor="#424242",
                )

            fig.update_yaxes(
                title_text="Registros",
                showgrid=True,
                gridcolor="#424242",
            )
            
            context["plot"] = fig.to_html(full_html=False, default_height=800, default_width=1000)
            context["plot_title"] = "Barras"
        
        if plot == 'map':
            
            df_map = df.groupby(['Latitude', 'Longitude', 'species']).size().reset_index(name='count')
            df_map = df_map.rename(columns={'Latitude': 'Latitude', 'Longitude': 'Longitude', 'species': 'Species', 'count': 'Count'})
            fig = px.scatter_mapbox(df_map, lat="Latitude", lon="Longitude", color="Species", size="Count", zoom=3, height=470)
            fig.update_layout(
                mapbox_style="open-street-map",
                margin={"r":0,"t":0,"l":0,"b":0},
                font=dict(size=13, family="Lato"),
                title_font=dict(size=20),
                title_y=0.93,
                    plot_bgcolor="#fbfaf5",
                    paper_bgcolor="#fbfaf5",
                    font_color="#333",
                width=1000,
                height=470,
            )
            
            context["plot"] = fig.to_html(full_html=False, default_height=800, default_width=1000)
            context["plot_title"] = "Mapa"
        
        if plot == 'pie':
            
            fig = px.pie(df_count, values='Count', names=df_count.index, title='Count of Species by Location')
            fig.update_layout(
                font=dict(size=13, family="Lato"),
                title_font=dict(size=20),
                title_y=0.93,
                    plot_bgcolor="#fbfaf5",
                    paper_bgcolor="#fbfaf5",
                    font_color="#333",
                width=1000,
                height=470,
            )
            
            context["plot"] = fig.to_html(full_html=False, default_height=800, default_width=1000)
            context["plot_title"] = "Pie"
      
        if plot == 'line':
            
            #Group the data by the averge age of each location
            df_line = df.groupby('Location')['species'].mean().reset_index()
            df_line = df_line.rename(columns={'Location': 'Lugar', 'species': 'Especies'})
            fig = px.bar(df_line, x='Lugar', y='Edad Promedio', color='Edad Promedio', title='Edad Promedio por Ubicacion')
            fig.update_layout(
                font=dict(size=13, family="Lato"),
                title_font=dict(size=20),
                title_y=0.93,
                    plot_bgcolor="#fbfaf5",
                    paper_bgcolor="#fbfaf5",
                    font_color="#333",
                width=1000,
                height=470,
            )
            
            fig.update_xaxes(
                tickangle=35,
                gridcolor="#424242",
            )
            
            fig.update_yaxes(showgrid=True, 
                             gridcolor="#424242")
            
            context["plot"] = fig.to_html(full_html=False, default_height=800, default_width=1000)
            context["plot_title"] = "Line"    
        
        if plot == 'bubble' :
            
            df_bubble = df.groupby(['species', 'date']).size().reset_index(name='count')
            df_bubble = df_bubble.rename(columns={'species': 'Species', 'date': 'Date', 'count': 'Count'})
            fig = px.scatter(df_bubble, x='Date', y='Count', size='Count', color='Species', title='Count of Species by Location')
            fig.update_layout(
                font=dict(size=13, family="Lato"),
                title_font=dict(size=20),
                title_y=0.93,
                    plot_bgcolor="#fbfaf5",
                    paper_bgcolor="#fbfaf5",
                    font_color="#333",
                width=1000,
                height=470,
            )
            
            context["plot"] = fig.to_html(full_html=False, default_height=800, default_width=1000)
            context["plot_title"] = "Bubble"
        
        if plot == 'dispersion':
            
            df_dispersion = df.groupby(['species', 'date']).size().reset_index(name='count')
            df_dispersion = df_dispersion.rename(columns={'species': 'Species', 'date': 'Date', 'count': 'Count'})
            fig = px.scatter(df_dispersion, x='Date', y='Count', color='Species', title='Count of Species by Location')
            fig.update_layout(
                font=dict(size=13, family="Lato"),
                title_font=dict(size=20),
                title_y=0.93,
                    plot_bgcolor="#fbfaf5",
                    paper_bgcolor="#fbfaf5",
                    font_color="#333",
                width=1000,
                height=470,
            )
            
            context["plot"] = fig.to_html(full_html=False, default_height=800, default_width=1000)
            context["plot_title"] = "Dispersion"
        
        return render(request, 'index.html', context=context)
    
    return render(request, 'index.html')

def mongodb(request):
    return render(request, 'mongodb.html')
    