import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_url

@frappe.whitelist(allow_guest=True)
def register_participant(full_name, email, town_hall_event):
    try:
        registration = frappe.get_doc({
            "doctype": "Town Hall Event Registration",
            "full_name": full_name,
            "email": email,
            "town_hall_event": town_hall_event
        })
        registration.insert(ignore_permissions=True)

        event = frappe.get_doc("Town Hall Event", town_hall_event)

        send_confirmation_email(email, full_name, event)
        frappe.db.commit()

        return {"status": "success", "message": "Registered and email sent."}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Event Registration Error")
        return {"status": "error", "message": str(e)}

def send_confirmation_email(email, name, event):
    subject = f"Thank you for registering for {event.name}"
    # subject = f"Thank you for registering"
    message = f"""
    <p>Dear {name},</p>
    <p>Thank you for registering for <strong></strong>.</p>
    <p><strong>Date:</strong> {event.start_datetime}<br>
    <strong>Location:</strong> {"surat"}</p>
    <p>We look forward to your participation.</p>
    <p>Best regards,<br>Your Event Team</p>
    """

    frappe.sendmail(
        recipients=email,
        subject=subject,
        message=message
    )