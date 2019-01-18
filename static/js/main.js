$(function()
{
  $('#id_rating').on('input change', function(){
    $(this).next($('#id_rating')).html(this.value);
  });
  $('#id_rating').each(function(){
    var value = $(this).prev().attr('value');
    $(this).html(value);
  });    
})
document.getElementsByClassName("slider_label") = "0";
