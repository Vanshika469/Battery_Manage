import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import time
import io
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Advanced Battery Cell Management System",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        animation: slideDown 1s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    .cell-card {
        background: linear-gradient(145deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 16px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .cell-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.8s;
    }
    
    .cell-card:hover::before {
        left: 100%;
    }
    
    .cell-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
    }
    
    .task-card {
        background: linear-gradient(145deg, #4facfe, #00f2fe);
        padding: 2rem;
        border-radius: 16px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 15px 35px rgba(79, 172, 254, 0.2);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        animation: fadeInLeft 1s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .task-card:hover {
        transform: scale(1.03) rotateY(5deg);
        box-shadow: 0 25px 50px rgba(79, 172, 254, 0.4);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }
    
    .status-indicator {
        width: 16px;
        height: 16px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 12px;
        position: relative;
        animation: pulse 2s infinite;
    }
    
    .status-indicator::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        border-radius: 50%;
        border: 2px solid currentColor;
        animation: ripple 2s infinite;
    }
    
    .status-active { background-color: #00ff88; color: #00ff88; }
    .status-idle { background-color: #ffd700; color: #ffd700; }
    .status-warning { background-color: #ff6b6b; color: #ff6b6b; }
    
    .datasheet-container {
        background: linear-gradient(145deg, #f8f9ff, #e6f3ff);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        animation: fadeIn 1s ease-out;
    }
    
    .export-section {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        animation: bounceIn 1s ease-out;
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-100px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    @keyframes ripple {
        0% { transform: scale(0.8); opacity: 1; }
        100% { transform: scale(2.4); opacity: 0; }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .metric-box {
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem;
        transition: transform 0.3s ease;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .metric-box:hover {
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'tasks_data' not in st.session_state:
    st.session_state.tasks_data = {}
if 'cell_list' not in st.session_state:
    st.session_state.cell_list = []
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = []

def create_cell_data(cell_type, idx):
    """Create cell data with random parameters and timestamps"""
    voltage = 3.2 if cell_type.lower() == "lfp" else 3.6
    min_voltage = 2.8 if cell_type.lower() == "lfp" else 3.2
    max_voltage = 3.6 if cell_type.lower() == "lfp" else 4.0
    current = round(random.uniform(0.5, 2.5), 2)
    temp = round(random.uniform(25, 40), 1)
    capacity = round(voltage * current, 2)
    soc = round(random.uniform(20, 100), 1)  # State of Charge
    health = round(random.uniform(85, 100), 1)  # Battery Health
    
    return {
        "voltage": voltage,
        "current": current,
        "temp": temp,
        "capacity": capacity,
        "min_voltage": min_voltage,
        "max_voltage": max_voltage,
        "soc": soc,
        "health": health,
        "status": "Active" if temp < 35 else "Warning",
        "timestamp": datetime.now(),
        "cell_type": cell_type
    }

def generate_historical_data(cells_data, hours=24):
    """Generate historical data for trend analysis"""
    historical = []
    base_time = datetime.now() - timedelta(hours=hours)
    
    for hour in range(hours):
        timestamp = base_time + timedelta(hours=hour)
        for cell_key, cell_data in cells_data.items():
            # Add some variation to simulate real data
            voltage_variation = random.uniform(-0.1, 0.1)
            temp_variation = random.uniform(-2, 2)
            current_variation = random.uniform(-0.2, 0.2)
            
            historical.append({
                'timestamp': timestamp,
                'cell_id': cell_key,
                'voltage': max(cell_data['min_voltage'], 
                              min(cell_data['max_voltage'], 
                                  cell_data['voltage'] + voltage_variation)),
                'temperature': max(20, cell_data['temp'] + temp_variation),
                'current': max(0, cell_data['current'] + current_variation),
                'capacity': cell_data['capacity'],
                'soc': max(0, min(100, cell_data['soc'] + random.uniform(-5, 5))),
                'health': cell_data['health']
            })
    
    return historical

def main():
    # Header with enhanced styling
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🔋 Advanced Battery Management System
        </h1>
        <p style="font-size: 1.2rem; margin-top: 1rem; opacity: 0.9;">
            Complete Battery Cell Analysis, Monitoring & Data Management Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Navigation Panel")
        page = st.selectbox(
            "Select Module", 
            ["🔧 Cell Configuration", "📋 Task Management", "📊 Live Dashboard", 
             "📈 Data Analysis", "📋 Datasheet View", "💾 Export Center"],
            index=0
        )
        
        st.markdown("---")
        
        # Quick stats in sidebar
        if st.session_state.cells_data:
            st.markdown("### 📊 Quick Stats")
            total_cells = len(st.session_state.cells_data)
            avg_temp = sum(cell['temp'] for cell in st.session_state.cells_data.values()) / total_cells
            active_cells = sum(1 for cell in st.session_state.cells_data.values() if cell['status'] == 'Active')
            
            st.metric("Total Cells", total_cells)
            st.metric("Active Cells", active_cells)
            st.metric("Avg Temperature", f"{avg_temp:.1f}°C")
        
        st.markdown("---")
        st.markdown("### 🚀 Features")
        st.info("✅ Real-time Monitoring\n✅ Advanced Analytics\n✅ Data Export\n✅ Historical Trends")
    
    # Route to different pages
    if "Cell Configuration" in page:
        cell_configuration_page()
    elif "Task Management" in page:
        task_management_page()
    elif "Live Dashboard" in page:
        dashboard_page()
    elif "Data Analysis" in page:
        data_analysis_page()
    elif "Datasheet View" in page:
        datasheet_page()
    elif "Export Center" in page:
        export_page()

def cell_configuration_page():
    st.header("🔧 Advanced Cell Configuration")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚡ Create Cell Network")
        with st.form("cell_form"):
            num_cells = st.number_input("Number of Cells", min_value=1, max_value=100, value=5)
            
            # Advanced cell configuration
            st.markdown("#### Cell Type Configuration")
            cell_types = []
            
            # Use tabs for better organization
            if num_cells <= 10:
                for i in range(num_cells):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        cell_type = st.selectbox(
                            f"Cell {i+1} Type", 
                            ["LFP", "Li-ion", "NMC", "LTO", "LiPo"], 
                            key=f"cell_type_{i}"
                        )
                    with col_b:
                        priority = st.selectbox(
                            "Priority",
                            ["High", "Medium", "Low"],
                            key=f"priority_{i}"
                        )
                    cell_types.append((cell_type, priority))
            else:
                # Bulk configuration for many cells
                default_type = st.selectbox("Default Cell Type", ["LFP", "Li-ion", "NMC", "LTO", "LiPo"])
                cell_types = [(default_type, "Medium") for _ in range(num_cells)]
            
            generate_historical = st.checkbox("Generate Historical Data (24h)", value=True)
            
            submitted = st.form_submit_button("⚡ Generate Cell Network", use_container_width=True)
            
            if submitted:
                st.session_state.cell_list = [ct[0] for ct in cell_types]
                st.session_state.cells_data = {}
                
                # Enhanced progress tracking
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, (cell_type, priority) in enumerate(cell_types):
                        cell_key = f"cell_{idx+1}_{cell_type.lower()}"
                        cell_data = create_cell_data(cell_type, idx+1)
                        cell_data['priority'] = priority
                        st.session_state.cells_data[cell_key] = cell_data
                        
                        progress = (idx + 1) / len(cell_types)
                        progress_bar.progress(progress)
                        status_text.text(f"⚡ Generating {cell_key}... ({idx+1}/{len(cell_types)})")
                        time.sleep(0.05)
                    
                    if generate_historical:
                        status_text.text("📊 Generating historical data...")
                        st.session_state.historical_data = generate_historical_data(st.session_state.cells_data)
                    
                    status_text.text("✅ Cell network generated successfully!")
                    st.success(f"🎉 Generated {len(cell_types)} cells with full data!")
                    time.sleep(1)
                    progress_bar.empty()
                    status_text.empty()
    
    with col2:
        if st.session_state.cells_data:
            st.subheader("🔋 Network Overview")
            
            # Enhanced metrics
            total_cells = len(st.session_state.cells_data)
            active_cells = sum(1 for cell in st.session_state.cells_data.values() if cell['status'] == 'Active')
            warning_cells = total_cells - active_cells
            avg_temp = sum(cell['temp'] for cell in st.session_state.cells_data.values()) / total_cells
            avg_voltage = sum(cell['voltage'] for cell in st.session_state.cells_data.values()) / total_cells
            total_capacity = sum(cell['capacity'] for cell in st.session_state.cells_data.values())
            avg_health = sum(cell['health'] for cell in st.session_state.cells_data.values()) / total_cells
            
            # Display metrics in cards
            metrics_data = [
                ("Total Cells", total_cells, "🔋"),
                ("Active", active_cells, "✅"),
                ("Warning", warning_cells, "⚠️"),
                ("Avg Temp", f"{avg_temp:.1f}°C", "🌡️"),
                ("Avg Voltage", f"{avg_voltage:.2f}V", "⚡"),
                ("Total Capacity", f"{total_capacity:.1f}Wh", "🔥"),
                ("Avg Health", f"{avg_health:.1f}%", "❤️")
            ]
            
            for i in range(0, len(metrics_data), 2):
                col_a, col_b = st.columns(2)
                with col_a:
                    label, value, icon = metrics_data[i]
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 2rem;">{icon}</div>
                        <div style="font-size: 1.5rem; font-weight: bold;">{value}</div>
                        <div style="opacity: 0.8;">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                if i + 1 < len(metrics_data):
                    with col_b:
                        label, value, icon = metrics_data[i + 1]
                        st.markdown(f"""
                        <div class="metric-box">
                            <div style="font-size: 2rem;">{icon}</div>
                            <div style="font-size: 1.5rem; font-weight: bold;">{value}</div>
                            <div style="opacity: 0.8;">{label}</div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Enhanced cell display
    if st.session_state.cells_data:
        st.markdown("---")
        st.subheader("🔍 Detailed Cell Information")
        
        # Filter and sort options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Active", "Warning"])
        with col2:
            sort_by = st.selectbox("Sort by", ["Cell ID", "Temperature", "Voltage", "Health"])
        with col3:
            view_mode = st.selectbox("View Mode", ["Cards", "Compact"])
        
        # Apply filters and sorting
        filtered_cells = st.session_state.cells_data.copy()
        if status_filter != "All":
            filtered_cells = {k: v for k, v in filtered_cells.items() if v['status'] == status_filter}
        
        # Sort cells
        if sort_by == "Temperature":
            filtered_cells = dict(sorted(filtered_cells.items(), key=lambda x: x[1]['temp'], reverse=True))
        elif sort_by == "Voltage":
            filtered_cells = dict(sorted(filtered_cells.items(), key=lambda x: x[1]['voltage'], reverse=True))
        elif sort_by == "Health":
            filtered_cells = dict(sorted(filtered_cells.items(), key=lambda x: x[1]['health'], reverse=True))
        
        if view_mode == "Cards":
            # Card view
            for cell_key, cell_data in filtered_cells.items():
                status_class = "status-active" if cell_data['status'] == 'Active' else "status-warning"
                health_color = "🟢" if cell_data['health'] > 90 else "🟡" if cell_data['health'] > 75 else "🔴"
                
                st.markdown(f"""
                <div class="cell-card">
                    <h3><span class="status-indicator {status_class}"></span>{cell_key.upper()}</h3>
                    <div class="metric-card">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div>
                                <strong>🔋 Voltage:</strong> {cell_data['voltage']}V<br>
                                <strong>⚡ Current:</strong> {cell_data['current']}A<br>
                                <strong>🌡️ Temperature:</strong> {cell_data['temp']}°C<br>
                                <strong>🔥 Capacity:</strong> {cell_data['capacity']}Wh
                            </div>
                            <div>
                                <strong>📊 State of Charge:</strong> {cell_data['soc']}%<br>
                                <strong>❤️ Health:</strong> {health_color} {cell_data['health']}%<br>
                                <strong>🎯 Priority:</strong> {cell_data.get('priority', 'Medium')}<br>
                                <strong>📝 Type:</strong> {cell_data['cell_type']}
                            </div>
                        </div>
                        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.2);">
                            <strong>Range:</strong> {cell_data['min_voltage']}V - {cell_data['max_voltage']}V | 
                            <strong>Status:</strong> {cell_data['status']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Compact table view
            df = pd.DataFrame.from_dict(filtered_cells, orient='index')
            st.dataframe(df, use_container_width=True)

def task_management_page():
    st.header("📋 Advanced Task Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("➕ Create New Task")
        
        with st.form("task_form"):
            task_name = st.text_input("Task Name", placeholder="e.g., Charging Cycle 1")
            task_type = st.selectbox("Task Type", ["CC_CV", "IDLE", "CC_CD"])
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            
            # Estimated duration calculator
            if task_type == "CC_CV":
                st.markdown("**⚡ Constant Current - Constant Voltage Parameters**")
                col_a, col_b = st.columns(2)
                with col_a:
                    cc_input = st.text_input("CC/CP Value", placeholder="e.g., 5A or 10W")
                    cv_voltage = st.number_input("CV Voltage (V)", min_value=0.0, value=3.6, step=0.1)
                with col_b:
                    current = st.number_input("Current (A)", min_value=0.0, value=1.0, step=0.1)
                    capacity = st.number_input("Capacity", min_value=0.0, value=100.0, step=1.0)
                
                time_seconds = st.number_input("Duration (seconds)", min_value=1, value=3600, step=1)
                
                # Calculate estimated completion
                hours = time_seconds // 3600
                minutes = (time_seconds % 3600) // 60
                st.info(f"⏱️ Estimated Duration: {hours}h {minutes}m")
                
                task_data = {
                    "task_name": task_name,
                    "task_type": "CC_CV",
                    "cc_cp": cc_input,
                    "cv_voltage": cv_voltage,
                    "current": current,
                    "capacity": capacity,
                    "time_seconds": time_seconds,
                    "priority": priority,
                    "created_at": datetime.now(),
                    "status": "Pending"
                }
                
            elif task_type == "IDLE":
                st.markdown("**⏸️ Idle Task Parameters**")
                time_seconds = st.number_input("Duration (seconds)", min_value=1, value=600, step=1)
                
                hours = time_seconds // 3600
                minutes = (time_seconds % 3600) // 60
                st.info(f"⏱️ Idle Duration: {hours}h {minutes}m")
                
                task_data = {
                    "task_name": task_name,
                    "task_type": "IDLE",
                    "time_seconds": time_seconds,
                    "priority": priority,
                    "created_at": datetime.now(),
                    "status": "Pending"
                }
                
            elif task_type == "CC_CD":
                st.markdown("**🔋 Constant Current - Constant Discharge Parameters**")
                col_a, col_b = st.columns(2)
                with col_a:
                    cc_input = st.text_input("CC/CP Value", placeholder="e.g., 5A or 10W")
                    voltage = st.number_input("Voltage (V)", min_value=0.0, value=3.2, step=0.1)
                with col_b:
                    capacity = st.number_input("Capacity", min_value=0.0, value=100.0, step=1.0)
                    time_seconds = st.number_input("Duration (seconds)", min_value=1, value=3600, step=1)
                
                hours = time_seconds // 3600
                minutes = (time_seconds % 3600) // 60
                st.info(f"⏱️ Estimated Duration: {hours}h {minutes}m")
                
                task_data = {
                    "task_name": task_name,
                    "task_type": "CC_CD",
                    "cc_cp": cc_input,
                    "voltage": voltage,
                    "capacity": capacity,
                    "time_seconds": time_seconds,
                    "priority": priority,
                    "created_at": datetime.now(),
                    "status": "Pending"
                }
            
            submitted = st.form_submit_button("🚀 Add Task", use_container_width=True)
            
            if submitted:
                task_number = len(st.session_state.tasks_data) + 1
                task_key = f"task_{task_number}"
                st.session_state.tasks_data[task_key] = task_data
                st.success(f"✅ Task '{task_name}' added successfully!")
    
    with col2:
        if st.session_state.tasks_data:
            st.subheader("📊 Task Queue Analytics")
            
            # Enhanced task analytics
            total_tasks = len(st.session_state.tasks_data)
            pending_tasks = sum(1 for task in st.session_state.tasks_data.values() if task.get('status') == 'Pending')
            high_priority = sum(1 for task in st.session_state.tasks_data.values() if task.get('priority') == 'High')
            
            # Calculate total estimated time
            total_time = sum(task.get('time_seconds', 0) for task in st.session_state.tasks_data.values())
            total_hours = total_time // 3600
            total_minutes = (total_time % 3600) // 60
            
            # Task type distribution
            task_types = {}
            for task in st.session_state.tasks_data.values():
                task_type = task.get('task_type', 'Unknown')
                