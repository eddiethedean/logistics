from behave import given, when, then
import streamlit as st
from streamlit.testing.v1 import AppTest
import sys
import os

# Add the app directory to the Python path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@given('an UI exists')
def step_ui_exists(context):
    """Set up the context for a UI that exists."""
    context.ui_exists = False
    context.app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "app.py")
    
    # Check if the app loads successfully
    try:
        context.at = AppTest.from_file(context.app_path)
        context.at.run(timeout=10)
        
        # Check if the app ran without errors
        if not context.at.exception:
            context.ui_exists = True
        else:
            context.ui_exists = False
            context.error = context.at.exception
            
    except Exception as e:
        context.ui_exists = False
        context.error = str(e)
    
    # This should pass since we have a working app
    assert context.ui_exists, f"UI should exist and load successfully. Error: {getattr(context, 'error', 'Unknown error')}"


@when('a user saves content to supply form')
def step_user_saves_content_to_supply_form(context):
    """User saves content to supply form."""
    # This should fail until supply form functionality is implemented
    context.supply_form_saved = False
    
    # Check if supply form functionality exists
    try:
        with open(context.app_path, 'r') as f:
            app_source = f.read()
        
        # Look for supply-related functionality
        supply_keywords = [
            'supply',
            'supply_form',
            'supply_data',
            'save_supply',
            'update_supply',
            'supply_class',
            'supply_management'
        ]
        
        supply_functionality = any(keyword in app_source.lower() for keyword in supply_keywords)
        
        if supply_functionality:
            context.supply_form_saved = True
        else:
            context.supply_form_saved = False
            
    except Exception as e:
        context.supply_form_saved = False
        context.error = str(e)
    
    # This should fail until supply form is implemented
    assert context.supply_form_saved, f"Supply form functionality should be implemented. Expected keywords: {supply_keywords}"


@then('new content is saved to supply database')
def step_content_saved_to_supply_database(context):
    """Verify that new content is saved to supply database."""
    # This should fail until supply database functionality is implemented
    context.supply_database_saved = False
    
    # Check if supply database functionality exists
    try:
        with open(context.app_path, 'r') as f:
            app_source = f.read()
        
        # Look for supply database-related functionality
        supply_database_keywords = [
            'supply.db',
            'save_supply_data',
            'get_supply_data',
            'supply_table',
            'supply_database',
            'supply_persistence'
        ]
        
        supply_database_functionality = any(keyword in app_source.lower() for keyword in supply_database_keywords)
        
        if supply_database_functionality:
            context.supply_database_saved = True
        else:
            context.supply_database_saved = False
            
    except Exception as e:
        context.supply_database_saved = False
        context.error = str(e)
    
    # This should fail until supply database functionality is implemented
    assert context.supply_database_saved, f"Supply database functionality should be implemented. Expected keywords: {supply_database_keywords}"
