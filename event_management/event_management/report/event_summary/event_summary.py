# Copyright (c) 2025, jeel and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate

def execute(filters=None):
    columns = [
        {"label": "Metric", "fieldname": "metric", "fieldtype": "Data"},
        {"label": "Value", "fieldname": "value", "fieldtype": "Int"},
    ]
    upcoming_events = frappe.db.count("Town Hall Event", filters={"start_datetime": [">=", nowdate()]})
    total_registrations = frappe.db.count("Town Hall Event Registration")

    data = [
        {"metric": "Upcoming Events", "value": upcoming_events},
        {"metric": "Total Registrations", "value": total_registrations},
    ]
    
    chart = {
        "data": {
            "labels": ["Upcoming Events", "Total Registrations"],
            "datasets": [
                {
                    "name": "metric",
                    "values": [upcoming_events, total_registrations],
                }
            ]
        },
        "type": "bar",  # bar / line / pie
        "height": 250
    }

    return columns, data, None, chart
