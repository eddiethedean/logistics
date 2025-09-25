import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.set_page_config(
        page_title="Logistics COP",
        page_icon="🚛",
        layout="wide"
    )
    
    # Main header with system purpose
    st.title("🚛 Logistics Common Operating Picture")
    st.markdown("---")
    
    st.header("System Purpose")
    st.markdown("""
    Create an easily accessible, tactical logistics common operating picture
    for SOF decision makers and tactical planners to enable better warfighter readiness.
    """)
    
    st.markdown("---")
    
    # Welcome message
    st.subheader("Welcome to the Logistics COP")
    st.write("This application provides tactical logistics information for decision makers and planners.")
    
    st.markdown("---")
    
    # Map section
    st.header("📍 Logistics Map")
    st.write("View tactical logistics information on the interactive map below.")
    
    # Create sample logistics data
    logistics_data = pd.DataFrame({
        'lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],  # Sample coordinates
        'lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
        'location': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
        'supply_type': ['Ammunition', 'Fuel', 'Medical', 'Food', 'Equipment'],
        'status': ['Available', 'Low Stock', 'Available', 'Critical', 'Available'],
        'priority': ['High', 'Medium', 'High', 'Critical', 'Low']
    })
    
    # Display the map
    st.map(
        logistics_data,
        latitude='lat',
        longitude='lon',
        size=20,
        color='#FF6B6B'
    )
    
    # Display logistics data table
    st.subheader("Logistics Data")
    st.dataframe(logistics_data, use_container_width=True)
    
    # Add some logistics-specific information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Locations", len(logistics_data))
    
    with col2:
        available_count = len(logistics_data[logistics_data['status'] == 'Available'])
        st.metric("Available Supplies", available_count)
    
    with col3:
        critical_count = len(logistics_data[logistics_data['status'] == 'Critical'])
        st.metric("Critical Alerts", critical_count, delta=f"-{critical_count}" if critical_count > 0 else "0")

if __name__ == "__main__":
        main()
