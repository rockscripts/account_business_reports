odoo.define("account_business_reports.dashboard", function (require)
{
    "use strict";
    
    var Class = require('web.Class');
    var rpc = require('web.rpc')

    var Dashboard = Class.extend({
        init: function () 
        {
            self.populate_default();    
        },
        define_events()
        {
            var self = this;
            $("#seller_search_informe_ganancia_liquida").on('blur',function()
            {
                var model = $(this).attr('model');
                var keyword = $(this).val();
                self.search_in_field(model, keyword, in_field);
            });
            $("#partner_search_informe_ganancia_liquida").on('blur',function(){
                
            });
        },
        populate_default()
        {
            
        },
        search_in_field(model, keyword, in_field)
        {
            rpc.query( 
                        {
                            model: 'reports.history',
                            method: 'search_in_field',
                            args:[[model, keyword, in_field]]
                        }
                    ).
                    then(function(results)
                    {  
                        console.log('search_in_field');
                        console.log(results);
                    });
        },
        assign_field_value(selector, value)
        {
            selector.val(value);
        }
    });
});