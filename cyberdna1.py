import streamlit as st
import time
import random
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="CyberDNA Cybersecurity Simulation",
    page_icon="🛡️",
    layout="wide"
)

# Define baseline for healthy system behavior
baseline = {
    "cpu_usage": (10, 15),
    "network_activity": (20, 40),
    "file_access_rate": (0, 3)
}

def simulate_behavior(cycle, total):
    """Simulate system behavior with anomalies in early cycles, normal in final cycle"""
    if cycle == total - 1:
        # Final cycle: return safe values
        return {
            "cpu_usage": 12,
            "network_activity": 30,
            "file_access_rate": 1
        }
    else:
        return {
            "cpu_usage": random.randint(5, 45),
            "network_activity": random.randint(10, 50),
            "file_access_rate": random.randint(0, 7)
        }

def detect_anomalies(values):
    """Detect anomalies by comparing values against baseline ranges"""
    anomalies = {}
    for k, (low, high) in baseline.items():
        v = values[k]
        if not (low <= v <= high):
            anomalies[k] = {
                "value": v,
                "expected_range": f"{low}-{high}"
            }
    return anomalies

def display_metrics(values, anomalies):
    """Display system metrics with color coding based on anomaly status"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if "cpu_usage" in anomalies:
            st.error(f"🔴 CPU Usage: {values['cpu_usage']}%")
        else:
            st.success(f"✅ CPU Usage: {values['cpu_usage']}%")
    
    with col2:
        if "network_activity" in anomalies:
            st.error(f"🔴 Network Activity: {values['network_activity']} Mbps")
        else:
            st.success(f"✅ Network Activity: {values['network_activity']} Mbps")
    
    with col3:
        if "file_access_rate" in anomalies:
            st.error(f"🔴 File Access Rate: {values['file_access_rate']}/sec")
        else:
            st.success(f"✅ File Access Rate: {values['file_access_rate']}/sec")

def display_anomalies(anomalies):
    """Display detailed anomaly information"""
    if anomalies:
        st.warning("⚠️ **Anomalies Detected:**")
        anomaly_data = []
        for key, details in anomalies.items():
            anomaly_data.append({
                "Metric": key.replace('_', ' ').title(),
                "Current Value": details["value"],
                "Expected Range": details["expected_range"]
            })
        st.table(anomaly_data)
    else:
        st.info("✅ **All systems normal. No threats detected.**")

def show_threat_response():
    """Display threat response animation"""
    st.error("🚨 **Threat Detected! Initiating Response...**")
    
    # Create placeholder for response steps
    response_placeholder = st.empty()
    
    response_steps = [
        "🔍 Analyzing threat patterns...",
        "🛡️ Isolating affected systems...",
        "🔧 Rolling back malicious changes...",
        "✅ System healed and secured!"
    ]
    
    for i, step in enumerate(response_steps):
        if i < len(response_steps) - 1:
            response_placeholder.warning(step)
        else:
            response_placeholder.success(step)
        time.sleep(1)

def run_simulation():
    """Main simulation logic"""
    st.title("🛡️ CyberDNA Cybersecurity Simulation")
    st.markdown("**Real-time threat detection and response demonstration**")
    
    # Initialize session state
    if 'simulation_running' not in st.session_state:
        st.session_state.simulation_running = False
        st.session_state.cycle = 0
        st.session_state.total_cycles = 3
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("🚀 Start Simulation", disabled=st.session_state.simulation_running):
            st.session_state.simulation_running = True
            st.session_state.cycle = 0
    
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.simulation_running = False
            st.session_state.cycle = 0
            st.rerun()
    
    # Display current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"**Current Time:** {timestamp}")
    
    # Run simulation if active
    if st.session_state.simulation_running:
        if st.session_state.cycle < st.session_state.total_cycles:
            # Display current cycle information
            st.markdown(f"### 📊 Monitoring Cycle {st.session_state.cycle + 1} of {st.session_state.total_cycles}")
            
            # Simulate system behavior
            values = simulate_behavior(st.session_state.cycle, st.session_state.total_cycles)
            anomalies = detect_anomalies(values)
            
            # Display metrics
            display_metrics(values, anomalies)
            
            st.markdown("---")
            
            # Display anomalies or normal status
            display_anomalies(anomalies)
            
            # Show detailed data in expandable section
            with st.expander("📋 Detailed System Data"):
                st.json({
                    "timestamp": timestamp,
                    "cycle": st.session_state.cycle + 1,
                    "metrics": values,
                    "anomalies": anomalies if anomalies else "None detected"
                })
            
            # Handle threat response if anomalies detected
            if anomalies:
                show_threat_response()
                time.sleep(2)
            else:
                time.sleep(2)
            
            # Progress to next cycle
            st.session_state.cycle += 1
            time.sleep(1)
            st.rerun()
        
        else:
            # Simulation complete
            st.success("🎉 **Simulation Complete!**")
            st.info("The CyberDNA system successfully detected and responded to all threats. System is now secure.")
            st.session_state.simulation_running = False
            
            # Show summary
            st.markdown("### 📈 Simulation Summary")
            summary_data = {
                "Total Cycles": st.session_state.total_cycles,
                "Threats Detected": st.session_state.total_cycles - 1,
                "Response Time": "< 3 seconds per threat",
                "System Status": "Secure ✅"
            }
            
            col1, col2 = st.columns(2)
            with col1:
                for key, value in list(summary_data.items())[:2]:
                    st.metric(key, value)
            with col2:
                for key, value in list(summary_data.items())[2:]:
                    st.metric(key, value)
    
    else:
        # Show information about the simulation
        st.markdown("### 📖 About This Simulation")
        st.info("""
        This CyberDNA simulation demonstrates:
        
        🔍 **Real-time System Monitoring**: Tracks CPU usage, network activity, and file access rates
        
        🚨 **Anomaly Detection**: Identifies when system metrics exceed normal baseline ranges
        
        🛡️ **Automated Response**: Shows how cybersecurity systems can automatically contain and neutralize threats
        
        📊 **Visual Feedback**: Provides clear visual indicators of system health and threat status
        
        Click **"Start Simulation"** to begin the demonstration.
        """)
        
        # Show baseline information
        st.markdown("### ⚖️ System Baseline (Normal Ranges)")
        baseline_display = []
        for metric, (low, high) in baseline.items():
            baseline_display.append({
                "Metric": metric.replace('_', ' ').title(),
                "Normal Range": f"{low} - {high}",
                "Unit": "%" if "cpu" in metric else "Mbps" if "network" in metric else "/sec"
            })
        st.table(baseline_display)

# Run the application
if __name__ == "__main__":
    run_simulation()