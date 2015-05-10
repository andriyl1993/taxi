function getToken() {
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	return 'csrfmiddlewaretoken=' + token;
}

$(function() {
	setInterval(function() {
		$.ajax({
			url:"/get_orders/",
			type: "POST",
			data: getToken(),
			success: function(orders) {
				add_new_orders(orders);
			},
		})
	}, 10000);
});

$(function() {
	my_orders = [];
	setTimeout(console.log("pause"), 4000);
	setInterval(function(){
		cords = my_place();
		console.log(cords); 
		$.ajax({
			url:"/post_my_position_in_interval/",
			type: "POST",
			data: getToken() + "&x=" + cords[0] + "&y=" + cords[1],
			cached: false,
		});
	}, 60000);
});

var my_orders;


function apply_order() {
	$.ajax({
		url: "/result_order/",
		type: "POST",
		data: getToken() + "&order=" + my_orders[0] + "&result=apply",
		success: function() {
			inter = setInterval(function() {
				console.log(my_orders[0]);
				$.ajax({
					url: '/last_result/',
					type: "POST",
					data: getToken() + '&order=' + my_orders[0],
					success: function(res) {
						res = JSON.parse(res);
						console.log(res);
						if (res.status == "ok") {
							console.log("apply");
							$(".order-container").append("<div> Order is apply </div>");
						}
						else { 
							if (res.status == "clear") {
								$(".order-container").append("<div> Order is clear </div>");
								window.clearInterval(inter);
								window.location.href = window.location.hrefж
							}
						}
					}
				});
			}, 5000);
		}
	});
}

function clear_order() {
	$.ajax({
		url: "/result_order/",
		type: "POST",
		data: getToken() + "&order=" + my_orders[0] + "&result=clear",
		success: function() {
			
		}
	});
}


//функція для додавання для підтвердження нових повідомлень
function add_new_orders(orders) {
	orders = JSON.parse(orders);
	if (orders.length > 0 && my_orders.length == 0) {
		order = orders[0]
		if (order.start_location.x == null) {
			start = order.start_location.city + " " + order.start_location.street + " " + order.start_location.building;
			end = order.end_location.city + " " + order.end_location.street + " " + order.end_location.building;
			way(start, end);
		}
		else{
			start = [order.start_location.x, order.start_location.y];
			end = [order.end_location.x, order.end_location.y];
			way(start, end);
		}
		$(".order-container").append("<div class = 'order" + order.pk + "'></div>")
		var div_val = '.order' + order.pk
		$(div_val).append("<h4><label> Order " + "</label></h4>");
		$(div_val).append("<label class='client'>" + order.client+ "</label><br>");
		$(div_val).append("<label class='date'>" + order.date + "</label><br>");
		$(div_val).append("<label class='is_fast'>" + order.is_fast+ "</label><br>");
		$(div_val).append("<label class='long_travel'>" + order.long_travel+ "</label><br>");
		$(div_val).append("<label class='time_travel'>" + order.time_travel+ "</label><br>");
		$(div_val).append("<label class='cost'>" + order.cost+ "</label><br>");
		$(div_val).append("<input type='button' id='add_order' class='add_order' value='Прийняти' onclick='apply_order()'></input><br>");
		$(div_val).append("<input type='button' class='clear_order' value='Відхилити' onclick='clear_order()'></input><br>");

		my_orders.push(order.pk);
	}
}