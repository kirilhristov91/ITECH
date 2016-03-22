$(document).ready(function(){
     $('.carousel').carousel({
        interval: 5000 //changes the speed
    });

      $('#goToBottom').click(function(){
          var WH = $(window).height();
          var SH = $('body')[0].scrollHeight;
          $('html, body').stop().animate({scrollTop: SH-WH}, 1000);

          console.log( SH+' '+WH ); // TEST

      });

    $(".summaryButton").click(function (event) {
        var element = this;
        $(this).attr("disabled", true);
        $.ajax({
            url: "/guess_the_movie/summary/" + element.id+"/update/",
            method: "GET",
            data: {},
            success: function (result) {
            }
        });
    });

        $( '#table' ).searchable({
        striped: true,
        oddRow: { 'background-color': '#f5f5f5' },
        evenRow: { 'background-color': '#fff' },
        searchType: 'fuzzy'
    });

    $( '#searchable-container' ).searchable({
        searchField: '#container-search',
        selector: '.row',
        childSelector: '.col-xs-4',
        show: function( elem ) {
            elem.slideDown(100);
        },
        hide: function( elem ) {
            elem.slideUp( 100 );
        }
    });


     var $table = $('table.scroll'),
    $bodyCells = $table.find('tbody tr:first').children(),
    colWidth;

// Adjust the width of thead cells when window resizes
$(window).resize(function() {
    // Get the tbody columns width array
    colWidth = $bodyCells.map(function() {
        return $(this).width();
    }).get();

    // Set the width of thead columns
    $table.find('thead tr').children().each(function(i, v) {
        $(v).width(colWidth[i]);
    });
}).resize(); // Trigger resize handler

});


function checkRegistration(form)
  {
    if(form.username.value == "") {
      alert("Error: Username cannot be blank!");
      form.username.focus();
      return false;
    }

    if(form.email.value == "") {
      alert("Error: Email cannot be blank!");
      form.email.focus();
      return false;
    }

    if(form.password.value == ""){
        alert("Password cannot be blank");
        form.password.focus();
        return false;
    }else if (form.password.value != form.password2.value){
        alert("Password not the same");
        form.password.focus();
        return false;

    }

    return true;
  }

function checkLogin(form)
{
    if(form.username.value == "") {
      alert("Error: Username cannot be blank!");
      form.username.focus();
      return false;
    }

    if(form.password.value == "") {
      alert("Error: Password cannot be blank!");
      form.password.focus();
      return false;
    }
}