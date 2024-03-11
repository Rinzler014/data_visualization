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
        
        plot = request.POST['graph']
        
        print(plot)
        
        context = {
            "plot" : None,
            "plot_title" : None
        }
        

        if plot == 'bar':
            
            df_family = df.groupby('family').size().reset_index(name='Count')
            
            fig = px.bar(df_family,
                        x="family",
                        y='Count',
                        title=f'Conteo de registros por familia')
            
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
                    tickangle=90,
                    title_text="Familia",
                    tickmode="linear",
                    gridcolor="#9A9A9A",
                    showgrid=False,
                )

            fig.update_yaxes(
                title_text="Registros",
                showgrid=True,
                gridcolor="#9A9A9A",
            )
            
            context["plot"] = fig.to_html(full_html=False, default_height=800, default_width=1000)
            context["plot_title"] = "Barras"
        
        if plot == 'pie':
            
            df_count = df.groupby('conservation_status').size().reset_index(name='count')
            
            fig = px.pie(df_count, values=df_count.index, names='conservation_status', title='Recuento de Conservaciones')
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
      
        if plot == 'bubble' :
            
            df_bubble = df.groupby('family').size().reset_index(name='count')
            
            fig = px.scatter(df_bubble, x='family', y='count', color='family', size='count', title='Recuento de Animales')
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
        
        if plot == 'histogram':
            
            fig = px.histogram(df, x='countries', title='Countries Histogram')
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
            context["plot_title"] = "Histograma"
        
        return render(request, 'index.html', context=context)
    
    return render(request, 'index.html')
    