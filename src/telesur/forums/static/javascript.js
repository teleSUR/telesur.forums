function changeState(e){
    e.preventDefault();
    jQuery.ajax({type: 'POST',
                 url: this.href,
                 async : true,
                 success: function(results){
                    location.reload();
                 }
    });

    return false;
}

function intervalSetMember() {
    editAjaxForum(".forums-pending", "session-view-pending", "#forums-loading-pending");
    editAjaxForum(".forums-rejected", "session-view-rejected", "#forums-loading-rejected");

    $.ajax({
        dataType: "json",
        url: "session-pending-number",
        success: function(data) {
            var number = parseInt(data['pending'], 10);
            if( number > 0) {
                $("#session-pending-number").text("("+number+")");
            }
        }
    });
}

$(document).ready(function() {

    if($(".portaltype-telesur-forums-session").length) {
        $('a.is-closed').live("click", function(e) {
            e.preventDefault();
            return false;
        });

        $("#forums-pending").click(function() {
            $("#forums-loading-pending").css("display", "inline");
            $(".forums-pending").css('display', 'none');
            editAjaxForum(".forums-pending", "session-view-pending", "#forums-loading-pending");
        });

        $("#forums-rejected").click(function() {
            $("#forums-loading-rejected").css("display", "inline");
            $(".forums-rejected").css('display', 'none');
            editAjaxForum(".forums-rejected", "session-view-rejected", "#forums-loading-rejected");
        });

        prepEdit(".forums-pending");
        prepEdit(".forums-rejected");

        $('a.wf-change').live("click", changeState);
    }
});