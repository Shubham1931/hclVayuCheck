import plotly.express as px
import plotly.graph_objects as go

def create_historical_chart(data):
    """Create historical AQI chart"""
    fig = px.line(
        data,
        x='date',
        y='aqi',
        title='Historical AQI Trends'
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family='Roboto',
        title_font_family='Roboto',
        title_font_size=20,
        xaxis_title="Date",
        yaxis_title="AQI",
        height=400
    )
    
    fig.update_traces(line_color='#4CAF50')
    
    return fig

def create_gauge_chart(aqi_value):
    """Create AQI gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 300]},
            'bar': {'color': "#4CAF50"},
            'steps': [
                {'range': [0, 50], 'color': "#4CAF50"},
                {'range': [51, 100], 'color': "#FFC107"},
                {'range': [101, 150], 'color': "#FF9800"},
                {'range': [151, 200], 'color': "#FF5722"},
                {'range': [201, 300], 'color': "#9C27B0"}
            ]
        }
    ))
    
    fig.update_layout(
        font_family='Roboto',
        height=300,
        margin=dict(l=30, r=30, t=30, b=30)
    )
    
    return fig
