$(function(){
  $('#radio_control').click(function(){
      value = $(this).prop('checked');
      if (value == true) {
        document.getElementById('radio').play();
      } else {
        document.getElementById('radio').pause();
      }
  });
  $(document).on('click', '.radio-control', function(){
      $('.radio-control').removeClass("active");
      $(this).addClass('active');
  });
  $.fn.scrollToTop=function(){
    $(this).hide().removeAttr("href");
    if($(window).scrollTop()!="0"){
        $(this).fadeIn("slow")
  }
  var scrollDiv=$(this);
  $(window).scroll(function(){
    if($(window).scrollTop()=="0"){
    $(scrollDiv).fadeOut("slow")
    }else{
    $(scrollDiv).fadeIn("slow")
  }
  });
    $(this).click(function(){
      $("html, body").animate({scrollTop:0},"slow")
    })
  }
});
$(function() {$("#toTop").scrollToTop();});
function toggle_radio_play() {
    if ($('#radio-control').text() == "вкл") {
        $('#radio-control').text("выкл");
        document.getElementById('radio').play();
    } else {
        $('#radio-control').text("вкл");
        document.getElementById('radio').pause();
    }
}
