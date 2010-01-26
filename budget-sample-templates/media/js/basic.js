var Basic = {
    setup: function() {
        Basic.highlight_current_tab();
        Basic.setup_datepickers();
        Basic.setup_hide_show_buttons();
    },
    
    highlight_current_tab: function() {
        var current_location = window.location.pathname;
        
        if(current_location.match(/summary/)) {
            $('#page_navigation ul li a[href*=summary]').addClass('active');
        }
        else if(current_location.match(/category/) || current_location.match(/budget\/budget/) || current_location.match(/setup/)) {
            $('#page_navigation ul li a[href*=setup]').addClass('active');
        }
        else if(current_location.match(/transaction/)) {
            $('#page_navigation ul li a[href*=transaction]').addClass('active');
        }
        else {
            // Dashboard special case.
            $('#page_navigation ul li:first a').addClass('active');
        }
    },
    
    setup_datepickers: function() {
        $("input[type=text]#id_date").datepicker({ 
            dateFormat: $.datepicker.ISO_8601, 
            showOn: "both", 
            buttonImage: "/img/calendar.gif", 
            buttonImageOnly: true 
        });
        
        $("input[type=text]#id_start_date_0").datepicker({ 
            dateFormat: $.datepicker.ISO_8601, 
            showOn: "both", 
            buttonImage: "/img/calendar.gif", 
            buttonImageOnly: true 
        });
    },
    
    setup_hide_show_buttons: function() {
        $('.hide_show_button').click(function() {
            if($(this).text() == "[+]") {
                $(this).text("[-]");
            }
            else {
                $(this).text("[+]");
            }
            
            var hide_show_id = $(this).attr('id')
            var relevant_transactions_id = hide_show_id.replace('id_hide_show', 'id_hidden_transaction_list');
            $('#' + relevant_transactions_id).toggle();
            return false;
        })
    }
}

$(document).ready(Basic.setup);