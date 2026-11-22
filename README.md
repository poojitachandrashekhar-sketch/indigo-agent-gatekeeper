# ✈️ Agent Gatekeeper for IndiGo Airlines
### Permission-Based AI Agent Governance and Security Prototype (AI Firewall)
**Course:** MBA in AI Agent Governance and Security  
**Academic Simulation Project**  
**Simulated Enterprise:** InterGlobe Aviation Limited (IndiGo Airlines)

---

## 🎓 Student Details
- **Student Name:** `[ENTER YOUR NAME]`
- **Enrollment Number:** `[ENTER YOUR ENROLLMENT NUMBER]`
- **Academic Course:** MBA - AI Agent Governance and Security
- **Specialization:** Enterprise Technology Strategy & AI Governance

---

## 📌 Project Overview
As generative AI evolves, consumer technology is rapidly transitioning from passive chatbots to autonomous **Personal AI Agents** (such as Apple Siri, Google Assistant, OpenAI Operator, and bespoke travel bots). These personal agents act on behalf of passengers to research flights, modify bookings, cancel itineraries, and purchase tickets.

The **Agent Gatekeeper for IndiGo Airlines** is a specialized, permission-based governance and security system designed to act as an **AI Firewall** between external personal AI agents and IndiGo's core reservation systems. It inspects incoming agent transactions in real time, applies 8 strict governance rules, and deterministically outputs one of three decisions:
- 🟢 **`ALLOW`**: The transaction is verified or low-risk and proceeds to airline systems.
- 🟡 **`ASK CUSTOMER`**: The action is sensitive or financial and requires explicit Human-in-the-Loop (HITL) confirmation.
- 🔴 **`BLOCK`**: The transaction violates security policy or exceeds authorized spending ceilings and is halted immediately.

---

## 🚨 Problem Statement
While autonomous AI agents bring unprecedented convenience to travelers, they introduce critical vulnerabilities to airlines:
1. **Unchecked Agent Autonomy:** Without governance, an autonomous agent could misunderstand a user's prompt or hallucinate, booking unwanted flights or non-refundable tickets.
2. **Irreversible Itinerary Destruction:** Malfunctioning or unauthorized agents could cancel flights or request premature refunds, leaving travelers stranded.
3. **Severe Financial Exposure:** An agent compromised by prompt injection or runaway loops could exhaust a passenger's credit limit.
4. **Zero-Trust Identity Deficit:** Open airline APIs cannot distinguish between certified passenger assistants, malicious scraper bots, and revoked delegates.

---

## 🏢 Why AI Agent Governance is Crucial for an Airline (IndiGo Context)
IndiGo Airlines is India's largest passenger airline, renowned for operational punctuality, high passenger volumes (over 300,000 travelers daily), and lean operational costs. 

