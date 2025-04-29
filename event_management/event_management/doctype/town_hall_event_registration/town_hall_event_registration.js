// Copyright (c) 2025, jeel and contributors
// For license information, please see license.txt

frappe.ui.form.on("Town Hall Event Registration", {
	refresh(frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('View Registrations'), function () {
                frappe.set_route('List', 'Town Hall Event Registration', {
                        'town_hall_event': frm.doc.town_hall_event
                });
            });
        }
	},
});
