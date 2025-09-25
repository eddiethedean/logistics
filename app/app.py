import streamlit as st

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

if __name__ == "__main__":
    main()