In this high-volume, low-margin environment:
- **Perishable Inventory:** Airline seats cannot be recovered once a flight departs. Uncontrolled agent booking or cancellation churn degrades seat availability for genuine flyers.
- **Customer Trust & Brand Equity:** Disputed transactions caused by rogue AI agents erode passenger trust and increase customer support overhead.
- **Regulatory Alignment:** Emerging AI regulations (e.g., EU AI Act, India's DPDP Act) require commercial enterprises to enforce accountability, data protection, and explicit human consent for autonomous automated actions.

---

## 🎯 Project Objectives
1. **Zero-Trust Identity Enforcement:** Ensure only certified, registered personal AI agents can communicate with IndiGo services.
2. **Autonomous Spending Capping:** Enforce a hard ₹10,000 ceiling on autonomous transactions to prevent catastrophic financial loss.
3. **Human-in-the-Loop (HITL) Gating:** Require verified passenger confirmation for all high-impact actions (bookings, changes, cancellations, refunds).
4. **Agent Lifecycle Control:** Provide immediate revocation capabilities to de-authorize rogue or compromised agents with timestamp tracking.
5. **Regulatory Auditability:** Maintain a real-time, tamper-evident audit log exportable to CSV for compliance and dispute resolution.

---

## 💡 Proposed Solution: The IndiGo Agent Gatekeeper
The Agent Gatekeeper operates as an intelligent policy decision point (PDP) positioned between external AI agents and IndiGo's booking engines.

```text
       [ Personal AI Agent ] (Siri, Google, Custom Bot)
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│          ✈️ INDIGO AGENT GATEKEEPER SECURITY ENGINE          │
├─────────────────────────────────────────────────────────────┤
│ 1. Identity & Lifecycle Check                               │
│    - Is agent Revoked? ──────────────> YES ───> [ BLOCK ]   │
│    - Is agent Unknown/Unregistered? ──> YES ───> [ BLOCK ]   │
│                                                             │
│ 2. Read-Only Query Inspection                               │
│    - Is action "View Fares"? ─────────> YES ───> [ ALLOW ]   │
│                                                             │
│ 3. Financial Ceiling Check                                  │
│    - Booking Amount > ₹10,000? ───────> YES ───> [ BLOCK ]   │
│                                                             │
│ 4. Human-in-the-Loop (HITL) Verification                    │
│    - Actions: Booking <= ₹10k, Change, Cancel, Refund       │
│      ├── Customer Confirmed == "Yes"  ─────────> [ ALLOW ]   │
│      └── Customer Confirmed == "No"   ───> [ ASK CUSTOMER ] │
└─────────────────────────────────────────────────────────────┘
                 │
                 ▼
   [ Immutable Audit Log & CSV Export ]
```

---

## ⚖️ The 8 Core Governance Rules

| Rule # | Security Policy | Decision | Business & Governance Justification |
| :---: | :--- | :---: | :--- |
| **Rule 1** | Unknown AI agents must be blocked | `BLOCK` | **Zero-Trust Baseline:** Unregistered or unverified personal agents are denied access to airline endpoints. |
| **Rule 2** | Registered agents can view flight fares without confirmation | `ALLOW` | **Read-Only Privilege:** Informational queries carry zero financial or itinerary risk and can run autonomously. |
| **Rule 3** | Flight bookings require customer confirmation | `ASK CUSTOMER` *(if unconfirmed)*<br>`ALLOW` *(if confirmed)* | **Human-in-the-Loop:** Eliminates accidental or hallucinated bookings by requiring explicit passenger consent. |
| **Rule 4** | Flight bookings above ₹10,000 must be blocked | `BLOCK` | **Financial Risk Ceiling:** Protects passenger bank accounts from high-value unintended debits. |
| **Rule 5** | Flight changes require customer confirmation | `ASK CUSTOMER` *(if unconfirmed)*<br>`ALLOW` *(if confirmed)* | **Operational Stability:** Date and time modifications trigger fare differences and potential change fees. |
| **Rule 6** | Flight cancellations require customer confirmation | `ASK CUSTOMER` *(if unconfirmed)*<br>`ALLOW` *(if confirmed)* | **Irreversible Action:** Prevents catastrophic accidental ticket forfeiture and travel disruption. |
| **Rule 7** | Refund requests require customer confirmation | `ASK CUSTOMER` *(if unconfirmed)*<br>`ALLOW` *(if confirmed)* | **Financial Integrity:** Ensures funds are routed to the proper source and prevents unauthorized redemption. |
| **Rule 8** | Revoked agents must be blocked from all actions | `BLOCK` | **Incident Response:** Any agent whose trust is revoked is immediately denied access with zero bypass. |

---

## 🌟 Key Application Features

1. **Executive Dashboard & Airline Branding:**
   - Designed with IndiGo's corporate colors: Navy Blue (`#001b69`), Corporate Blue (`#002e8a`), Sky Blue (`#e8f2fe`), and White (`#ffffff`).
   - Dynamic Student Details banner displaying Name and Enrollment Number with live sidebar editing.
2. **Interactive Request Simulator:**
   - Multi-parameter payload testing: Customer Name, AI Agent, Status, Action, Amount (₹), and Confirmation.
   - Real-time decision banner displaying `ALLOW`, `ASK CUSTOMER`, or `BLOCK` with explicit policy justifications.
3. **Agent Registry & Revocation Management:**
   - Register new personal agents with certified ecosystem providers.
   - Instantly revoke agent access with automatic date & time timestamping.
   - View summary metrics: Total Agents, Active Agents, and Revoked Agents.
4. **Tamper-Evident Audit Trail:**
   - Chronological logging of all simulated requests with timestamps.
   - Filter by decision (`ALLOW`, `ASK CUSTOMER`, `BLOCK`) or search by passenger/agent name.
   - **Download Audit Log as CSV:** One-click compliance export.
5. **Automated Security Test Suite:**
   - Pre-configured test suite verifying all 8 governance rules.
   - Real-time `PASS / FAIL` status indicators with 100% verified compliance.
   - One-click "Load into Simulator" to demonstrate individual test scenarios.
6. **Academic Governance & Strategy Guide:**
   - In-app reference covering AI agent architecture, OWASP LLM/Agent top risks, and enterprise governance frameworks.

---

## 🛠️ Technology Stack
- **Programming Language:** Python 3.11+
- **Web UI Framework:** Streamlit 1.35+
- **Data Analytics & Export:** Pandas 2.0+
- **Unit Testing Framework:** Python Standard Library `unittest`
- **Operating Environment:** Windows 10 / 11 (Local laptop execution)

---

## 💻 Installation & Setup Instructions (Windows)

### Prerequisites
- Python 3.11 or higher installed on your laptop.

### Quick Start: Method 1 (One-Click Windows Launcher)
1. Open this project folder in Windows File Explorer:
   `c:\Users\POOJITA\Desktop\IndiGo-Agent-Gatekeeper`
2. Double-click the file named **`run_app.bat`**.
3. The launcher will automatically find Python, initialize Streamlit, and open your browser at:
   ```
   http://localhost:8501
   ```

### Method 2: Manual Terminal Execution
1. Open PowerShell or Command Prompt in the project folder:
   ```powershell
   cd c:\Users\POOJITA\Desktop\IndiGo-Agent-Gatekeeper
   ```
2. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Launch the Streamlit application:
   ```powershell
   streamlit run app.py
   ```
   *(Or: `python -m streamlit run app.py`)*

---

## 🧪 How to Run Automated Tests

The prototype includes both graphical and command-line test runners.

### Option A: Standard Python Unittest Runner
Run the official automated test suite via the command line:
```powershell
python -m unittest test_gatekeeper.py -v
```

Expected Output:
```text
test_all_predefined_test_cases_pass ... ok
test_rule_1_unknown_agent_blocked ... ok
test_rule_2_registered_agent_view_fares_allowed ... ok
test_rule_3_booking_under_10k_no_confirmation_asks_customer ... ok
test_rule_3_booking_under_10k_with_confirmation_allowed ... ok
test_rule_4_booking_over_10k_blocked_even_if_confirmed ... ok
test_rule_5_change_flight_no_confirmation_asks_customer ... ok
test_rule_5_change_flight_with_confirmation_allowed ... ok
test_rule_6_cancel_flight_no_confirmation_asks_customer ... ok
test_rule_6_cancel_flight_with_confirmation_allowed ... ok
test_rule_7_refund_request_no_confirmation_asks_customer ... ok
test_rule_7_refund_request_with_confirmation_allowed ... ok
test_rule_8_revoked_agent_blocked_all_actions ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.001s

OK
```

### Option B: Executive Test Runner
Run the custom formatted test runner:
```powershell
python test_gatekeeper.py
```

### Option C: In-App Test Suite
Navigate to the **🧪 Security Test Suite** tab inside the Streamlit web dashboard and click **▶️ Run All Security Tests**.

---

## 📊 Predefined Test Cases & Verified Results

| Test ID | Scenario Tested | Policy Evaluated | Inputs (Status, Action, Amount, Confirmed) | Expected | Actual | Status |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **TC-01** | Unknown Agent Booking Attempt | Rule 1 | Unknown, View Fares, ₹0, No | `BLOCK` | `BLOCK` | ✅ **PASS** |
| **TC-02** | Registered Agent View Fares | Rule 2 | Registered, View Fares, ₹0, No | `ALLOW` | `ALLOW` | ✅ **PASS** |
| **TC-03** | Booking $\le$ ₹10k without Confirmation | Rule 3 | Registered, Book Flight, ₹6,500, No | `ASK CUSTOMER` | `ASK CUSTOMER` | ✅ **PASS** |
| **TC-04** | Booking $\le$ ₹10k with Confirmation | Rule 3 | Registered, Book Flight, ₹8,200, Yes | `ALLOW` | `ALLOW` | ✅ **PASS** |
| **TC-05** | High-Value Booking $>$ ₹10,000 | Rule 4 | Registered, Book Flight, ₹15,400, Yes | `BLOCK` | `BLOCK` | ✅ **PASS** |
| **TC-06** | Flight Change without Confirmation | Rule 5 | Registered, Change Flight, ₹1,200, No | `ASK CUSTOMER` | `ASK CUSTOMER` | ✅ **PASS** |
| **TC-07** | Flight Cancellation without Confirmation | Rule 6 | Registered, Cancel Flight, ₹0, No | `ASK CUSTOMER` | `ASK CUSTOMER` | ✅ **PASS** |
| **TC-08** | Refund Request with Confirmation | Rule 7 | Registered, Request Refund, ₹4,500, Yes | `ALLOW` | `ALLOW` | ✅ **PASS** |
| **TC-09** | Revoked Agent Attempting Interaction | Rule 8 | Revoked, View Fares, ₹0, Yes | `BLOCK` | `BLOCK` | ✅ **PASS** |

**Verified Test Compliance: 100% (All scenarios pass with zero discrepancies).**

---

## 📋 Audit Log & Compliance Accountability
The gatekeeper enforces complete traceability:
- Every evaluated request creates an immutable record in `st.session_state.audit_log`.
- Log records include timestamp, passenger name, agent identifier, action type, transaction value (₹), human confirmation status, deterministic decision, and explicit policy justification.
- Compliance officers can export the full log to CSV format using the **📥 Download Audit Log as CSV** button.
- A pre-seeded sample log is preserved in `documentation/sample_audit_log.csv`.

---

## 📈 Strategic Business Benefits for IndiGo Airlines
1. **Risk Containment:** Hard financial caps eliminate large accidental debits caused by agent hallucination or prompt injection.
2. **Passenger Sovereignty:** Explicit confirmation gates ensure travelers maintain full decision-making control over their travel plans.
3. **Operational Stability:** Autonomous query access (Rule 2) enables efficient agent shopping while blocking bot-driven seat inventory hoarding.
4. **Audit Readiness:** Comprehensive transaction logging ensures compliance with airline consumer protection frameworks.

---

## ⚠️ Limitations & Future Enhancements

### Current Limitations
- **Academic Simulation:** Designed as a standalone prototype for MBA coursework; does not link to live IndiGo flight databases or real credit card payment processors.
- **Session-Based Storage:** Uses Streamlit session state and in-memory persistence rather than an external distributed database.
- **Rule-Based Evaluation:** Employs deterministic rule engines rather than cryptographic identity verification (e.g., OAuth 2.0 / mTLS).

### Future Roadmap
1. **Cryptographic Agent Attestation:** Integration of decentralized identities (DIDs) and OAuth 2.0 mutual attestation for personal agents.
2. **AI Anomaly Detection:** Machine learning monitoring to detect abnormal booking velocity or suspicious booking patterns.
3. **Biometric Human-in-the-Loop:** Step-up facial or fingerprint authentication directly from the passenger's mobile device when `ASK CUSTOMER` is triggered.
4. **Multi-Carrier Alliance Standards:** Standardizing agent governance protocols across Star Alliance and SkyTeam partner airlines.

---

## ⚖️ Academic Disclaimer
> **IMPORTANT NOTICE:** This project is an academic simulation created solely for the purpose of completing an MBA assignment on AI Agent Governance and Security. It is **not** an official application of InterGlobe Aviation Limited (IndiGo Airlines), is **not** connected to live production booking systems, and does **not** process real passenger data or financial transactions.
## Governance Decisions

The Agent Gatekeeper uses three security decisions:

- ALLOW: Permits authorized requests that follow governance policies.
- ASK CUSTOMER: Requires explicit customer confirmation for sensitive actions.
- BLOCK: Rejects unauthorized, revoked, or high-risk requests.

## Security Policies

1. Unknown agents cannot access airline services.
2. Registered agents can perform permitted activities.
3. Flight bookings require customer confirmation.
4. Transactions exceeding ₹10,000 are blocked.
5. Revoked agents cannot perform any actions.
6. All security decisions are recorded in the audit log.

## Testing

The prototype was tested using authorized requests, unauthorized agents, revoked agents, missing customer confirmation, and transactions exceeding the permitted limit.
