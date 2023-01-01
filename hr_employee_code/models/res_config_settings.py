# Copyright 2015 Salton Massally <smassally@idtlabs.sl>
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2018 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    employee_code_gen_method = fields.Selection(
        related="company_id.employee_code_gen_method",
        readonly=False,
        default=lambda self: self._default_code_gen_method(),
    )
    employee_code_random_digits = fields.Integer(
        related="company_id.employee_code_random_digits",
        readonly=False,
        default=lambda self: self._default_code_random_digits(),
    )
    employee_code_sequence = fields.Many2one(
        "ir.sequence",
        related="company_id.employee_code_sequence",
        readonly=False,
        default=lambda self: self._default_code_sequence(),
    )

    def _default_code_gen_method(self):
        gen_method = self.env.user.company_id.employee_code_gen_method
        if not gen_method:
            gen_method = self.env["res.company"].default_get(
                ["employee_code_gen_method"]
            )["employee_code_gen_method"]
        return gen_method

    def _default_code_random_digits(self):
        digits = self.env.user.company_id.employee_code_random_digits
        if not digits:
            digits = self.env["res.company"].default_get(["employee_code_random_digits"])[
                "employee_code_random_digits"
            ]
        return digits

    def _default_code_sequence(self):
        sequence = self.env.user.company_id.employee_code_sequence
        if not sequence:
            sequence = self.env.ref("hr_employee_code.seq_hr_employee_code")
        return sequence and sequence.id or False
