odoo.define('pos_cash_for_users.chrome_override', function(require) {
    'use strict';

    const Chrome = require('point_of_sale.Chrome');
    const Registries = require('point_of_sale.Registries');

    const ChromeCashForUsers = Chrome => class extends Chrome {
        
        /**
         * MAIN FIX: Override showCashMoveButton to allow POS Users
         * 
         * Original pos_hr.chrome code:
         * return super.showCashMoveButton() && (!this.env.pos.cashier || this.env.pos.cashier.role == 'manager');
         * 
         * Problem: Only shows for managers (this.env.pos.cashier.role == 'manager')
         * Solution: Remove the role restriction
         */
        showCashMoveButton() {
            // Get the basic requirements (same as parent)
            const parentResult = super.showCashMoveButton();
            
            // Check if HR module is enabled
            if (this.env.pos.config.module_pos_hr) {
                // Original logic had: && (!this.env.pos.cashier || this.env.pos.cashier.role == 'manager')
                // New logic: Show for ALL users if they have a cashier assigned
                const hasCashier = !this.env.pos.cashier || this.env.pos.cashier;
                
                console.log(');=== Cash Move Button Check ==='
                console.log('Parent result (basic requirements):', parentResult);
                console.log('Current cashier:', this.env.pos.cashier?.name);
                console.log('Cashier role:', this.env.pos.cashier?.role);
                console.log('Has cashier:', hasCashier);
                console.log('Final result:', parentResult && hasCashier);
                console.log('===============================');
                
                return parentResult && hasCashier;
            }
            
            // If no HR module, use parent result
            return parentResult;
        }
        
        /**
         * ADDITIONAL FIX: Ensure header buttons show for all users
         * 
         * Original pos_hr.chrome code:
         * return !this.env.pos.config.module_pos_hr || this.env.pos.get_cashier().role == 'manager' || this.env.pos.get_cashier_user_id() === this.env.pos.user.id;
         */
        get headerButtonIsShown() {
            if (this.env.pos.config.module_pos_hr) {
                // Show header buttons if:
                // 1. User is a manager, OR
                // 2. User is the same as cashier, OR  
                // 3. Any POS user (NEW: this allows all POS users)
                const cashier = this.env.pos.get_cashier();
                const isManager = cashier && cashier.role === 'manager';
                const isSameUser = this.env.pos.get_cashier_user_id() === this.env.pos.user.id;
                const isPosUser = this.env.pos.user && this.env.pos.user.groups_id;
                
                return isManager || isSameUser || isPosUser;
            }
            
            // If no HR module, always show
            return true;
        }
        
        /**
         * SUPPORTING FIX: Ensure cash control is available for all users
         */
        shouldShowCashControl() {
            if (this.env.pos.config.module_pos_hr) {
                // Original: return super.shouldShowCashControl() && this.env.pos.hasLoggedIn;
                // New: Show if cash control is enabled and any user is logged in
                const basicRequirement = super.shouldShowCashControl();
                const hasAnyUser = this.env.pos.cashier || this.env.pos.user;
                
                return basicRequirement && hasAnyUser;
            }
            return super.shouldShowCashControl();
        }
    };

    Registries.Component.extend(Chrome, ChromeCashForUsers);
    return Chrome;
});
