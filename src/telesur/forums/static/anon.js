function prepEdit(clsContainer) {
        $('a.edit-question').click(function(e) {
            e.preventDefault();
            $(this).addClass("clicked");
            $(clsContainer).parent().addClass("overlay-active");
            return false;
        }).prepOverlay({
             subtype: 'ajax',
             filter: '#content>*',
             formselector: 'form',
             noform: function(el) {
                $('a.edit-question.click').removeClass("clicked");
                return $.plonepopups.noformerrorshow(el, 'reload');
             }
            });
    }

function editAjaxForum(clsConatainer, urlAjax, clsLoading) {
    if(!$('a.edit-question.clicked').length) {
        $.ajax({
            url: urlAjax,
            success: function(html) {
                if(!$('a.edit-question.clicked').length) {
                    $(clsConatainer).parent().html(html);
                    prepEdit(clsConatainer);
                    $(clsLoading).css("display", "none");
                }
            }
        });
    }
}

function intervalSetAnon() {
    editAjaxForum(".session-quesion-answered", "session-view-published", "#forums-loading-responded");
}

$(document).ready(function() {
    if($(".portaltype-telesur-forums-session").length) {
        $('a.question-link').prepOverlay({
             subtype: 'ajax',
             filter: '#content>*',
             formselector: 'form',
             noform: 'reload'
        });

        $("#forums-responded").click(function() {
            $("#forums-loading-responded").css("display", "inline");
            $(".session-quesion-answered").css('display', 'none');
            editAjaxForum(".session-quesion-answered", "session-view-published", "#forums-loading-responded");
        });

        $("ul.session-tabs").tabs("div.session-right-column");
    }
});