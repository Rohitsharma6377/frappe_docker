import frappe
from frappe.model.document import Document # type: ignore
from frappe.utils import getdate, nowdate


class FollowUp(Document):
    def on_update(self):
        # Ensure assigned_to set
        if not self.assigned_to:
            self.assigned_to = frappe.session.user


def mark_overdue_and_notify():
    """Find overdue follow-ups and mark as Missed and notify assigned user."""
    overdue = frappe.get_all(
        "Follow Up",
        filters={"status": "Pending", "follow_up_date": ["<", nowdate()]},
        fields=["name", "assigned_to", "reference_type", "reference_name", "follow_up_date"],
    )
    for f in overdue:
        try:
            doc = frappe.get_doc("Follow Up", f.name)
            doc.status = "Missed"
            doc.save(ignore_permissions=True)
            frappe.sendmail(
                recipients=[doc.assigned_to],
                subject=f"Follow-up missed: {doc.reference_name}",
                message=f"Your follow-up for {doc.reference_type} {doc.reference_name} scheduled on {doc.follow_up_date} is marked Missed.",
            )
        except Exception:
            frappe.log_error(frappe.get_traceback(), "mark_overdue_and_notify")
