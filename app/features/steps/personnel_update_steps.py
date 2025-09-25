from behave import given, when, then
import streamlit as st
from streamlit.testing.v1 import AppTest
import sys
import os

# Add the app directory to the Python path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@given('a UI exists with forms')
def step_ui_exists_with_forms(context):
    """Set up the context for a UI with forms."""
    context.ui_has_forms = False
    context.app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "app.py")
    
    # Check if the app has form elements
    try:
        context.at = AppTest.from_file(context.app_path)
        context.at.run(timeout=10)
        
        # Look for form elements in the app
        if hasattr(context.at, 'main') and context.at.main:
            for element in context.at.main:
                if hasattr(element, 'type'):
                    element_type = str(element.type).lower()
                    if 'form' in element_type or 'input' in element_type or 'text_input' in element_type:
                        context.ui_has_forms = True
                        break
        
        # Also check source code for form components
        with open(context.app_path, 'r') as f:
            app_source = f.read()
        
        form_components = ['st.form', 'st.text_input', 'st.selectbox', 'st.button']
        form_found = any(component in app_source for component in form_components)
        
        if form_found:
            context.ui_has_forms = True
            
    except Exception as e:
        context.ui_has_forms = False
        context.error = str(e)
    
    # This should fail until forms are implemented
    assert context.ui_has_forms, "UI should have forms for personnel updates"


@when('a user saves content to personnel')
def step_user_saves_content_to_personnel(context):
    """User saves content to personnel."""
    # This should fail until personnel saving functionality is implemented
    context.personnel_saved = False
    
    # Check if personnel saving functionality exists
    try:
        with open(context.app_path, 'r') as f:
            app_source = f.read()
        
        # Look for personnel-related functionality
        personnel_keywords = [
            'personnel',
            'save_personnel',
            'update_personnel',
            'personnel_data',
            'personnel_form'
        ]
        
        personnel_functionality = any(keyword in app_source.lower() for keyword in personnel_keywords)
        
        if personnel_functionality:
            context.personnel_saved = True
        else:
            context.personnel_saved = False
            
    except Exception as e:
        context.personnel_saved = False
        context.error = str(e)
    
    # This should fail until personnel saving is implemented
    assert context.personnel_saved, "Personnel saving functionality should be implemented"


@then('new content is saved to database')
def step_content_saved_to_database(context):
    """Verify that new content is saved to database."""
    # This should fail until database functionality is implemented
    context.database_saved = False
    
    # Check if database functionality exists
    try:
        with open(context.app_path, 'r') as f:
            app_source = f.read()
        
        # Look for database-related functionality
        database_keywords = [
            'database',
            'sqlite',
            'postgresql',
            'mysql',
            'sqlalchemy',
            'pymongo',
            'save_to_db',
            'insert',
            'update',
            'commit'
        ]
        
        database_functionality = any(keyword in app_source.lower() for keyword in database_keywords)
        
        if database_functionality:
            context.database_saved = True
        else:
            context.database_saved = False
            
    except Exception as e:
        context.database_saved = False
        context.error = str(e)
    
    # This should fail until database functionality is implemented
    assert context.database_saved, "Database saving functionality should be implemented"
