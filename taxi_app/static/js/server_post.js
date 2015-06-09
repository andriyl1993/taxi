/*
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
}*/

/*function post_location() {
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
}*/

//робочий метод, потріьно розкоментувати
//function post_my_position_in_interval(){



/*$(function() {
	$('#create_order').click(function(){
		alert('ads');
			
		$.ajax({
			url:"/search_driver/",
			type: "POST",
			data: getToken() + "&client_x=" + my_place_coord[0] + "&client_y=" + my_place_coord[1],
			cached: false,
			success:
				function(res) {
					drivers = JSON.parse(res);
					console.log(drivers);
					for (var i = 0; i < drivers.length; i++){
						start = [drivers[i].x, drivers[i].y];
						end = [my_place_coord[0], my_place_coord[1]];
						ret = $.getScript("multyroute_driving.js", only_way_res(start, end));
					}
					setTimeout(function(){
						$.ajax({
							url:"/search_driver/",
							type: "POST",
							data: getToken() + "&data=" + JSON.stringify(data_about_drivers_length) + "&add_data=True" + "&drivers=" + JSON.stringify(drivers),
						}); 
					 }, 2000);
				}
		});
	});
})

*/