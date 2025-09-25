import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime

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
    
    st.markdown("---")
    
    # Personnel Update Section
    st.header("👥 Personnel Management")
    st.write("Update personnel class information and manage personnel records.")
    
    # Initialize database
    init_database()
    
    # Personnel form
    with st.form("personnel_form"):
        st.subheader("Update Personnel Class")
        
        col1, col2 = st.columns(2)
        
        with col1:
            personnel_id = st.text_input("Personnel ID", placeholder="Enter personnel ID", help="Required field")
            first_name = st.text_input("First Name", placeholder="Enter first name", help="Required field")
            last_name = st.text_input("Last Name", placeholder="Enter last name", help="Required field")
            personnel_class = st.selectbox("Personnel Class", 
                                         ["Officer", "Enlisted", "Civilian", "Contractor"], 
                                         help="Select personnel class")
        
        with col2:
            rank = st.text_input("Rank", placeholder="Enter rank")
            unit = st.text_input("Unit", placeholder="Enter unit assignment")
            clearance_level = st.selectbox("Clearance Level", 
                                         ["Unclassified", "Confidential", "Secret", "Top Secret"], 
                                         help="Select clearance level")
            status = st.selectbox("Status", 
                                ["Active", "Inactive", "Reserve", "Retired"], 
                                help="Select personnel status")
        
        # Additional information
        notes = st.text_area("Notes", placeholder="Enter additional notes or comments")
        
        # Form validation
        validation_errors = []
        
        # Required field validation
        if not personnel_id:
            validation_errors.append("Personnel ID is required")
        if not first_name:
            validation_errors.append("First Name is required")
        if not last_name:
            validation_errors.append("Last Name is required")
        
        # Display validation errors
        if validation_errors:
            for error in validation_errors:
                st.error(f"⚠️ {error}")
        
        # Submit button
        submitted = st.form_submit_button("Save Personnel Data", type="primary")
        
        if submitted:
            if not validation_errors:
                # Save to database
                success = save_personnel_data({
                    'personnel_id': personnel_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'personnel_class': personnel_class,
                    'rank': rank,
                    'unit': unit,
                    'clearance_level': clearance_level,
                    'status': status,
                    'notes': notes,
                    'updated_at': datetime.now().isoformat()
                })
                
                if success:
                    st.success("✅ Personnel data saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save personnel data. Please try again.")
            else:
                st.warning("Please fix the validation errors before submitting.")
    
    # Display existing personnel data
    st.subheader("Current Personnel Records")
    personnel_data = get_personnel_data()
    
    if not personnel_data.empty:
        st.dataframe(personnel_data, use_container_width=True)
    else:
        st.info("No personnel records found. Add some personnel data using the form above.")
    
    st.markdown("---")
    
    # Supply Management Section
    st.header("📦 Supply Management")
    st.write("Update supply class information and manage supply inventory.")
    
    # Initialize supply database
    init_supply_database()
    
    # Supply form
    with st.form("supply_form"):
        st.subheader("Update Supply Class")
        
        col1, col2 = st.columns(2)
        
        with col1:
            supply_id = st.text_input("Supply ID", placeholder="Enter supply ID", help="Required field")
            supply_name = st.text_input("Supply Name", placeholder="Enter supply name", help="Required field")
            supply_class = st.selectbox("Supply Class", 
                                      ["Ammunition", "Fuel", "Medical", "Food", "Equipment", "Clothing"], 
                                      help="Select supply class")
            supply_type = st.selectbox("Supply Type", 
                                     ["Consumable", "Durable", "Perishable", "Hazardous"], 
                                     help="Select supply type")
        
        with col2:
            quantity = st.number_input("Quantity", min_value=0, value=0, help="Enter quantity in stock")
            unit = st.selectbox("Unit", 
                              ["Each", "Box", "Pallet", "Gallon", "Pound", "Kilogram"], 
                              help="Select unit of measurement")
            status = st.selectbox("Status", 
                                ["Available", "Low Stock", "Out of Stock", "Reserved"], 
                                help="Select supply status")
            priority = st.selectbox("Priority", 
                                  ["Low", "Medium", "High", "Critical"], 
                                  help="Select supply priority")
        
        # Additional information
        location = st.text_input("Storage Location", placeholder="Enter storage location")
        supplier = st.text_input("Supplier", placeholder="Enter supplier name")
        notes = st.text_area("Supply Notes", placeholder="Enter additional notes or comments")
        
        # Form validation
        supply_validation_errors = []
        
        # Required field validation
        if not supply_id:
            supply_validation_errors.append("Supply ID is required")
        if not supply_name:
            supply_validation_errors.append("Supply Name is required")
        
        # Quantity validation
        if quantity < 0:
            supply_validation_errors.append("Quantity must be non-negative")
        
        # Display validation errors
        if supply_validation_errors:
            for error in supply_validation_errors:
                st.error(f"⚠️ {error}")
        
        # Submit button
        supply_submitted = st.form_submit_button("Save Supply Data", type="primary")
        
        if supply_submitted:
            if not supply_validation_errors:
                # Save to supply database
                success = save_supply_data({
                    'supply_id': supply_id,
                    'supply_name': supply_name,
                    'supply_class': supply_class,
                    'supply_type': supply_type,
                    'quantity': quantity,
                    'unit': unit,
                    'status': status,
                    'priority': priority,
                    'location': location,
                    'supplier': supplier,
                    'notes': notes,
                    'updated_at': datetime.now().isoformat()
                })
                
                if success:
                    st.success("✅ Supply data saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save supply data. Please try again.")
            else:
                st.warning("Please fix the validation errors before submitting.")
    
    # Display existing supply data
    st.subheader("Current Supply Inventory")
    supply_data = get_supply_data()
    
    if not supply_data.empty:
        st.dataframe(supply_data, use_container_width=True)
        
        # Supply metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_items = len(supply_data)
            st.metric("Total Items", total_items)
        
        with col2:
            low_stock_count = len(supply_data[supply_data['status'] == 'Low Stock'])
            st.metric("Low Stock Items", low_stock_count, delta=f"-{low_stock_count}" if low_stock_count > 0 else "0")
        
        with col3:
            out_of_stock_count = len(supply_data[supply_data['status'] == 'Out of Stock'])
            st.metric("Out of Stock", out_of_stock_count, delta=f"-{out_of_stock_count}" if out_of_stock_count > 0 else "0")
        
        with col4:
            critical_count = len(supply_data[supply_data['priority'] == 'Critical'])
            st.metric("Critical Items", critical_count, delta=f"-{critical_count}" if critical_count > 0 else "0")
    else:
        st.info("No supply records found. Add some supply data using the form above.")

