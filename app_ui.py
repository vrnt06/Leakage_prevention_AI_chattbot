# app_ui.py
import streamlit as st
import chatbot_engine as engine

st.set_page_config(page_title="SDG 6 Water Infrastructure Auditor", page_icon="💧", layout="centered")

st.title("💧 SDG 6: Clean Water Infrastructure Auditor")
st.caption("An interactive AI dispatch system parsing conversational inputs to combat global water resource depletion.")

# -----------------------------
# Secure API Key Side Panel
# -----------------------------
with st.sidebar:
    st.write("### 🔑 API Key Authentication")
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Grab a free token inside Google AI Studio")
    st.info("Don't have an API key? You can generate a free development key at Google AI Studio instantly.")

if not api_key:
    st.warning("Please provide a valid Google AI API key in the sidebar panel to connect the infrastructure pipeline.")
    st.stop()

# Initialize core sessions
if "water_chat" not in st.session_state:
    st.session_state.water_chat = engine.initialize_water_bot(api_key)
if "chat_display_logs" not in st.session_state:
    st.session_state.chat_display_logs = [
        {"role": "assistant", "content": "Welcome to the Municipal Water Control Desk. Please describe the issue you are observing, including the location and estimated rate of water flow or contamination."}
    ]
if "gallons_wasted" not in st.session_state:
    st.session_state.gallons_wasted = 0
if "dispatch_tickets" not in st.session_state:
    st.session_state.dispatch_tickets = []

# -----------------------------
# Infrastructure Analytics Metrics
# -----------------------------
st.write("### 📊 Real-Time Operations Monitoring Matrix")
stat_col1, stat_col2 = st.columns(2)

with stat_col1:
    st.metric(
        label="Total Wasted Fluid Vol (Est.)", 
        value=f"{st.session_state.gallons_wasted} Gallons/Day",
        delta=f"+{st.session_state.gallons_wasted} Over Baseline" if st.session_state.gallons_wasted > 0 else None,
        delta_color="inverse"
    )

with stat_col2:
    if st.button("Reset Operations Dashboard", use_container_width=True):
        st.session_state.water_chat = engine.initialize_water_bot(api_key)
        st.session_state.chat_display_logs = [{"role": "assistant", "content": "Dashboard reset complete. Listening for incoming infrastructure field inputs..."}]
        st.session_state.gallons_wasted = 0
        st.session_state.dispatch_tickets = []
        st.rerun()

st.divider()

# -----------------------------
# Active Chat Interface Layout
# -----------------------------
for msg in st.session_state.chat_display_logs:
    with st.chat_message(msg["role"]):
        # Strips away background tags from the frontend text view
        clean_text = msg["content"].split("[SEVERITY:")[0].strip()
        st.write(clean_text)

if user_input := st.chat_input("Ex: 'A main pipe split open on 5th Avenue and it's flooding the street'"):
    st.session_state.chat_display_logs.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
        
    with st.chat_message("assistant"):
        with st.spinner("AI analyzing infrastructure report telemetry..."):
            response = st.session_state.water_chat.send_message(user_input)
            raw_response = response.text
            
        # Parse the backend string to retrieve status adjustments
        loss_volume, severity_label = engine.evaluate_leakage_metrics(raw_response)
        
        # Adjust session data structures
        st.session_state.gallons_wasted += loss_volume
        st.session_state.dispatch_tickets.append({
            "User Notification Snippet": user_input[:45] + "...",
            "Severity Assignment": severity_label,
            "Daily Fluid Loss Cost": f"{loss_volume} Gal/Day"
        })
        
        # Output parsed response cleanly
        clean_response = raw_response.split("[SEVERITY:")[0].strip()
        st.write(clean_response)
        
        st.session_state.chat_display_logs.append({"role": "assistant", "content": raw_response})
        st.rerun()

# -----------------------------
# Dispatch Logistics Table
# -----------------------------
if st.session_state.dispatch_tickets:
    st.write("### 📝 Generated Utility Dispatch Matrix")
    st.dataframe(st.session_state.dispatch_tickets, use_container_width=True, hide_index=True)