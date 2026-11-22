"""
IndiGo Airlines - AI Agent Gatekeeper Security Engine
=====================================================
Course: MBA in AI Agent Governance and Security
Project: Agent Gatekeeper for IndiGo Airlines

This module contains the core governance and security evaluation rules
that govern personal AI agents interacting with IndiGo's airline services.
"""

from datetime import datetime
from typing import Dict, Any, List, Tuple

# Security Decisions Defined by Policy
DECISION_ALLOW = "ALLOW"
DECISION_ASK_CUSTOMER = "ASK CUSTOMER"
DECISION_BLOCK = "BLOCK"

# Maximum financial threshold for autonomous agent booking without human escalation
MAX_AUTONOMOUS_BOOKING_AMOUNT_INR = 10000.0

# Registered Actions Supported by IndiGo Gatekeeper
ACTION_VIEW_FARES = "View Fares"
ACTION_BOOK_FLIGHT = "Book Flight"
ACTION_CHANGE_FLIGHT = "Change Flight"
ACTION_CANCEL_FLIGHT = "Cancel Flight"
ACTION_REQUEST_REFUND = "Request Refund"

ALL_ACTIONS = [
    ACTION_VIEW_FARES,
    ACTION_BOOK_FLIGHT,
    ACTION_CHANGE_FLIGHT,
    ACTION_CANCEL_FLIGHT,
    ACTION_REQUEST_REFUND
]

# Agent Status Definitions
STATUS_REGISTERED = "Registered"
STATUS_UNKNOWN = "Unknown"
STATUS_REVOKED = "Revoked"


def evaluate_security_rule(
    agent_status: str,
    action: str,
    amount_inr: float,
    customer_confirmation: str
) -> Tuple[str, str, str]:
    """
    Evaluates an incoming request from a personal AI agent against IndiGo's
    8 Core Security & Governance Rules.

    Parameters:
        agent_status (str): "Registered", "Unknown", or "Revoked"
        action (str): "View Fares", "Book Flight", "Change Flight", "Cancel Flight", "Request Refund"
        amount_inr (float): Monetary value in INR for the transaction
        customer_confirmation (str): "Yes" or "No"

    Returns:
        tuple: (decision, reason, rule_code)
               decision is one of 'ALLOW', 'ASK CUSTOMER', 'BLOCK'
               reason provides clear audit justification
               rule_code identifies the specific security rule enforced
    """
    # Normalize inputs
    status = (agent_status or "").strip()
    act = (action or "").strip()
    conf = (customer_confirmation or "").strip().capitalize()
    is_confirmed = (conf == "Yes")
    amount = float(amount_inr) if amount_inr is not None else 0.0

    # -------------------------------------------------------------------------
    # RULE 8: Revoked agents must be blocked from all actions
    # -------------------------------------------------------------------------
    if status == STATUS_REVOKED:
        return (
            DECISION_BLOCK,
            "Security Rule 8: Agent authorization has been REVOKED. All interactions with IndiGo systems are prohibited.",
            "RULE_8_REVOKED_AGENT"
        )

    # -------------------------------------------------------------------------
    # RULE 1: Unknown AI agents must be blocked
    # -------------------------------------------------------------------------
    if status == STATUS_UNKNOWN:
        return (
            DECISION_BLOCK,
            "Security Rule 1: Unknown / unregistered AI agent detected. Personal agents must be vetted and registered before accessing IndiGo APIs.",
            "RULE_1_UNKNOWN_AGENT"
        )

    # If the agent is not Registered at this point, reject as safe default
    if status != STATUS_REGISTERED:
        return (
            DECISION_BLOCK,
            f"Security Exception: Unrecognized agent status '{status}'. Request blocked by default fail-safe policy.",
            "RULE_GENERIC_SAFETY"
        )

    # =========================================================================
    # ACTIONS FOR REGISTERED AGENTS
    # =========================================================================

    # -------------------------------------------------------------------------
    # RULE 2: Registered agents can view flight fares without confirmation
    # -------------------------------------------------------------------------
    if act == ACTION_VIEW_FARES:
        return (
            DECISION_ALLOW,
            "Security Rule 2: Registered agents are permitted to view flight schedules and fares autonomously (read-only informational query).",
            "RULE_2_VIEW_FARES_AUTONOMOUS"
        )

    # -------------------------------------------------------------------------
    # RULE 4: Flight bookings above ₹10,000 must be blocked
    # RULE 3: Flight bookings require customer confirmation (if <= ₹10,000)
    # -------------------------------------------------------------------------
    if act == ACTION_BOOK_FLIGHT:
        # Check financial cap first
        if amount > MAX_AUTONOMOUS_BOOKING_AMOUNT_INR:
            return (
                DECISION_BLOCK,
                f"Security Rule 4: Flight booking amount of ₹{amount:,.2f} exceeds the allowed autonomous agent ceiling of ₹{MAX_AUTONOMOUS_BOOKING_AMOUNT_INR:,.2f}. Blocked to protect customer from unauthorized large debit.",
                "RULE_4_BOOKING_AMOUNT_LIMIT"
            )

        # Under the threshold: check human confirmation
        if is_confirmed:
            return (
                DECISION_ALLOW,
                f"Security Rule 3: Flight booking for ₹{amount:,.2f} is within limit and customer confirmation is verified.",
                "RULE_3_BOOKING_CONFIRMED"
            )
        else:
            return (
                DECISION_ASK_CUSTOMER,
                f"Security Rule 3: Flight booking requires explicit customer confirmation. Agent must prompt customer for approval.",
                "RULE_3_BOOKING_REQUIRES_CONFIRMATION"
            )

    # -------------------------------------------------------------------------
    # RULE 5: Flight changes require customer confirmation
    # -------------------------------------------------------------------------
    if act == ACTION_CHANGE_FLIGHT:
        if is_confirmed:
            return (
                DECISION_ALLOW,
                "Security Rule 5: Flight modification authorized with verified customer confirmation.",
                "RULE_5_CHANGE_CONFIRMED"
            )
        else:
            return (
                DECISION_ASK_CUSTOMER,
                "Security Rule 5: Flight changes require explicit customer confirmation. Agent must request confirmation before altering flight itinerary.",
                "RULE_5_CHANGE_REQUIRES_CONFIRMATION"
            )

    # -------------------------------------------------------------------------
    # RULE 6: Flight cancellations require customer confirmation
    # -------------------------------------------------------------------------
    if act == ACTION_CANCEL_FLIGHT:
        if is_confirmed:
            return (
                DECISION_ALLOW,
                "Security Rule 6: Flight cancellation authorized with verified customer confirmation.",
                "RULE_6_CANCEL_CONFIRMED"
            )
        else:
            return (
                DECISION_ASK_CUSTOMER,
                "Security Rule 6: Flight cancellation requires explicit customer confirmation to prevent accidental itinerary loss. Prompt customer for approval.",
                "RULE_6_CANCEL_REQUIRES_CONFIRMATION"
            )

    # -------------------------------------------------------------------------
    # RULE 7: Refund requests require customer confirmation
    # -------------------------------------------------------------------------
    if act == ACTION_REQUEST_REFUND:
        if is_confirmed:
            return (
                DECISION_ALLOW,
                "Security Rule 7: Refund request authorized with verified customer confirmation.",
                "RULE_7_REFUND_CONFIRMED"
            )
        else:
            return (
                DECISION_ASK_CUSTOMER,
                "Security Rule 7: Refund request requires explicit customer confirmation. Agent must confirm banking/refund route with customer.",
                "RULE_7_REFUND_REQUIRES_CONFIRMATION"
            )

    # Fallback for unrecognized action
    return (
        DECISION_BLOCK,
        f"Security Warning: Unknown action '{act}'. Blocked by gatekeeper zero-trust policy.",
        "RULE_UNKNOWN_ACTION"
    )


