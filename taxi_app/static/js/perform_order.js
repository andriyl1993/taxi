function getToken() {
  var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  return 'csrfmiddlewaretoken=' + token;
}

$(function() {
	order = JSON.parse($("#order_json").attr("value"));
	drivers = JSON.parse($("#drivers_json").attr("value"));
	var res = []
	if (order.start_location.x == null){
		start = order.start_location.city + " " + order.start_location.street + " " + order.start_location.building
	}
	else{
		start = [order.start_location.x, order.start_location.y]
	}
	var i = 0
	setTimeout( function() {
		for (i = 0; i < drivers.length; i++) {
			$("body").append("<div id='viewContainer' style='display:none;'></div>");
			end = [drivers[i].x, drivers[i].y]

			way(start, end);
			route_length();
			data = {}
			setTimeout(function() {
				console.log(this.drivers);
				data = return_data_route();
				$("#viewContainer").remove(); 
				inf = {};
				obj = Object();
				obj.distance_to_client = data['distance'];
				obj.duration_to_client = data['duration'];
				obj.distance = this.order['long_travel'];
				obj.duration = this.order['time_travel'];
				obj.order_pk = this.order['pk'];

				obj.username = this.drivers[res.length].username;
				js = JSON.stringify(obj);
				res.push(js);
			}, 5000);
		}
	}, 5000);
	setTimeout(function() {
		$.ajax({
			url: "/return_driver_data_result/",
			type: "POST",
			data: getToken() + "&data=" + res,
		})
	 }, 6000 + 5000 * drivers.length);
});

$(function() {
  $(".send").click(function() {
    $.ajax({
      url: "/apply/",
      type: "POST",
      data: getToken() + "&res=" + $(this).attr('value'),
      success: function() {
        setTimeout(function() {
          window.location.href = window.location.href;
        }, 15000);
      }
    });
  });
});

$(function() {
	interv = setInterval(function() {
		$.ajax({
			url: "/get_result_from_driver/",
			type: "POST",
			data: getToken(),
			success: function(res) {
				res = JSON.parse(res);
				console.log("/get_result_from_driver/");
				console.log(res);
				$("#cost").text("Cost of travel - " + res.cost);
				$("#cost").append("<input type='button' value='Infa about driver' onclick='driver_infa()'>")
				console.log(res.status);	
				if (res.status == "apply" || res.status == "ok") {
					$("#state").text(res.status);
					$(".send").css("display", "inline");
					$("#cost").append("<p>Cost of travel - " + res.order.cost + "</p>");
					$("#cost").append("<input type='button' value='Infa about driver' onclick='driver_infa()'>")
				
					window.clearInterval(interv);
				}
				else if (res.status == "clear") {
					$("#state").text(res.status);
					console.log('clear');
					window.clearInterval(interv);	
				}
				else{
					$("#state").text(res.status);
				}
			},
		});
	}, 20000);
});

driver_infa = function() {
  $.ajax({
    url: '/profile_to_json/',
    type: 'POST',
    data: getToken() + '&type_user=driver&username=' + order.client,
    success: function(res) {
      res = JSON.parse(res);
      console.log(res);
      $(".user-infa").append("<p>Driver - " + res.username + "</p>");
      $(".user-infa").append("<p>Rating - " + res.rating + "</p>");
      $(".user-infa").append("<p>Date registration - " + res.date_registration + "</p>");
    }
  });
}