function getToken() {
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	return 'csrfmiddlewaretoken=' + token;
}
/*
$(function() {
	$("#sign_in").click(function() {
		$.ajax({
			url:"/logging/",
			type:"POST",
			data: getToken() + "&username=" + $("#logging_username").val() + "&password=" + $("#logging_password").val(),
			cached: false,
			success: function(data){
				console.log('ok');
			}
		})
	});
});*/

function post_route_data(data) {
	$.ajax({
		url:"/route_data/",
		type:"POST",
		data: getToken() + "&distance=" + data.distance + "&duration=" + data.duration,
		cached: false,
		success: function(){
			console.log("route data posted");
		}
	});
}

function post_location() {
	$("#post").click(function() {
		var data = "";
		if (typeof pos != "undefined" || pos[0] != 0)
			data = getToken() + "&pos[0]=" + pos[0] + "&pos[1]=" + pos[1];
		else
			data = getToken() + "&start=" + start + "&end=" + end;
		$.ajax({
			url:"/post_location/",
			type:"POST",
			data: data,
			cached: false,
			success: function(){
				console.log("location posted");
			}
		});
	});
}

