/** @odoo-module **/
import { patch } from '@web/core/utils/patch';
import { CashOpeningPopup } from "@point_of_sale/app/store/cash_opening_popup/cash_opening_popup";
import { useService } from "@web/core/utils/hooks"; // Add missing import
import { usePos } from "@point_of_sale/app/store/pos_hook"; // Add missing import
import { useState } from "@odoo/owl";

patch(CashOpeningPopup.prototype, {
    setup() {
        super.setup();  // Call the parent setup first

        console.log("CashOpeningPopup loaded!");

        this.pos = usePos();
        this.state = useState({
            notes: "",
            openingCash: "0", // Override to empty string
        });

        this.popup = useService("popup");
        this.orm = useService("orm");
        this.hardwareProxy = useService("hardware_proxy");

        console.log("POS Instance: ", this.pos);
    }
});
