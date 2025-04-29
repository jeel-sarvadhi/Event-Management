import frappe
from frappe import _
from frappe.utils import validate_email_address, cstr
import re

@frappe.whitelist(allow_guest=True)
def register_for_event():
    # """
    # API to register a participant for an event.
    # """
    town_hall_event = frappe.form_dict.get("town_hall_event")
    full_name = frappe.form_dict.get("full_name")
    email = frappe.form_dict.get("email")
    phone = frappe.form_dict.get("phone")
    try:
        if not town_hall_event:
            return {"status": "error", "message": _("Event is mandatory")}
        
        if not full_name:
            return {"status": "error", "message": _("Full Name is mandatory")}
        
        if not email:
            return {"status": "error", "message": _("Email is mandatory")}
        
        validate_email_address(email, throw=True)
        
        phone = cstr(phone).strip()
        if phone and not re.match(r'^[\d\s+-]{10,15}$', phone):
            return {"status": "error", "message": _("Invalid phone number format")}
        
        if not frappe.db.exists("Town Hall Event", town_hall_event):
            return {"status": "error", "message": _("Event not found")}
        
        if frappe.db.exists("Town Hall Event Registration", {"town_hall_event": town_hall_event, "email": email}):
            return {"status": "error", "message": _("You are already registered for this event")}

        registration = frappe.get_doc({
            "doctype": "Town Hall Event Registration",
            "town_hall_event": town_hall_event,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            # "registration_date": frappe.utils.nowdate(),
            "status": "Confirmed"
        })
        
        registration.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": _("Successfully registered for the event"),
            # "registration_id": registration.name
        }
    
    except Exception as e:
        frappe.log_error(f"Town Hall Event Registration Error: {str(e)}")
        return {
            "status": "error",
            "message": _("An error occurred while processing your registration: {0}").format(str(e))
        }
        