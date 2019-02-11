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
// document.getElementsByClassName("slider_label") = "0";



// $(document).ready(function(){
//     $("#approve").click(function(){
//     console.log("create post is working!") // sanity check
//     $.ajax({
//         url : "post_approve", // the endpoint
//         type : "POST", // http method
//         data : { "is_approve" : true }, // data sent with the post request

//         // handle a successful response
//         success : function(json) {
//             console.log("success"); // another sanity check
//         },
//     });
//   });
// })


