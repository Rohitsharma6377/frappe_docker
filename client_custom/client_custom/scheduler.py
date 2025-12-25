import frappe


def daily_followups():
    """Daily scheduled job: mark overdue follow-ups and notify assigned users."""
    try:
        frappe.get_doc("Follow Up")
    except Exception:
        # If doctype missing, skip
        return

    try:
        from client_custom.client_custom.doctype.follow_up.follow_up import mark_overdue_and_notify

        mark_overdue_and_notify()
    except Exception:
        frappe.log_error(frappe.get_traceback(), "client_custom.daily_followups")
