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


function pagination() {
  $(".paginate-questions a").live("click", function(e) {
    e.preventDefault();
    var actual = parseInt($(this).attr("actual"));
    var urlAjax = $(this).attr("redirect") + "/session-view-pag";
    var side = $(this).parent().attr("id");
    $.ajax({
                      url: urlAjax,
                       data:{'b_start':actual, 'side':side},
                      success: function( data ) {
                        $(".session-quesion-answered").html(data);
                      }
                    });
    return false;
    
  });
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
    pagination();
});