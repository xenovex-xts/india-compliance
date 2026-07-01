import frappe

from india_compliance.utils.custom_fields import delete_old_fields


def execute():
    delete_tax_id_custom_field()
    set_correct_state_number()
    remove_shipping_fields_from_purchase_invoice()


def delete_tax_id_custom_field():
    # delete custom field tax_id if it exists
    # this field was move to core ERPNext
    delete_old_fields("tax_id", ("Sales Order", "Sales Invoice", "Delivery Note"))


def set_correct_state_number():
    # set correct state number for all states with single digit state number.
    # Backtick-quote the table (frappe rewrites backticks to double quotes on PG)
    # and use LPAD with a single-quoted literal. The original concat("0", ...)
    # broke on PG, where "0" is parsed as an identifier rather than a string.
    frappe.db.sql(
        """UPDATE `tabAddress` SET gst_state_number = LPAD(gst_state_number, 2, '0')
            WHERE LENGTH(gst_state_number) = 1"""
    )


def remove_shipping_fields_from_purchase_invoice():
    delete_old_fields(("port_code", "shipping_bill_number", "shipping_bill_date"), "Purchase Invoice")
