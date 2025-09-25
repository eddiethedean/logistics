from behave import given, when, then
import streamlit as st
from streamlit.testing.v1 import AppTest
import sys
import os

# Add the app directory to the Python path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@given('a viewer wants to see the LogCOP')
def step_viewer_wants_to_see_logcop(context):
    """Set up the context for a viewer wanting to see the LogCOP."""
    context.viewer = "viewer"
    # Set up the app path for testing - go up two levels from features/steps to get to app directory
    context.app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "app.py")


@when('a user accesses the application')
def step_user_accesses_application(context):
    """User accesses the application."""
    # Use Streamlit's built-in testing framework
    context.at = AppTest.from_file(context.app_path)
    context.at.run(timeout=10)  # Increase timeout for map rendering
    
    # Check if the app ran successfully
    assert not context.at.exception, f"Application failed to run: {context.at.exception}"


@then('they see a map')
def step_they_see_a_map(context):
    """Verify that the user sees a map."""
    # This test should fail because the map feature is not implemented yet
    # We're checking for actual map elements that don't exist in the current app
    
    # Check if the app ran successfully
    assert context.at is not None, "Application should have been initialized"
    assert not context.at.exception, "Application should run without exceptions"
    
    # Check if there are any map-related components in the Streamlit app
    # Look for map components that should exist but don't yet
    map_components = [
        'st.map',
        'st.pydeck_chart', 
        'st.plotly_chart',
        'folium',
        'leaflet'
    ]
    
    # Get the app's source code to inspect what components are used
    with open(context.app_path, 'r') as f:
        app_source = f.read()
    
    # Look for map-related function calls in the source code
    map_found = any(component in app_source for component in map_components)
    
    # Also check if there are any map-related elements in the rendered app
    # This is more comprehensive than just checking source code
    app_has_map = False
    
    # Check if the app has any map-related elements
    if hasattr(context.at, 'main') and context.at.main:
        # Look for map elements in the app's main area
        for element in context.at.main:
            if hasattr(element, 'type') and 'map' in str(element.type).lower():
                app_has_map = True
                break
    
    # This assertion should fail until the map is actually implemented
    assert map_found or app_has_map, f"Map should be present in the application. Expected to find map components: {map_components}"
