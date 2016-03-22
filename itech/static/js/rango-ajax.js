 $(document).ready(function(e) {
    $('#likes').click(function(){
    console.log("pressed");
    var catid;
    queid = $(this).attr("data-queid");
    $.get('/guess_the_movie/question/', {question_id: queid}, function(data){
               $('#like_count').html(data);

    });
    });

    $('.myLinkToTop').click(function () {
    $('html, body').animate({scrollTop:$(document).height()}, 'slow');
    return false;
});
});