def init_database():
    """Initialize the SQLite database for personnel data."""
    conn = sqlite3.connect('personnel.db')
    cursor = conn.cursor()
    
    # Create personnel table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personnel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            personnel_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            personnel_class TEXT NOT NULL,
            rank TEXT,
            unit TEXT,
            clearance_level TEXT,
            status TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_personnel_data(personnel_data):
    """Save personnel data to the database."""
    try:
        conn = sqlite3.connect('personnel.db')
        cursor = conn.cursor()
        
        # Insert or update personnel data
        cursor.execute('''
            INSERT OR REPLACE INTO personnel 
            (personnel_id, first_name, last_name, personnel_class, rank, unit, clearance_level, status, notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            personnel_data['personnel_id'],
            personnel_data['first_name'],
            personnel_data['last_name'],
            personnel_data['personnel_class'],
            personnel_data['rank'],
            personnel_data['unit'],
            personnel_data['clearance_level'],
            personnel_data['status'],
            personnel_data['notes'],
            personnel_data['updated_at']
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return False

def get_personnel_data():
    """Retrieve all personnel data from the database."""
    try:
        conn = sqlite3.connect('personnel.db')
        df = pd.read_sql_query("SELECT * FROM personnel ORDER BY updated_at DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return pd.DataFrame()

def init_supply_database():
    """Initialize the SQLite database for supply data."""
    conn = sqlite3.connect('supply.db')
    cursor = conn.cursor()
    
    # Create supply table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS supply (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supply_id TEXT UNIQUE NOT NULL,
            supply_name TEXT NOT NULL,
            supply_class TEXT NOT NULL,
            supply_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit TEXT NOT NULL,
            status TEXT NOT NULL,
            priority TEXT NOT NULL,
            location TEXT,
            supplier TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_supply_data(supply_data):
    """Save supply data to the database."""
    try:
        conn = sqlite3.connect('supply.db')
        cursor = conn.cursor()
        
        # Insert or update supply data
        cursor.execute('''
            INSERT OR REPLACE INTO supply 
            (supply_id, supply_name, supply_class, supply_type, quantity, unit, status, priority, location, supplier, notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            supply_data['supply_id'],
            supply_data['supply_name'],
            supply_data['supply_class'],
            supply_data['supply_type'],
            supply_data['quantity'],
            supply_data['unit'],
            supply_data['status'],
            supply_data['priority'],
            supply_data['location'],
            supply_data['supplier'],
            supply_data['notes'],
            supply_data['updated_at']
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Supply database error: {str(e)}")
        return False

def get_supply_data():
    """Retrieve all supply data from the database."""
    try:
        conn = sqlite3.connect('supply.db')
        df = pd.read_sql_query("SELECT * FROM supply ORDER BY updated_at DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Supply database error: {str(e)}")
        return pd.DataFrame()

if __name__ == "__main__":
        main()
