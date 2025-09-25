"""
Unit tests for the map feature using Streamlit's AppTest class.
These tests should fail until the map feature is implemented.
"""

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMapFeature:
    """Test class for map feature functionality."""
    
    @pytest.fixture
    def app_test(self):
        """Create an AppTest instance for testing."""
        # Go up from tests/unit/ to app/ directory
        app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "app.py")
        return AppTest.from_file(app_path)
    
    def test_app_loads_successfully(self, app_test):
        """Test that the Streamlit app loads without errors."""
        app_test.run()
        assert not app_test.exception, f"App should load without errors, but got: {app_test.exception}"
    
    def test_map_component_exists_in_source(self, app_test):
        """Test that map components exist in the app source code."""
        app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "app.py")
        
        with open(app_path, 'r') as f:
            app_source = f.read()
        
        # Look for map-related components that should exist
        map_components = [
            'st.map',
            'st.pydeck_chart',
            'st.plotly_chart',
            'folium',
            'leaflet'
        ]
        
        map_found = any(component in app_source for component in map_components)
        assert map_found, f"Map components should be present in source code. Expected: {map_components}"
    
    
    def test_map_displays_logistics_data(self, app_test):
        """Test that the map displays logistics-related data."""
        app_test.run()
        
        # Check if any logistics-related content is present
        logistics_keywords = [
            'logistics',
            'supply',
            'transport',
            'warehouse',
            'distribution',
            'cargo',
            'freight'
        ]
        
        logistics_content_found = False
        
        if hasattr(app_test, 'main') and app_test.main:
            for element in app_test.main:
                if hasattr(element, 'value'):
                    element_text = str(element.value).lower()
                    if any(keyword in element_text for keyword in logistics_keywords):
                        logistics_content_found = True
                        break
        
        assert logistics_content_found, f"Map should display logistics data. Expected keywords: {logistics_keywords}"
    
    def test_map_performance(self, app_test):
        """Test that the map loads and renders within acceptable time limits."""
        import time
        
        start_time = time.time()
        app_test.run()
        end_time = time.time()
        
        load_time = end_time - start_time
        
        # Map should load within 5 seconds
        assert load_time < 5.0, f"Map should load within 5 seconds, but took {load_time:.2f} seconds"
