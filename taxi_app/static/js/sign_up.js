$(function() {
	$("#sign_in").click(function() {
		$.ajax({
			url:"/logging/",
			type:"POST",
			data: getToken() + "&username=" + $("#logging_username").val() + "&password=" + $("#logging_password").val(),
			cached: false,
			success: function(data){
				/*res = jQuery.parseJSON(data);
				if (res.status == "ok") {

				}*/
			}
		})
	});
});


$(function(){
	$("#client_radiobutton").change(function(){
		$('#client_radiobutton').prop("checked", true);
		$('#driver_radiobutton').prop("checked", false);
		$('#driver_register_form').css("display", "none");
		$('#client_register_form').css("display", "block");
	});
});

$(function(){
	$("#driver_radiobutton").click(function() {
		$('#client_radiobutton').prop("checked", false);
		$('#driver_radiobutton').prop("checked", true);
		$('#driver_register_form').css("display", "block");
		$('#client_register_form').css("display", "none");	
	});
});