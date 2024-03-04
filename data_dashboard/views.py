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
                SELECT * FROM [dbo].[Animals];
                """
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        df = pd.DataFrame(rows, columns=column_names)
        
        df_count = df.groupby('species').size().reset_index(name='count')
        df_count = df_count.rename(columns={'species': 'Species', 'count': 'Count'})
        df_count = df_count.set_index('Species')
        
        plot = "bar"
        
        context = {
            "plot" : None
        }
        
        #plot with plotly express with a bar chart the number of species per Location
        
        if plot == 'bar':
            
            fig = px.bar(df_count,
                        x=df_count.index,
                        y='Count',
                        title=f'Count of Species by Location')
            
            fig.update_layout(
                    font=dict(size=13, family="Lato"),
                    title_font=dict(size=20),
                    title_y=0.93,
                    plot_bgcolor="#212121",
                    paper_bgcolor="#212121",
                    font_color="white",
                    width=1000,
                    height=470,
                )
            
            fig.update_xaxes(
                    tickangle=35,
                    title_text="Location",
                    tickmode="linear",
                    gridcolor="#424242",
                )

            fig.update_yaxes(
                title_text="Species",
                showgrid=True,
                gridcolor="#424242",
            )
            
            context["plot_map"] = fig.to_html(full_html=False, default_height=800, default_width=1000)
        
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
                plot_bgcolor="#212121",
                paper_bgcolor="#212121",
                font_color="white",
                width=1000,
                height=470,
            )
            
            context["plot_map"] = fig.to_html(full_html=False, default_height=800, default_width=1000)
        
        return render(request, 'index.html', context=context)
    
    
    
    return render(request, 'index.html')

def mongodb(request):
    return render(request, 'mongodb.html')
    