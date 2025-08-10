/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { ClosePosPopup } from "@point_of_sale/app/navbar/closing_popup/closing_popup";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useState } from "@odoo/owl";

patch(ClosePosPopup.prototype, {
    setup() {
        super.setup();

        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
        this.hardwareProxy = useService("hardware_proxy");

        // Initialize state
        this.state = useState({
            notes: "",
            payments: {}
        });

        // Set cash control to "0" as in original
        if (this.pos.config.cash_control) {
            this.state.payments[this.props.default_cash_details.id] = {
                counted: "0"  // Keep original behavior
            };
        }

        // Initialize other payment methods that have transactions
        this.props.other_payment_methods.forEach((pm) => {
            if (pm.amount !== 0) {
                this.state.payments[pm.id] = {
                    counted: "0"  // Set to "0" for other methods with transactions
                };
            }
        });
    },

    // Helper method to check if this is ATM specifically (based on name)
    isATM(pm) {
        return pm && pm.name === 'ATM';
    },

    // Helper method to check if this is a delivery service (all other bank types except ATM)
    isDeliveryService(pm) {
        return pm && pm.type === 'bank' && pm.name !== 'ATM';
    },

    // Helper method to check if this is Customer Account
    isCustomerAccount(pm) {
        return pm && pm.name === 'Customer Account';
    },

    // Helper method to show/hide Expected column based on payment method and config
    shouldShowExpected(pm) {
        // For Cash
        if (!pm) {
            // Hide Expected for Cash if balance_control is active
            return !this.pos.config.balance_control;
        }

        // For ATM specifically
        if (this.isATM(pm)) {
            // Hide Expected for ATM if for_atm is active
            return !this.pos.config.for_atm;
        }

        // For delivery services and customer account
        if (this.isDeliveryService(pm) || this.isCustomerAccount(pm)) {
            // Hide Expected if for_others is active
            return !this.pos.config.for_others;
        }

        // Default - show Expected
        return true;
    },

    // Helper method to show/hide Difference column based on payment method and config
    shouldShowDifference(pm, hasAmount = true) {
        if (!hasAmount) {
            return false;
        }

        // For Cash
        if (!pm) {
            // Hide Difference for Cash if balance_control is active
            return !this.pos.config.balance_control;
        }

        // For ATM specifically
        if (this.isATM(pm)) {
            // Hide Difference for ATM if for_atm is active
            return !this.pos.config.for_atm && hasAmount;
        }

        // For delivery services and customer account
        if (this.isDeliveryService(pm) || this.isCustomerAccount(pm)) {
            // Hide Difference if for_others is active
            return !this.pos.config.for_others && hasAmount;
        }

        // Default - show Difference if has amount
        return hasAmount;
    },

    // Override the getDifference method to handle difference calculations
    getDifference(paymentId) {
        // Get the payment method details
        const isCash = paymentId === this.props.default_cash_details?.id;
        const pm = this.props.other_payment_methods.find(pm => pm.id === paymentId);

        if (!pm && !isCash) {
            return 0;
        }

        // Get counted value
        const counted = this.state.payments[paymentId]?.counted;
        if (!counted || !this.env.utils.isValidFloat(counted)) {
            return 0; // Return 0 instead of NaN
        }

        // Calculate difference
        const expectedAmount = isCash
            ? this.props.default_cash_details.amount
            : pm ? pm.amount : 0;

        return parseFloat(counted) - expectedAmount;
    }
});