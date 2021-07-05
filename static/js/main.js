
(function ($) {
    "use strict";

    /*==================================================================
    [ Validate ]*/
    var message = $('.validate-input textarea[name="message"]');
    /*==

    $('.validate-form').on('submit',function(){
        var check = true;

        if($(message).val().trim() == ''){
            showValidate(message);
            check=false;
        }

        return check;
    });


    $('.validate-form .input1').each(function(){
        $(this).focus(function(){
           hideValidate(this);
       });
    });

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

    */
})(jQuery);