def get_predefined_test_cases() -> List[Dict[str, Any]]:
    """
    Returns a comprehensive suite of predefined test cases covering
    all 8 security governance rules as required by the assignment.
    """
    return [
        {
            "id": "TC-01",
            "name": "Unknown Agent Booking Attempt",
            "rule": "Rule 1: Unknown agents must be blocked",
            "customer_name": "Rohan Verma",
            "agent_name": "ShadowBot_v3",
            "agent_status": STATUS_UNKNOWN,
            "action": ACTION_VIEW_FARES,
            "amount_inr": 0.0,
            "customer_confirmation": "No",
            "expected_decision": DECISION_BLOCK,
            "description": "An unregistered personal AI agent attempts to query IndiGo fares."
        },
        {
            "id": "TC-02",
            "name": "Registered Agent Views Fares (Autonomous)",
            "rule": "Rule 2: Registered agents view fares without confirmation",
            "customer_name": "Ananya Sen",
            "agent_name": "IndiGo TravelBuddy",
            "agent_status": STATUS_REGISTERED,
            "action": ACTION_VIEW_FARES,
            "amount_inr": 0.0,
            "customer_confirmation": "No",
            "expected_decision": DECISION_ALLOW,
            "description": "Registered agent views fares autonomously without human intervention."
        },
        {
            "id": "TC-03",
            "name": "Booking Under ₹10k Without Confirmation",
            "rule": "Rule 3: Flight bookings require customer confirmation",
            "customer_name": "Vikram Patel",
            "agent_name": "Siri Flight Concierge",
            "agent_status": STATUS_REGISTERED,
            "action": ACTION_BOOK_FLIGHT,
            "amount_inr": 6500.0,
            "customer_confirmation": "No",
            "expected_decision": DECISION_ASK_CUSTOMER,
            "description": "Agent tries to auto-book a flight for ₹6,500 without customer confirmation."
        },
        {
            "id": "TC-04",
            "name": "Booking Under ₹10k With Customer Confirmation",
            "rule": "Rule 3: Flight bookings require customer confirmation",
            "customer_name": "Pooja Mehta",
            "agent_name": "MakeMyTrip AI",
            "agent_status": STATUS_REGISTERED,
            "action": ACTION_BOOK_FLIGHT,
            "amount_inr": 8200.0,
            "customer_confirmation": "Yes",
            "expected_decision": DECISION_ALLOW,
            "description": "Agent books a flight for ₹8,200 with customer confirmation verified."
        },
        {
            "id": "TC-05",
            "name": "High-Value Booking Above ₹10,000",
            "rule": "Rule 4: Flight bookings above ₹10,000 must be blocked",
            "customer_name": "Rajesh Nair",
            "agent_name": "IndiGo TravelBuddy",
            "agent_status": STATUS_REGISTERED,
            "action": ACTION_BOOK_FLIGHT,
            "amount_inr": 15400.0,
            "customer_confirmation": "Yes",
            "expected_decision": DECISION_BLOCK,
            "description": "Agent attempts booking of ₹15,400 (exceeds ₹10k threshold even if confirmed)."
        },
        {
            "id": "TC-06",
            "name": "Flight Modification Without Confirmation",
            "rule": "Rule 5: Flight changes require customer confirmation",
            "customer_name": "Sneha Iyer",
            "agent_name": "Google Assistant Agent",
            "agent_status": STATUS_REGISTERED,
            "action": ACTION_CHANGE_FLIGHT,
            "amount_inr": 1200.0,
            "customer_confirmation": "No",
            "expected_decision": DECISION_ASK_CUSTOMER,
            "description": "Agent attempts to modify flight departure date without asking customer."
        },
        {
            "id": "TC-07",
            "name": "Flight Cancellation Without Confirmation",
            "rule": "Rule 6: Flight cancellations require customer confirmation",
            "customer_name": "Amitabh Roy",
            "agent_name": "IndiGo TravelBuddy",
            "agent_status": STATUS_REGISTERED,
            "action": ACTION_CANCEL_FLIGHT,
            "amount_inr": 0.0,
            "customer_confirmation": "No",
            "expected_decision": DECISION_ASK_CUSTOMER,
            "description": "Agent triggers flight cancellation without explicit customer authorization."
        },
        {
            "id": "TC-08",
            "name": "Refund Request With Customer Confirmation",
            "rule": "Rule 7: Refund requests require customer confirmation",
            "customer_name": "Divya Rao",
            "agent_name": "Siri Flight Concierge",
            "agent_status": STATUS_REGISTERED,
            "action": ACTION_REQUEST_REFUND,
            "amount_inr": 4500.0,
            "customer_confirmation": "Yes",
            "expected_decision": DECISION_ALLOW,
            "description": "Agent requests ₹4,500 refund after customer explicitly verified the request."
        },
        {
            "id": "TC-09",
            "name": "Revoked Agent Attempting Any Action",
            "rule": "Rule 8: Revoked agents must be blocked from all actions",
            "customer_name": "Karan Kapoor",
            "agent_name": "CompromisedScraperBot",
            "agent_status": STATUS_REVOKED,
            "action": ACTION_VIEW_FARES,
            "amount_inr": 0.0,
            "customer_confirmation": "Yes",
            "expected_decision": DECISION_BLOCK,
            "description": "A revoked rogue agent attempts even a read-only fare lookup; must be blocked."
        }
    ]


def run_all_security_tests() -> List[Dict[str, Any]]:
    """
    Executes the predefined test cases against evaluate_security_rule()
    and returns comprehensive test results including pass/fail status.
    """
    test_cases = get_predefined_test_cases()
    results = []

    for tc in test_cases:
        actual_decision, reason, rule_code = evaluate_security_rule(
            agent_status=tc["agent_status"],
            action=tc["action"],
            amount_inr=tc["amount_inr"],
            customer_confirmation=tc["customer_confirmation"]
        )

        passed = (actual_decision == tc["expected_decision"])

        results.append({
            "test_id": tc["id"],
            "test_name": tc["name"],
            "rule_tested": tc["rule"],
            "customer_name": tc["customer_name"],
            "agent_name": tc["agent_name"],
            "agent_status": tc["agent_status"],
            "action": tc["action"],
            "amount_inr": tc["amount_inr"],
            "customer_confirmation": tc["customer_confirmation"],
            "expected_decision": tc["expected_decision"],
            "actual_decision": actual_decision,
            "status": "PASS" if passed else "FAIL",
            "reason": reason,
            "rule_code": rule_code,
            "description": tc["description"]
        })

    return results
