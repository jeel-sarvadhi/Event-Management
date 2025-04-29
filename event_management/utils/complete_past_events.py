import frappe
from frappe.utils import now_datetime

def update_completed_events():
    """
    Scheduled task to update events whose end date and time has passed to 'Completed' status.
    """
    current_time = now_datetime()
    
    events = frappe.get_all(
        "Town Hall Event",
        filters={
            "end_datetime": ("<", current_time),
            "status": ("!=", "Completed")
        },
        fields=["name"]
    )

    for event in events:
        frappe.db.set_value("Town Hall Event", event.name, "status", "Completed")
    frappe.db.commit()