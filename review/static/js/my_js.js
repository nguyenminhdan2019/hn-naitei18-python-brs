$(document).ready(function () {
    $("#markFavoriteButton").click(function () {
        var serializedData =
            $("#markFavoriteForm").serialize();

        $.ajax({
            url: $("#markFavoriteForm").data('url'),
            data: serializedData,
            type: 'post',
            success: function (response) {
                if (response.stt == 'fa') {
                    $("#fa_status").val('un_fa')
                    $("#markFavoriteButton").val('Unfavorite');
                } else {
                    $("#fa_status").val('fa')
                    $("#markFavoriteButton").val('Favorite');
                }
            }
        })
        $("#markFavoriteForm")[0].reset();
    });

    $("#markReadButton").change(function () {
        var serializedData =
            $("#markReadForm").serialize();

        $.ajax({
            url: $("#markReadForm").data('url'),
            data: serializedData,
            type: 'post',
            success: function (response) {
                if (response.stt == 'nr') {
                    $("#markReadButton").val('nr')
                } else if (response.stt == 'r_ing') {
                    $("#markReadButton").val('r_ing')
                } else
                    $("#markReadButton").val('r_ed')
            }
        })
        $("#markReadForm")[0].reset();
    });

    $("#btn-edit").on('click',function () {
        var edit_review = $("#edit-review")
        edit_review.css({display:'block'});
        var my_review = $("#my-review")
        my_review.css({display:'none'});        
    });

    $("#btn-cancle").on('click',function () {
        var edit_review = $("#edit-review")
        edit_review.css({display:'none'});
        var my_review = $("#my-review")
        my_review.css({display:'block'}); 
    });
});
