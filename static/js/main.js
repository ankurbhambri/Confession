$(document).on('submit', '#form-comment', function(event){
	var form = $(this).closest("form");
	var url = form.attr("data-validate-url");
	var username = form.attr("data-validate-username");
	var comment = $("textarea").val();
  	event.preventDefault();
   	$.ajax({
      url: url,
      type: "POST",
      data: form.serialize(),
      success: function(response) {
      	var n = '<div class="panel panel-default arrow left"> <div class="panel-body"><header class="text-left"> <div class="comment-user"><i class="fa fa-user"></i> '+  username +' </div> <time class="comment-date" datetime="16-12-2014 01:05"><i class="fa fa-clock-o"></i>Dec 16, 2014</time></header><div class="comment-post"><p><span>';
	    var option = '';
	    if (url != 'undefinded'){
	    	option = '<a class="text-right" href="'+url+'"><i class="fa fa-reply"></i> reply</a>';
	    }
	    var e = '</span></p></p></div>'+option+'</div></div>';
	    text = n + comment + e
      	document.getElementById('show-comment').innerHTML = text;
      }
    });
   document.getElementById('form-comment').reset(); 	
 });
