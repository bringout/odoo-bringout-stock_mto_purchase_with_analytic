from odoo import api, models


# treba mi li ovo uopšte - ne treba
#class PurchaseOrder(models.Model):
#    _inherit = 'purchase.order'
#
#    @api.model_create_multi
#    def create(self, vals_list):
#        orders = super().create(vals_list)
#        # When the order comes from MTO rule, every picking->move->origin
#        # chain points to mrp.production.  We copy the analytic_distribution.
#        for order in orders:
#            if not order.analytic_distribution and order.origin:
#                # Origin looks like 'WH/MO/00044'
#                mo = self.env['mrp.production'].search([('name', '=', order.origin)], limit=1)
#                if mo and mo.analytic_distribution:
#                    order.analytic_distribution = mo.analytic_distribution
#                    #hernad: ovo radi
#                    order.partner_ref = 'ANALYTIC'
#        return orders


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if not line.analytic_distribution:
                mo = self.env['mrp.production'].search([('name', '=', line.order_id.origin)], limit=1)
                if mo and mo.analytic_distribution:
                    line.order_id.analytic_distribution = mo.analytic_distribution

        return lines