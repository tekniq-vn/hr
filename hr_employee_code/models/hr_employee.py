# Copyright 2011, 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>
# Copyright 2016 OpenSynergy Indonesia
# Copyright 2018 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import random
import string

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    """Implement company wide unique code number."""

    _inherit = "hr.employee"

    code = fields.Char(string="Code", groups="hr.group_hr_user", tracking=True, copy=False)

    _sql_constraints = [
        (
            "code_uniq",
            "unique(code)",
            "The Employee Number must be unique across the company(s).",
        ),
    ]

    @api.model
    def _generate_code(self):
        """Generate a random employee code number"""
        company = self.env.user.company_id

        steps = 0
        for _retry in range(50):
            employee_code = False
            if company.employee_code_gen_method == "sequence":
                if not company.employee_code_sequence:
                    _logger.warning("No sequence configured for employee Code generation")
                    return employee_code
                employee_code = company.employee_code_sequence.next_by_id()
            elif company.employee_code_gen_method == "random":
                employee_code_random_digits = company.employee_code_random_digits
                rnd = random.SystemRandom()
                employee_code = "".join(
                    rnd.choice(string.digits) for x in range(employee_code_random_digits)
                )

            if self.search_count([("code", "=", employee_code)]):
                steps += 1
                continue

            return employee_code

        raise UserError(
            _("Unable to generate unique Employee Code in %d steps.") % (steps,)
        )

    @api.model
    def create(self, vals):
        if not vals.get("code"):
            vals["code"] = self._generate_code()
        return super(HrEmployee, self).create(vals)
