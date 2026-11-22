"""
IndiGo Airlines - AI Agent Gatekeeper Security Test Suite
========================================================
Course: MBA in AI Agent Governance and Security
Project: Agent Gatekeeper for IndiGo Airlines

This test suite verifies that the security engine accurately executes all 8 security rules
and validates all governance policies.

Supports execution via:
    python -m unittest test_gatekeeper.py
    python test_gatekeeper.py
"""

import sys
import unittest
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
    evaluate_security_rule,
    get_predefined_test_cases,
    run_all_security_tests,
)


class TestIndiGoAgentGatekeeper(unittest.TestCase):
    """
    Unit test cases for evaluating IndiGo's 8 Core AI Agent Security & Governance Rules.
    """

    def test_rule_1_unknown_agent_blocked(self):
        """Rule 1: Unknown or unregistered AI agents must be blocked from all actions."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_UNKNOWN,
            action=ACTION_VIEW_FARES,
            amount_inr=0.0,
            customer_confirmation="No"
        )
        self.assertEqual(decision, DECISION_BLOCK)
        self.assertEqual(rule_code, "RULE_1_UNKNOWN_AGENT")
        self.assertIn("Unknown", reason)

    def test_rule_2_registered_agent_view_fares_allowed(self):
        """Rule 2: Registered agents can view flight fares without confirmation."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_VIEW_FARES,
            amount_inr=0.0,
            customer_confirmation="No"
        )
        self.assertEqual(decision, DECISION_ALLOW)
        self.assertEqual(rule_code, "RULE_2_VIEW_FARES_AUTONOMOUS")
        self.assertIn("Rule 2", reason)

    def test_rule_3_booking_under_10k_no_confirmation_asks_customer(self):
        """Rule 3: Flight bookings require customer confirmation (No confirmation -> ASK CUSTOMER)."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_BOOK_FLIGHT,
            amount_inr=6500.0,
            customer_confirmation="No"
        )
        self.assertEqual(decision, DECISION_ASK_CUSTOMER)
        self.assertEqual(rule_code, "RULE_3_BOOKING_REQUIRES_CONFIRMATION")
        self.assertIn("Rule 3", reason)

    def test_rule_3_booking_under_10k_with_confirmation_allowed(self):
        """Rule 3: Flight bookings with verified customer confirmation are allowed."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_BOOK_FLIGHT,
            amount_inr=8200.0,
            customer_confirmation="Yes"
        )
        self.assertEqual(decision, DECISION_ALLOW)
        self.assertEqual(rule_code, "RULE_3_BOOKING_CONFIRMED")
        self.assertIn("Rule 3", reason)

    def test_rule_4_booking_over_10k_blocked_even_if_confirmed(self):
        """Rule 4: Autonomous flight bookings above INR 10,000 must be blocked."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_BOOK_FLIGHT,
            amount_inr=15400.0,
            customer_confirmation="Yes"
        )
        self.assertEqual(decision, DECISION_BLOCK)
        self.assertEqual(rule_code, "RULE_4_BOOKING_AMOUNT_LIMIT")
        self.assertIn("Rule 4", reason)

    def test_rule_5_change_flight_no_confirmation_asks_customer(self):
        """Rule 5: Flight changes require customer confirmation (No confirmation -> ASK CUSTOMER)."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_CHANGE_FLIGHT,
            amount_inr=1200.0,
            customer_confirmation="No"
        )
        self.assertEqual(decision, DECISION_ASK_CUSTOMER)
        self.assertEqual(rule_code, "RULE_5_CHANGE_REQUIRES_CONFIRMATION")
        self.assertIn("Rule 5", reason)

    def test_rule_5_change_flight_with_confirmation_allowed(self):
        """Rule 5: Flight changes with verified customer confirmation are allowed."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_CHANGE_FLIGHT,
            amount_inr=1200.0,
            customer_confirmation="Yes"
        )
        self.assertEqual(decision, DECISION_ALLOW)
        self.assertEqual(rule_code, "RULE_5_CHANGE_CONFIRMED")

    def test_rule_6_cancel_flight_no_confirmation_asks_customer(self):
        """Rule 6: Flight cancellations require customer confirmation (No confirmation -> ASK CUSTOMER)."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_CANCEL_FLIGHT,
            amount_inr=0.0,
            customer_confirmation="No"
        )
        self.assertEqual(decision, DECISION_ASK_CUSTOMER)
        self.assertEqual(rule_code, "RULE_6_CANCEL_REQUIRES_CONFIRMATION")
        self.assertIn("Rule 6", reason)

    def test_rule_6_cancel_flight_with_confirmation_allowed(self):
        """Rule 6: Flight cancellations with verified customer confirmation are allowed."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_CANCEL_FLIGHT,
            amount_inr=0.0,
            customer_confirmation="Yes"
        )
        self.assertEqual(decision, DECISION_ALLOW)
        self.assertEqual(rule_code, "RULE_6_CANCEL_CONFIRMED")

    def test_rule_7_refund_request_no_confirmation_asks_customer(self):
        """Rule 7: Refund requests require customer confirmation (No confirmation -> ASK CUSTOMER)."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_REQUEST_REFUND,
            amount_inr=4500.0,
            customer_confirmation="No"
        )
        self.assertEqual(decision, DECISION_ASK_CUSTOMER)
        self.assertEqual(rule_code, "RULE_7_REFUND_REQUIRES_CONFIRMATION")
        self.assertIn("Rule 7", reason)
  
    def test_rule_7_refund_request_with_confirmation_allowed(self):
        """Rule 7: Refund requests with verified customer confirmation are allowed."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REGISTERED,
            action=ACTION_REQUEST_REFUND,
            amount_inr=4500.0,
            customer_confirmation="Yes"
        )
        self.assertEqual(decision, DECISION_ALLOW)
        self.assertEqual(rule_code, "RULE_7_REFUND_CONFIRMED")

    def test_rule_8_revoked_agent_blocked_all_actions(self):
        """Rule 8: Revoked agents must be blocked from all actions."""
        decision, reason, rule_code = evaluate_security_rule(
            agent_status=STATUS_REVOKED,
            action=ACTION_VIEW_FARES,
            amount_inr=0.0,
            customer_confirmation="Yes"
        )
        self.assertEqual(decision, DECISION_BLOCK)
        self.assertEqual(rule_code, "RULE_8_REVOKED_AGENT")
        self.assertIn("Rule 8", reason)

    def test_all_predefined_test_cases_pass(self):
        """Ensure all 9 predefined test cases in the test suite pass with 100% compliance."""
        results = run_all_security_tests()
        for res in results:
            self.assertEqual(
                res["actual_decision"],
                res["expected_decision"],
                f"Mismatch in test {res['test_id']} ({res['test_name']}): expected {res['expected_decision']} but got {res['actual_decision']}"
            )
            self.assertEqual(res["status"], "PASS")


def print_banner():
    print("=" * 75)
    print("   ✈️  INDIGO AIRLINES - AI AGENT GATEKEEPER SECURITY TEST SUITE")
    print("   Course: MBA AI Agent Governance & Security")
    print("=" * 75)


def main():
    print_banner()
    print("\nRunning automated security verification across all 8 governance rules...\n")

    results = run_all_security_tests()
    all_passed = True

    for res in results:
        status_symbol = "✅ PASS" if res["status"] == "PASS" else "❌ FAIL"
        if res["status"] != "PASS":
            all_passed = False

        print(f"[{res['test_id']}] {res['test_name']}")
        print(f"       Policy  : {res['rule_tested']}")
        print(f"       Inputs  : Agent='{res['agent_name']}' ({res['agent_status']}), Action='{res['action']}', Amount=INR {res['amount_inr']:,.2f}, Confirmed='{res['customer_confirmation']}'")
        print(f"       Expected: {res['expected_decision']} | Actual: {res['actual_decision']}  ->  {status_symbol}")
        print(f"       Reason  : {res['reason']}")
        print("-" * 75)

    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["status"] == "PASS")

    print("\n" + "=" * 75)
    print(f"TEST SUMMARY: {passed_tests}/{total_tests} Tests Passed ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 75)

    if all_passed:
        print("\n🎉 SUCCESS: All security policies passed with 100% compliance!")
        return 0
    else:
        print("\n⚠️ WARNING: One or more security tests failed. Please review the rules.")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--unittest":
        unittest.main(argv=[sys.argv[0]])
    else:
        sys.exit(main())
