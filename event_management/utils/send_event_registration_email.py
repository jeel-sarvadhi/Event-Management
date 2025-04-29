import frappe

@frappe.whitelist(allow_guest=True)
def send_event_registration_email(registration_docname):
  # """Send a confirmation email to participant after successful event registration."""
    try:
        registration = frappe.get_doc("Town Hall Event Registration", registration_docname)
        
        if not registration.email:
            frappe.throw("Participant email is missing.")
        
        subject = f"Thank You for Registering for {registration.town_hall_event}!"
        
        message = f"""
        <p>Dear {registration.full_name},</p>
        
        <p>Thank you for registering for the event <strong>{registration.town_hall_event}</strong>.</p>

        <p><strong>Event Details:</strong></p>
        <ul>
            <li><strong>Date:</strong> {registration.start_datetime}</li>
            <li><strong>Time:</strong> {registration.start_datetime or 'TBD'}</li>
           
        </ul>

        <p>We look forward to your participation!</p>

        <p>Warm regards,<br>Your Events Team</p>
        """

        frappe.sendmail(
            recipients=[registration.email],
            subject=subject,
            message=message
        )

        frappe.msgprint(f"Email sent to {registration.email}")
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Event Registration Email Error")
        frappe.throw(f"Failed to send email: {str(e)}")
