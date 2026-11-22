"""
IndiGo Airlines - Agent Gatekeeper Prototype
=============================================
Course: MBA in AI Agent Governance and Security
Project: Agent Gatekeeper for IndiGo Airlines

This application simulates an enterprise security gatekeeper / firewall
that governs personal AI agents attempting to perform actions on behalf of customers.
"""

import io
from datetime import datetime
import pandas as pd
import streamlit as st

# Import the core security rules engine
from gatekeeper import (
    DECISION_ALLOW,
    DECISION_ASK_CUSTOMER,
    DECISION_BLOCK,
    STATUS_REGISTERED,
    STATUS_UNKNOWN,
    STATUS_REVOKED,
    ACTION_VIEW_FARES,
    ACTION_BOOK_FLIGHT,
    ACTION_CHANGE_FLIGHT,
    ACTION_CANCEL_FLIGHT,
    ACTION_REQUEST_REFUND,
    ALL_ACTIONS,
    MAX_AUTONOMOUS_BOOKING_AMOUNT_INR,
    evaluate_security_rule,
    get_predefined_test_cases,
    run_all_security_tests
)

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="IndiGo Agent Gatekeeper | AI Governance",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM STYLING (IndiGo Airline Theme: Navy Blue, White, Light Blue)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Background and Fonts */
    .main {
        background-color: #f6f9fc;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }

    /* Primary Navy Header Banner */
    .indigo-header {
        background: linear-gradient(135deg, #001b69 0%, #002e8a 55%, #0056b3 100%);
        color: #ffffff;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(0, 27, 105, 0.2);
    }
    .indigo-header h1 {
        color: #ffffff !important;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .indigo-header p {
        color: #dbeafe;
        font-size: 14px;
        margin-top: 6px;
        margin-bottom: 0;
    }
    .airline-tag {
        display: inline-block;
        background-color: #ffffff;
        color: #001b69;
        font-weight: 800;
        font-size: 11px;
        padding: 3px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    /* Student Badge */
    .student-badge-card {
        background-color: #ffffff;
        border: 1px solid #bfdbfe;
        border-left: 5px solid #002e8a;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }

    /* Cards */
    .custom-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 18px;
    }

    /* Decision Result Badges */
    .decision-badge-allow {
        background: linear-gradient(135deg, #0f5132 0%, #198754 100%);
        color: #ffffff;
        padding: 16px 20px;
        border-radius: 10px;
        font-size: 22px;
        font-weight: 800;
        text-align: center;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 12px rgba(25, 135, 84, 0.25);
    }
    .decision-badge-ask {
        background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
        color: #ffffff;
        padding: 16px 20px;
        border-radius: 10px;
        font-size: 22px;
        font-weight: 800;
        text-align: center;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 12px rgba(217, 119, 6, 0.25);
    }
    .decision-badge-block {
        background: linear-gradient(135deg, #842029 0%, #dc3545 100%);
        color: #ffffff;
        padding: 16px 20px;
        border-radius: 10px;
        font-size: 22px;
        font-weight: 800;
        text-align: center;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 12px rgba(220, 53, 69, 0.25);
    }

    /* Reason Alert Box */
    .reason-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 14px 18px;
        margin-top: 14px;
        font-size: 14px;
        line-height: 1.5;
        color: #1e293b;
    }

    /* Metric Boxes */
    .metric-box {
        background: #ffffff;
        border-top: 4px solid #002e8a;
        padding: 14px;
        border-radius: 8px;
        text-align: center;
        border-left: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #001b69;
    }
    .metric-label {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }

    /* Security Rules List Card */
    .rule-item {
        padding: 8px 12px;
        border-radius: 6px;
        margin-bottom: 6px;
        background-color: #f1f5f9;
        font-size: 13px;
        border-left: 4px solid #002e8a;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
def initialize_state():
    """Initializes session state with student details, agents, and audit logs."""
    # Student Details
    if "student_name" not in st.session_state:
        st.session_state.student_name = "[ENTER YOUR NAME]"
    if "student_enrollment" not in st.session_state:
        st.session_state.student_enrollment = "[ENTER YOUR ENROLLMENT NUMBER]"

    # Pre-seeded AI Agents Registry
    if "agents" not in st.session_state:
        st.session_state.agents = [
            {
                "name": "IndiGo TravelBuddy",
                "status": STATUS_REGISTERED,
                "provider": "IndiGo Official Certified Agent",
                "registered_at": "2026-10-15 09:30:00",
                "revoked_at": "-"
            },
            {
                "name": "Siri Flight Concierge",
                "status": STATUS_REGISTERED,
                "provider": "Apple Personal Assistant Ecosystem",
                "registered_at": "2026-10-20 11:15:00",
                "revoked_at": "-"
            },
            {
                "name": "MakeMyTrip AI Delegate",
                "status": STATUS_REGISTERED,
                "provider": "MakeMyTrip OTA Agent API",
                "registered_at": "2026-11-01 14:00:00",
                "revoked_at": "-"
            },
            {
                "name": "CompromisedScraperBot",
                "status": STATUS_REVOKED,
                "provider": "Third-party Unknown Scraper",
                "registered_at": "2026-09-01 10:00:00",
                "revoked_at": "2026-11-05 16:45:12"
            }
        ]

    # Pre-seeded Audit Log
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = [
            {
                "timestamp": "2026-11-20 10:14:22",
                "customer_name": "Aditya Verma",
                "agent_name": "IndiGo TravelBuddy",
                "status": STATUS_REGISTERED,
                "action": ACTION_VIEW_FARES,
                "amount": 0.0,
                "customer_confirmation": "No",
                "decision": DECISION_ALLOW,
                "reason": "Security Rule 2: Registered agents are permitted to view flight schedules and fares autonomously."
            },
            {
                "timestamp": "2026-11-20 11:30:45",
                "customer_name": "Neha Sharma",
                "agent_name": "Siri Flight Concierge",
                "status": STATUS_REGISTERED,
                "action": ACTION_BOOK_FLIGHT,
                "amount": 8450.0,
                "customer_confirmation": "Yes",
                "decision": DECISION_ALLOW,
                "reason": "Security Rule 3: Flight booking within threshold (₹8,450.00) is authorized with verified customer confirmation."
            },
            {
                "timestamp": "2026-11-21 15:20:10",
                "customer_name": "Manish Gupta",
                "agent_name": "ShadowBot_v2",
                "status": STATUS_UNKNOWN,
                "action": ACTION_VIEW_FARES,
                "amount": 0.0,
                "customer_confirmation": "No",
                "decision": DECISION_BLOCK,
                "reason": "Security Rule 1: Unknown / unregistered AI agent detected. Personal agents must be vetted and registered."
            },
            {
                "timestamp": "2026-11-21 18:05:33",
                "customer_name": "Pooja Mehta",
                "agent_name": "IndiGo TravelBuddy",
                "status": STATUS_REGISTERED,
                "action": ACTION_BOOK_FLIGHT,
                "amount": 14200.0,
                "customer_confirmation": "Yes",
                "decision": DECISION_BLOCK,
                "reason": "Security Rule 4: Flight booking amount of ₹14,200.00 exceeds the allowed autonomous agent ceiling of ₹10,000.00."
            }
        ]

    # Pre-loaded simulation form state
    if "sim_customer" not in st.session_state:
        st.session_state.sim_customer = "Rahul Sharma"
    if "sim_agent_name" not in st.session_state:
        st.session_state.sim_agent_name = "IndiGo TravelBuddy"
    if "sim_agent_status" not in st.session_state:
        st.session_state.sim_agent_status = STATUS_REGISTERED
    if "sim_action" not in st.session_state:
        st.session_state.sim_action = ACTION_BOOK_FLIGHT
    if "sim_amount" not in st.session_state:
        st.session_state.sim_amount = 7500.0
    if "sim_confirmation" not in st.session_state:
        st.session_state.sim_confirmation = "Yes"
    if "last_evaluation" not in st.session_state:
        st.session_state.last_evaluation = None


initialize_state()

# -----------------------------------------------------------------------------
# SIDEBAR: BRANDING, STUDENT DETAILS, NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 15px 0;">
            <div style="font-size: 38px;">✈️</div>
            <h2 style="color: #001b69; margin: 0; font-size: 20px; font-weight: 800; letter-spacing: 1px;">IndiGo</h2>
            <div style="color: #0078d4; font-size: 11px; font-weight: 700; letter-spacing: 2px;">6E SECURITY GATEWAY</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Editable Student Details
    st.markdown("### 🎓 Student Information")
    st.caption("Enter your details below to personalize your project submission:")

    st.session_state.student_name = st.text_input(
        "Student Name",
        value=st.session_state.student_name,
        help="Your full name as per college enrollment"
    )

    st.session_state.student_enrollment = st.text_input(
        "Enrollment Number",
        value=st.session_state.student_enrollment,
        help="Your official college roll number / student ID"
    )

    st.markdown("""
        <div style="background-color: #e8f2fe; padding: 10px; border-radius: 6px; font-size: 12px; color: #002e8a; margin-top: 8px;">
            <strong>Course:</strong> MBA in AI Agent Governance & Security<br>
            <strong>Organization:</strong> InterGlobe Aviation (IndiGo)
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation Tabs
    st.markdown("### 🧭 Dashboard Navigation")
    navigation_option = st.radio(
        "Select Section",
        [
            "🛡️ Request Simulator",
            "🤖 Agent Management",
            "📋 Audit Log & History",
            "🧪 Security Test Suite",
            "📚 Governance Rules & Guide"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; font-size: 11px; color: #64748b;">
            <strong>IndiGo Gatekeeper v2.4</strong><br>
            Autonomous Agent Governance Sandbox<br>
            Simulated Prototype • No Real APIs
        </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# MAIN HEADER BANNER (Displayed on every view)
# -----------------------------------------------------------------------------
st.markdown(f"""
    <div class="indigo-header">
        <span class="airline-tag">IndiGo Airlines • AI Security System</span>
        <h1>Agent Gatekeeper for IndiGo Airlines</h1>
        <p>A Zero-Trust Governance & Security Firewall for Personal AI Agents Interacting with Airline Systems</p>
    </div>
""", unsafe_allow_html=True)

# Student Details Card
st.markdown(f"""
    <div class="student-badge-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase;">Student Submission</span><br>
                <span style="font-size: 18px; font-weight: 700; color: #001b69;">👤 {st.session_state.student_name}</span>
            </div>
            <div>
                <span style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase;">Enrollment ID</span><br>
                <span style="font-size: 16px; font-weight: 600; color: #0056b3;">🆔 {st.session_state.student_enrollment}</span>
            </div>
            <div>
                <span style="font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase;">System Status</span><br>
                <span style="display: inline-block; background-color: #d1e7dd; color: #0f5132; font-weight: 700; font-size: 12px; padding: 3px 10px; border-radius: 12px;">
                    🟢 GATEKEEPER ACTIVE
                </span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SECTION 1: REQUEST SIMULATOR
# -----------------------------------------------------------------------------
if navigation_option == "🛡️ Request Simulator":
    st.subheader("🛡️ AI Agent Request Simulator")
    st.write(
        "Simulate an incoming interaction from a customer's personal AI agent (e.g., booking flights, "
        "checking fares, modifying itineraries) and observe the Gatekeeper's governance decision in real-time."
    )

    col_sim_left, col_sim_right = st.columns([1.1, 1], gap="large")

    with col_sim_left:
        st.markdown("#### 📝 Agent Request Payload")
        with st.form("agent_request_form"):
            # Customer Name
            customer_name_input = st.text_input(
                "Customer Name",
                value=st.session_state.sim_customer,
                help="The passenger on whose behalf the AI agent is acting"
            )

            # Agent Name & Pre-configured Agent selection
            known_agent_names = [a["name"] for a in st.session_state.agents]
            agent_choice_options = known_agent_names + ["+ Custom / Other Agent"]

            selected_agent_choice = st.selectbox(
                "Select AI Agent",
                options=agent_choice_options,
                index=0 if st.session_state.sim_agent_name in known_agent_names else len(agent_choice_options) - 1
            )

            if selected_agent_choice == "+ Custom / Other Agent":
                agent_name_input = st.text_input(
                    "Custom Agent Name",
                    value="AutonomousBot_X" if st.session_state.sim_agent_name in known_agent_names else st.session_state.sim_agent_name
                )
                default_status_index = 1  # Unknown
            else:
                agent_name_input = selected_agent_choice
                # Auto-determine status from agent registry
                matched_agent = next((a for a in st.session_state.agents if a["name"] == selected_agent_choice), None)
                if matched_agent:
                    status_map = {STATUS_REGISTERED: 0, STATUS_UNKNOWN: 1, STATUS_REVOKED: 2}
                    default_status_index = status_map.get(matched_agent["status"], 0)
                else:
                    default_status_index = 0

            # Agent Status
            agent_status_input = st.radio(
                "Agent Status in IndiGo Gatekeeper Registry",
                options=[STATUS_REGISTERED, STATUS_UNKNOWN, STATUS_REVOKED],
                index=default_status_index,
                horizontal=True,
                help="Registered (Certified), Unknown (Unverified), or Revoked (Blocked)"
            )

            # Requested Action
            action_input = st.selectbox(
                "Requested Action",
                options=ALL_ACTIONS,
                index=ALL_ACTIONS.index(st.session_state.sim_action) if st.session_state.sim_action in ALL_ACTIONS else 1
            )

            # Amount in INR
            amount_input = st.number_input(
                "Transaction Amount (INR ₹)",
                min_value=0.0,
                max_value=100000.0,
                value=float(st.session_state.sim_amount),
                step=500.0,
                help=f"Note: Autonomous bookings exceeding ₹{MAX_AUTONOMOUS_BOOKING_AMOUNT_INR:,.0f} are automatically blocked by Rule 4."
            )

            # Customer Confirmation
            confirmation_input = st.radio(
                "Customer Explicit Confirmation Obtained?",
                options=["Yes", "No"],
                index=0 if st.session_state.sim_confirmation == "Yes" else 1,
                horizontal=True,
                help="Whether the human customer verified and agreed to this action"
            )

            submit_request = st.form_submit_button("⚡ Evaluate Request with Gatekeeper", use_container_width=True)

        if submit_request:
            # Evaluate using security rules engine
            decision, reason, rule_code = evaluate_security_rule(
                agent_status=agent_status_input,
                action=action_input,
                amount_inr=amount_input,
                customer_confirmation=confirmation_input
            )

            # Record timestamp
            eval_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Store result in session state
            st.session_state.last_evaluation = {
                "timestamp": eval_time,
                "customer_name": customer_name_input,
                "agent_name": agent_name_input,
                "status": agent_status_input,
                "action": action_input,
                "amount": amount_input,
                "customer_confirmation": confirmation_input,
                "decision": decision,
                "reason": reason,
                "rule_code": rule_code
            }

            # Prepend to audit log
            st.session_state.audit_log.insert(0, {
                "timestamp": eval_time,
                "customer_name": customer_name_input,
                "agent_name": agent_name_input,
                "status": agent_status_input,
                "action": action_input,
                "amount": amount_input,
                "customer_confirmation": confirmation_input,
                "decision": decision,
                "reason": reason
            })

            # Update simulation cache
            st.session_state.sim_customer = customer_name_input
            st.session_state.sim_agent_name = agent_name_input
            st.session_state.sim_agent_status = agent_status_input
            st.session_state.sim_action = action_input
            st.session_state.sim_amount = amount_input
            st.session_state.sim_confirmation = confirmation_input

            st.rerun()

    # RIGHT COLUMN: Gatekeeper Decision Display
    with col_sim_right:
        st.markdown("#### 🎯 Gatekeeper Real-Time Decision")

        last_eval = st.session_state.last_evaluation

        if last_eval:
            dec = last_eval["decision"]

            # Visual Decision Banner
            if dec == DECISION_ALLOW:
                st.markdown(f"""
                    <div class="decision-badge-allow">
                        ✅ ALLOW
                    </div>
                """, unsafe_allow_html=True)
            elif dec == DECISION_ASK_CUSTOMER:
                st.markdown(f"""
                    <div class="decision-badge-ask">
                        ⚠️ ASK CUSTOMER
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="decision-badge-block">
                        🛑 BLOCK
                    </div>
                """, unsafe_allow_html=True)

            # Details Breakdown Card
            st.markdown(f"""
                <div class="reason-box">
                    <strong>📋 Audit Justification & Policy Reason:</strong><br>
                    {last_eval["reason"]}
                </div>
            """, unsafe_allow_html=True)

            st.markdown("##### 🔍 Inspection Details")
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.write(f"**Customer:** {last_eval['customer_name']}")
                st.write(f"**AI Agent:** {last_eval['agent_name']}")
                st.write(f"**Agent Status:** `{last_eval['status']}`")
            with col_d2:
                st.write(f"**Action:** `{last_eval['action']}`")
                st.write(f"**Amount:** ₹{last_eval['amount']:,.2f}")
                st.write(f"**Customer Confirmed:** `{last_eval['customer_confirmation']}`")

            st.caption(f"Evaluated at: {last_eval['timestamp']} | Rule Reference: `{last_eval.get('rule_code', 'N/A')}`")
            st.success("✔️ This transaction has been recorded in the Audit Log.")

        else:
            st.info("👈 Fill out the simulator form on the left and click **Evaluate Request with Gatekeeper** to see the governance decision.")

            st.markdown("""
                <div class="custom-card">
                    <h5 style="color: #001b69; margin-top: 0;">🛡️ Core Governance Rules Quick Guide</h5>
                    <div class="rule-item"><strong>1. Unknown Agents:</strong> Blocked immediately.</div>
                    <div class="rule-item"><strong>2. View Fares:</strong> Allowed autonomously for registered agents.</div>
                    <div class="rule-item"><strong>3. Booking &le; ₹10,000:</strong> Requires customer confirmation.</div>
                    <div class="rule-item"><strong>4. Booking &gt; ₹10,000:</strong> Always blocked (limit exceeded).</div>
                    <div class="rule-item"><strong>5, 6, 7. Changes, Cancels, Refunds:</strong> Require customer confirmation.</div>
                    <div class="rule-item"><strong>8. Revoked Agents:</strong> Strictly blocked from all actions.</div>
                </div>
            """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SECTION 2: AGENT MANAGEMENT
# -----------------------------------------------------------------------------
elif navigation_option == "🤖 Agent Management":
    st.subheader("🤖 AI Agent Registry & Lifecycle Management")
    st.write(
        "Govern which personal AI agents are authorized to communicate with IndiGo's digital channels. "
        "Register newly vetted agents, or immediately revoke permissions for rogue, outdated, or compromised agents."
    )

    col_reg, col_mgmt = st.columns([1, 1.4], gap="large")

    with col_reg:
        st.markdown("#### ➕ Register New Personal AI Agent")
        with st.form("register_agent_form"):
            new_agent_name = st.text_input(
                "Agent Name",
                placeholder="e.g., Samsung Bixby Travel",
                help="A unique name identifying the AI agent instance"
            )
            new_agent_provider = st.text_input(
                "Developer / Provider Ecosystem",
                placeholder="e.g., Samsung Electronics / LangChain Agent",
                help="Organization or model platform powering this agent"
            )

            register_btn = st.form_submit_button("Register Agent with Gatekeeper", use_container_width=True)

            if register_btn:
                if not new_agent_name.strip():
                    st.error("Please enter a valid agent name.")
                elif any(a["name"].lower() == new_agent_name.strip().lower() for a in st.session_state.agents):
                    st.warning(f"An agent named '{new_agent_name.strip()}' already exists in the registry.")
                else:
                    reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.agents.append({
                        "name": new_agent_name.strip(),
                        "status": STATUS_REGISTERED,
                        "provider": new_agent_provider.strip() or "Independent Personal Agent",
                        "registered_at": reg_time,
                        "revoked_at": "-"
                    })
                    st.success(f"Agent '{new_agent_name.strip()}' registered successfully as **{STATUS_REGISTERED}**!")
                    st.rerun()

        st.markdown("---")
        st.markdown("#### ⚠️ Revoke Agent Permissions")
        st.write("Revoking an agent immediately forbids it from executing any further requests (Rule 8).")

        registered_agents = [a["name"] for a in st.session_state.agents if a["status"] == STATUS_REGISTERED]

        if registered_agents:
            agent_to_revoke = st.selectbox("Select Active Agent to Revoke", options=registered_agents)
            revoke_reason = st.text_input("Revocation Audit Note", value="Security review / customer authorization withdrawn")

            if st.button("🚨 Revoke Agent Permissions Now", type="primary", use_container_width=True):
                revoke_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for a in st.session_state.agents:
                    if a["name"] == agent_to_revoke:
                        a["status"] = STATUS_REVOKED
                        a["revoked_at"] = revoke_time
                        break

                # Also add an entry in the audit log for governance tracking
                st.session_state.audit_log.insert(0, {
                    "timestamp": revoke_time,
                    "customer_name": "SECURITY ADMIN",
                    "agent_name": agent_to_revoke,
                    "status": STATUS_REVOKED,
                    "action": "REVOKE AGENT PERMISSIONS",
                    "amount": 0.0,
                    "customer_confirmation": "Yes",
                    "decision": DECISION_BLOCK,
                    "reason": f"Agent permission revoked by administrator: {revoke_reason}"
                })

                st.error(f"Agent '{agent_to_revoke}' has been REVOKED at {revoke_time}. Further requests will be blocked.")
                st.rerun()
        else:
            st.info("No active registered agents available to revoke.")

    with col_mgmt:
        st.markdown("#### 📑 Current Agent Registry")

        # Metric summary
        total_agents = len(st.session_state.agents)
        active_agents = sum(1 for a in st.session_state.agents if a["status"] == STATUS_REGISTERED)
        revoked_agents = sum(1 for a in st.session_state.agents if a["status"] == STATUS_REVOKED)

        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value">{total_agents}</div>
                    <div class="metric-label">Total Agents</div>
                </div>
            """, unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"""
                <div class="metric-box" style="border-top-color: #198754;">
                    <div class="metric-value" style="color: #198754;">{active_agents}</div>
                    <div class="metric-label">Active (Registered)</div>
                </div>
            """, unsafe_allow_html=True)
        with m_col3:
            st.markdown(f"""
                <div class="metric-box" style="border-top-color: #dc3545;">
                    <div class="metric-value" style="color: #dc3545;">{revoked_agents}</div>
                    <div class="metric-label">Revoked (Blocked)</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Display table of agents
        df_agents = pd.DataFrame(st.session_state.agents)
        df_agents.columns = ["Agent Name", "Status", "Provider / Details", "Registered Timestamp", "Revoked Timestamp"]

        st.dataframe(
            df_agents,
            use_container_width=True,
            hide_index=True
        )

        # Allow restoring a revoked agent for easy testing
        revoked_list = [a["name"] for a in st.session_state.agents if a["status"] == STATUS_REVOKED]
        if revoked_list:
            with st.expander("🔄 Re-activate / Re-register a Revoked Agent (For Testing)"):
                agent_to_reactivate = st.selectbox("Select Revoked Agent to Re-activate", options=revoked_list)
                if st.button("Re-activate Agent"):
                    for a in st.session_state.agents:
                        if a["name"] == agent_to_reactivate:
                            a["status"] = STATUS_REGISTERED
                            a["revoked_at"] = "-"
                            break
                    st.success(f"Agent '{agent_to_reactivate}' re-activated to {STATUS_REGISTERED}!")
                    st.rerun()


# -----------------------------------------------------------------------------
# SECTION 3: AUDIT LOG
# -----------------------------------------------------------------------------
elif navigation_option == "📋 Audit Log & History":
    st.subheader("📋 Gatekeeper Audit Log & Transaction Trail")
    st.write(
        "A tamper-evident audit record of every personal AI agent interaction, decision, and rationale. "
        "Compliant with AI governance transparency standards and downloadable for compliance reviews."
    )

    if not st.session_state.audit_log:
        st.warning("No audit records present in the log yet.")
    else:
        # Summary counts
        total_records = len(st.session_state.audit_log)
        allow_count = sum(1 for r in st.session_state.audit_log if r["decision"] == DECISION_ALLOW)
        ask_count = sum(1 for r in st.session_state.audit_log if r["decision"] == DECISION_ASK_CUSTOMER)
        block_count = sum(1 for r in st.session_state.audit_log if r["decision"] == DECISION_BLOCK)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Requests Evaluated", total_records)
        with c2:
            st.metric("Allowed (ALLOW)", allow_count)
        with c3:
            st.metric("Escalated (ASK CUSTOMER)", ask_count)
        with c4:
            st.metric("Blocked (BLOCK)", block_count)

        st.markdown("---")

        # Filters
        f_col1, f_col2 = st.columns([1, 2])
        with f_col1:
            decision_filter = st.selectbox(
                "Filter by Decision",
                options=["All", DECISION_ALLOW, DECISION_ASK_CUSTOMER, DECISION_BLOCK]
            )
        with f_col2:
            search_query = st.text_input("Search by Customer, Agent, or Action", placeholder="e.g. Rahul, Siri, Book Flight")

        # Apply Filters
        filtered_log = st.session_state.audit_log
        if decision_filter != "All":
            filtered_log = [r for r in filtered_log if r["decision"] == decision_filter]
        if search_query.strip():
            sq = search_query.strip().lower()
            filtered_log = [
                r for r in filtered_log
                if sq in r["customer_name"].lower()
                or sq in r["agent_name"].lower()
                or sq in r["action"].lower()
            ]

        # Display Dataframe
        if filtered_log:
            df_display = pd.DataFrame(filtered_log)
            # Reorder & rename columns for clean display
            column_order = ["timestamp", "customer_name", "agent_name", "status", "action", "amount", "customer_confirmation", "decision", "reason"]
            df_display = df_display[[c for c in column_order if c in df_display.columns]]
            df_display.columns = ["Timestamp", "Customer Name", "Agent Name", "Agent Status", "Action", "Amount (INR ₹)", "Customer Confirmed", "Decision", "Reason"]

            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No records match the selected filter criteria.")

        st.markdown("---")

        # CSV Download Option
        col_down, col_clear = st.columns([2, 1])
        with col_down:
            full_df = pd.DataFrame(st.session_state.audit_log)
            csv_buffer = io.StringIO()
            full_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue().encode("utf-8")

            st.download_button(
                label="📥 Download Audit Log as CSV File",
                data=csv_data,
                file_name=f"indigo_agent_gatekeeper_audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_clear:
            if st.button("🗑️ Reset / Clear Audit Log", use_container_width=True):
                st.session_state.audit_log = []
                st.rerun()


# -----------------------------------------------------------------------------
# SECTION 4: SECURITY TEST SUITE
# -----------------------------------------------------------------------------
elif navigation_option == "🧪 Security Test Suite":
    st.subheader("🧪 Automated Security Test Suite")
    st.write(
        "Demonstrate systematic compliance with all 8 security rules defined in the assignment. "
        "Execute automated test cases to evaluate actual vs. expected decisions."
    )

    col_btn, col_stats = st.columns([1, 2])
    with col_btn:
        run_tests_clicked = st.button("▶️ Run All Security Tests", type="primary", use_container_width=True)

    test_results = run_all_security_tests()
    total_tests = len(test_results)
    passed_tests = sum(1 for t in test_results if t["status"] == "PASS")
    failed_tests = total_tests - passed_tests

    with col_stats:
        if passed_tests == total_tests:
            st.success(f"🎉 **{passed_tests}/{total_tests} Tests Passed (100% Security Rule Compliance)**")
        else:
            st.error(f"⚠️ **{failed_tests} Test(s) Failed. Please inspect the rule engine.**")

    st.markdown("---")

    # Render each test case in a structured card
    for tc in test_results:
        with st.container():
            col_icon, col_info, col_dec = st.columns([0.6, 2.5, 1.3])

            with col_icon:
                if tc["status"] == "PASS":
                    st.markdown("""
                        <div style="background-color: #d1e7dd; color: #0f5132; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 14px;">
                            ✅ PASS
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div style="background-color: #f8d7da; color: #842029; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 14px;">
                            ❌ FAIL
                        </div>
                    """, unsafe_allow_html=True)

            with col_info:
                st.markdown(f"**[{tc['test_id']}] {tc['test_name']}**")
                st.caption(f"Governance Policy: *{tc['rule_tested']}*")
                st.write(
                    f"**Inputs:** Agent: `{tc['agent_name']}` ({tc['agent_status']}) | "
                    f"Action: `{tc['action']}` | "
                    f"Amount: ₹{tc['amount_inr']:,.2f} | "
                    f"Customer Confirmed: `{tc['customer_confirmation']}`"
                )
                st.markdown(f"<small style='color: #475569;'>Rationale: {tc['reason']}</small>", unsafe_allow_html=True)

            with col_dec:
                st.write(f"**Expected:** `{tc['expected_decision']}`")
                st.write(f"**Actual:** `{tc['actual_decision']}`")

                # Quick button to load this test into simulator
                if st.button(f"Load into Simulator", key=f"load_{tc['test_id']}"):
                    st.session_state.sim_customer = tc["customer_name"]
                    st.session_state.sim_agent_name = tc["agent_name"]
                    st.session_state.sim_agent_status = tc["agent_status"]
                    st.session_state.sim_action = tc["action"]
                    st.session_state.sim_amount = tc["amount_inr"]
                    st.session_state.sim_confirmation = tc["customer_confirmation"]

                    # Evaluate immediately
                    actual_decision, reason, rule_code = evaluate_security_rule(
                        tc["agent_status"], tc["action"], tc["amount_inr"], tc["customer_confirmation"]
                    )
                    eval_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.last_evaluation = {
                        "timestamp": eval_time,
                        "customer_name": tc["customer_name"],
                        "agent_name": tc["agent_name"],
                        "status": tc["agent_status"],
                        "action": tc["action"],
                        "amount": tc["amount_inr"],
                        "customer_confirmation": tc["customer_confirmation"],
                        "decision": actual_decision,
                        "reason": reason,
                        "rule_code": rule_code
                    }
                    st.info(f"Loaded test case '{tc['test_id']}' into simulator! Switch to the 'Request Simulator' tab to view.")

            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SECTION 5: MBA GOVERNANCE RULES & GUIDE
# -----------------------------------------------------------------------------
elif navigation_option == "📚 Governance Rules & Guide":
    st.subheader("📚 AI Agent Governance & Security Framework")
    st.write(
        "Academic reference and governance blueprint for the IndiGo Agent Gatekeeper project. "
        "Useful for viva questions, report writing, and explaining the strategic necessity of agent firewalls."
    )

    t1, t2, t3 = st.tabs(["🏛️ Strategic Rationale", "📜 The 8 Security Rules", "⚙️ Gatekeeper Architecture"])

    with t1:
        st.markdown("""
        ### Why do Airlines need an AI Agent Gatekeeper?
        As consumer AI agents (like Apple Siri, Google Assistant, OpenAI Operator, and personal booking bots) 
        become autonomous, they begin making financial and operational decisions on behalf of users.

        #### Key Governance Risks:
        1. **Privilege Creep:** Autonomous agents making non-reversible changes (canceling tickets or initiating refunds) without explicit human consent.
        2. **Financial Exploitation:** Agents falling prey to prompt injection or hallucination and purchasing high-value tickets unintentionally.
        3. **Denial of Inventory & Scraping:** Unverified personal bots querying flight routes in bulk, causing server strain and inventory locking.
        4. **Zero-Trust Identity Deficit:** Airlines cannot trust arbitrary API requests claiming to represent a passenger without registered agent verification.

        #### Strategic Solution:
        The **Agent Gatekeeper** enforces a **Human-in-the-Loop (HITL)** governance model. It creates three deterministic decision boundaries:
        - **ALLOW:** Permitted low-risk or verified actions.
        - **ASK CUSTOMER:** Escalation gate requiring step-up human authentication.
        - **BLOCK:** Immediate cessation of high-risk or unauthorized attempts.
        """)

    with t2:
        st.markdown("""
        ### Complete Policy Matrix: 8 Security Rules

        | Rule # | Policy Description | Enforced Decision | Business / Risk Justification |
        | :--- | :--- | :---: | :--- |
        | **Rule 1** | Unknown AI agents must be blocked | `BLOCK` | Zero-Trust: Unvetted bots could be scrapers, vulnerability scanners, or unauthorized delegates. |
        | **Rule 2** | Registered agents can view flight fares without confirmation | `ALLOW` | Informational query: Read-only operations pose zero financial or itinerary risk. |
        | **Rule 3** | Flight bookings require customer confirmation | `ASK CUSTOMER` *(if unconfirmed)* <br>`ALLOW` *(if confirmed)* | Human-in-the-Loop: Ensures the passenger explicitly agrees to dates, flight times, and fare terms. |
        | **Rule 4** | Flight bookings above ₹10,000 must be blocked | `BLOCK` | Financial Risk Ceiling: Autonomous delegates are capped at ₹10,000 to prevent catastrophic unintended debt. |
        | **Rule 5** | Flight changes require customer confirmation | `ASK CUSTOMER` *(if unconfirmed)* <br>`ALLOW` *(if confirmed)* | Operational Integrity: Modifying flight dates carries change fees and schedule disruptions. |
        | **Rule 6** | Flight cancellations require customer confirmation | `ASK CUSTOMER` *(if unconfirmed)* <br>`ALLOW` *(if confirmed)* | Irreversible Risk: Accidental ticket forfeiture causes severe passenger distress and inventory chaos. |
        | **Rule 7** | Refund requests require customer confirmation | `ASK CUSTOMER` *(if unconfirmed)* <br>`ALLOW` *(if confirmed)* | Financial Compliance: Prevents unauthorized account credit drain and ensures proper refund routing. |
        | **Rule 8** | Revoked agents must be blocked from all actions | `BLOCK` | Incident Response: Deprovisioned or rogue agents are immediately rendered inert. |
        """)

    with t3:
        st.markdown("""
        ### Gatekeeper Architectural Flow

        ```text
        [ Personal AI Agent ]
                 │
                 ▼
        ┌─────────────────────────────────────────────────────────┐
        │       IndiGo Agent Gatekeeper Security Filter           │
        ├─────────────────────────────────────────────────────────┤
        │ 1. Identity Verification                                │
        │    - Is Agent Revoked? ──────────> (YES) ──> [ BLOCK ]   │
        │    - Is Agent Unknown? ──────────> (YES) ──> [ BLOCK ]   │
        │                                                         │
        │ 2. Action Classification & Safety Checks                │
        │    - View Fares? ────────────────> (YES) ──> [ ALLOW ]   │
        │    - Booking > ₹10,000? ─────────> (YES) ──> [ BLOCK ]   │
        │                                                         │
        │ 3. Human-in-the-Loop Verification                       │
        │    - Booking <= ₹10k, Change, Cancel, Refund            │
        │      ├─ Customer Confirmed == "Yes" ───────> [ ALLOW ]   │
        │      └─ Customer Confirmed == "No"  ───> [ ASK CUSTOMER ]│
        └─────────────────────────────────────────────────────────┘
                 │
                 ▼
        [ Tamper-Evident Audit Trail (CSV Export) ]
        ```
        """)


# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; color: #64748b; font-size: 13px; padding-bottom: 20px;">
        <strong>IndiGo Airlines AI Agent Gatekeeper Prototype</strong> • Developed for MBA Assignment on AI Governance & Security<br>
        Student: <strong>{st.session_state.student_name}</strong> | Enrollment ID: <strong>{st.session_state.student_enrollment}</strong><br>
        Simulated Environment • No live connections to real IndiGo production systems
    </div>
""", unsafe_allow_html=True)
