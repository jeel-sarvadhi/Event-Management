# Copyright (c) 2025, jeel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class TownHallEventRegistration(Document):
	# """Validate event registration before saving."""
    def validate(self):
        self.check_event_capacity()
        
    def check_event_capacity(self):
        if not self.town_hall_event:
            return

        max_participants = frappe.db.get_value("Town Hall Event", self.town_hall_event, "max_participants")
        if not max_participants:
            return

        current_count = frappe.db.count("Town Hall Event Registration", {
            "town_hall_event": self.town_hall_event,
            "docstatus": ["<", 2]
        })

        if current_count >= max_participants:
            frappe.throw(_("Registration closed: Event has reached the maximum number of participants."))
            