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
  	alert($(this).attr('value'));
    $.ajax({
      url: "/apply/",
      type: "POST",
      data: getToken() + "&res=" + $(this).attr('value'),
      success: function() {
        setTimeout(function() {
          //window.location.href = window.location.href;
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
				//$("#cost").text("Ціна за поїздку - " + res.order.cost + " грн");
				//$("#cost").append("<div><input type='button' value='Переглянути інформацію про водія' onclick='driver_infa()'></div>")
				if (res.status == "apply" || res.status == "ok") {
					$("#state").text("Підтверджено");
					$(".send").css("display", "inline");
					$("#cost").append("<p>Ціна за поїздку - " + res.cost + " грн</p>");
					$("#cost").append("<input type='button' class='data-client' value='Про водія' onclick='driver_infa()'>")
					window.clearInterval(interv);
				}
				else if (res.status == "clear") {
					$("#state").text("Відміна замовлення");
					window.clearInterval(interv);	
				}
				else{
					$("#state").text("Очікуйте");
				}
			},
		});
	}, 20000);
});

driver_infa = function() {
  $.ajax({
    url: '/profile_to_json/',
    type: 'POST',
    data: getToken() + '&type_user=driver&order_id=' + order.pk,
    success: function(res) {
      res = JSON.parse(res);
      console.log(res);
      $(".user-infa").append("<p>Водій - " + res.username + "</p>");
      $(".user-infa").append("<p>Рейтинг - " + res.rating + "</p>");
      $(".user-infa").append("<p>Дата реєстрації - " + res.date_registration + "</p>");
    }
  });
}