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

    $('a.edit-question').prepOverlay({
         subtype: 'ajax',
         filter: '#content>*',
         formselector: 'form',
         noform: 'reload'
        });

    $('a.wf-change').click(changeState);
    $("ul.session-tabs").tabs("div.session-right-column");
});