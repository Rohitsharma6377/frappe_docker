app_name = "client_custom"
app_title = "Client Custom"
app_publisher = "You"
app_description = "Custom CRM app built on Frappe + ERPNext"
app_icon = "octicon octicon-organization"
app_color = "grey"
app_email = "you@example.com"
app_license = "MIT"

# Scheduler: daily job to mark missed follow-ups and notify users
scheduler_events = {
    "daily": [
        "client_custom.client_custom.scheduler.daily_followups"
    ]
}

# Hooks: run after insert on Lead Plus to create default follow-up
doc_events = {
    "Lead Plus": {
        "after_insert": "client_custom.client_custom.doctype.lead_plus.lead_plus.create_default_followup"
    }
}

# Fixtures (roles/workflows) can be exported and added here later
fixtures = [
    "Role",
    "Workflow",
    "Workflow State",
    "Workflow Action"
]
