import frappe
from frappe.model.document import Document


STAGE_PROBABILITY = {
    "Prospecting": 10,
    "Negotiation": 60,
    "Won": 100,
    "Lost": 0
}


class OpportunityPlus(Document):
    def validate(self):
        self.ensure_probability()
        self.prevent_closing_without_customer()

    def ensure_probability(self):
        # set probability based on stage if not manually set
        if self.stage in STAGE_PROBABILITY:
            self.probability = STAGE_PROBABILITY[self.stage]

    def prevent_closing_without_customer(self):
        if self.stage == "Won" and not self.customer:
            frappe.throw("Cannot mark Opportunity as Won without a linked Customer")
