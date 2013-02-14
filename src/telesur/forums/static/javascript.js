function changeState(){
    jQuery.ajax({type: 'POST',
                 url: this.href,
                 async : true,
                 success: function(results){
                    location.reload();
                 }
    });

    return false;
}




$(document).ready(function() {
    $('a.is-closed').click(function(e) {
        e.preventDefault();
        return false;
    });


    function limitText(limitField, limitNum) {
        if (limitField.value.length > limitNum) {
            limitField.value = limitField.value.substring(0, limitNum);
        }
    }

    if($(".template-telesur\\.forums\\.session").length) {
        var help = $("#formfield-form-widgets-IDublinCore-description .formHelp");
        help.text(help.text() + " (max 200 caracteres)");
        $("#form-widgets-IDublinCore-description").keydown(function() {
            limitText(this, 200);
        });
        $("#form-widgets-IDublinCore-description").focusout(function() {
            limitText(this, 200);
        });
        $("#form-widgets-IDublinCore-description").change(function() {
            limitText(this, 200);
        });
    }


    $('a.edit-question').prepOverlay({
         subtype: 'ajax',
         filter: '#content>*',
         formselector: 'form',
         noform: 'reload'
        });

    $('a.wf-change').click(changeState);
    $("ul.session-tabs").tabs("div.session-right-column");
});