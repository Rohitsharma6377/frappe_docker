import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, add_days
import re


class LeadPlus(Document):
    def validate(self):
        self.validate_contact()
        self.auto_assign()

    def validate_contact(self):
        # basic phone validation
        if self.phone:
            digits = re.sub(r"\D", "", self.phone)
            if len(digits) < 7:
                frappe.throw("Phone number looks invalid")

        # basic email validation
        if self.email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
                frappe.throw("Email looks invalid")

    def auto_assign(self):
        # If not assigned, pick first available CRM User or any enabled user as fallback
        if not self.assigned_to:
            assigned = None
            users = frappe.get_all("Has Role", filters={"role": "CRM User"}, fields=["parent"]) or []
            if users:
                assigned = users[0].parent
            else:
                u = frappe.get_all("User", filters={"enabled": 1}, fields=["name"], limit=1)
                if u:
                    assigned = u[0].name
            if assigned:
                self.assigned_to = assigned


def create_default_followup(doc, method=None):
    """
    Create a default follow-up 2 days after lead creation.
    Called via hook after_insert
    """
    try:
        from frappe.utils import add_days

        fu = frappe.new_doc("Follow Up")
        fu.reference_type = "Lead Plus"
        fu.reference_name = doc.name
        fu.follow_up_date = add_days(frappe.utils.nowdate(), 2)
        fu.assigned_to = doc.assigned_to or frappe.session.user
        fu.status = "Pending"
        fu.insert(ignore_permissions=True)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "create_default_followup")
