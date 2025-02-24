import plotly.express as px

def create_historical_chart(data):
    """Create enhanced historical AQI chart"""
    fig = px.line(
        data,
        x='date',
        y='aqi',
        title='Historical AQI Trends'
    )
    
    fig.update_layout(
        plot_bgcolor='rgb(248, 248, 248)',  # Light gray background
        paper_bgcolor='white',
        font_family='Arial, sans-serif',
        title_font_family='Arial, sans-serif',
        title_font_size=24,
        title_font_color='rgb(34, 34, 34)',  # Dark gray title
        xaxis_title="Date",
        yaxis_title="AQI",
        height=500,
        width=800,
        xaxis=dict(
            showgrid=True,  # Show grid lines for X axis
            gridwidth=0.5,
            gridcolor='rgba(200, 200, 200, 0.5)',  # Light gray gridlines
            ticks='outside',  # Ticks outside for better visibility
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(200, 200, 200, 0.5)',  # Light gray gridlines
            ticks='outside',
        )
    )
    
    # Markers to highlight data points
    fig.update_traces(line_color='#4CAF50', mode='lines+markers', marker=dict(size=8, color='#4CAF50'))
    
    # Add hover effects
    fig.update_traces(
        hovertemplate="Date: %{x}<br>AQI: %{y}<extra></extra>",
        hoverlabel=dict(bgcolor='rgba(0, 0, 0, 0.8)', font_size=12, font_family="Arial", font_color='white')
    )
    
    return fig
import plotly.graph_objects as go

def create_gauge_chart(aqi_value):
    """Create AQI gauge chart with enhanced color scheme."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'shape': "angular",  # Angular for circular appearance
            'axis': {
                'range': [0, 500],  # Adjust to the full AQI scale
                'tickwidth': 2,
                'tickcolor': "black"
            },
            'bar': {'color': "#66bb6a"},  # Bar color to reflect the actual value
            'steps': [
                {'range': [0, 50], 'color': "#66bb6a"},  # Good: Green
                {'range': [51, 100], 'color': "#ffeb3b"},  # Moderate: Yellow
                {'range': [101, 150], 'color': "#ffa726"},  # Unhealthy for Sensitive Groups: Orange
                {'range': [151, 200], 'color': "#f44336"},  # Unhealthy: Red
                {'range': [201, 300], 'color': "#9c27b0"},  # Very Unhealthy: Purple
                {'range': [301, 500], 'color': "#d32f2f"}  # Hazardous: Dark Red
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},  # Line to show current AQI value
                'thickness': 0.75,
                'value': aqi_value
            }
        }
    ))

    fig.update_layout(
        title="Air Quality Index (AQI)",
        font_family="Roboto",
        font_size=16,
        height=400,
        margin=dict(l=30, r=30, t=50, b=30)
    )

    return fig
