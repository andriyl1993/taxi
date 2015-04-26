function getToken() {
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	return 'csrfmiddlewaretoken=' + token;
}

$(function() {
	$("#change_state").click(function() {
		var state = 0;
		var state_new = 0;
		if ($("#state p b").html() == "offline") {
			state = 2;
			state_new = 0;
		}
		else {
			state = 0;
			state_new = 2;
		}

		driver = JSON.parse($("#driver").attr("value"))
		$.ajax({
			url: "/change_state/",
			type:"POST",
			data: getToken() + "&state=" + state_new + "&driver=" + driver.username,
			success: function(data){
				if (state_new == 2) {
					$("#state p b").html("offline");
				}
				else{
					$("#state p b").html("online");	
				}
			}
		});
	});
});

$(function() {
	$(".mark").click(function() {
		console.log($(this).parents("table").find("tr th")[0].innerHTML);
		if ($(this).parents("table").find("tr th")[0].innerHTML == "Driver") {
			$(this).parents("tr").append("<input type='text' class='car_state'>");
			$(this).parents("tr").append("<input type='text' class='order_execution'>");
			$(this).parents("tr").append("<input type='text' class='comfort'>");
			$(this).parents("tr").append("<input type='button' class='post_rating' value='save'>");	
		}
		else {
			$(this).parents("tr").append("<input type='text' class='value'>");
			$(this).parents("tr").append("<input type='button' class='post_rating' value='save'>");
		}

		$(".post_rating").click(function() {	
			if ($(this).parents("table").find("tr th")[0].innerHTML == "Driver") {
				var car_state = $(this).parents("tr").find(".car_state")[0].value;
				if (!$.isNumeric(car_state) || parseInt(car_state) > 5 || parseInt(car_state) < 0)
					return false;
				var order_execution = $(this).parents("tr").find(".order_execution")[0].value;
				if (!$.isNumeric(order_execution) || parseInt(order_execution) > 5 || parseInt(order_execution) < 0)
					return false;
				var comfort = $(this).parents("tr").find(".comfort")[0].value;
				if (!$.isNumeric(comfort) || parseInt(comfort) > 5 || parseInt(comfort) < 0)
					return false;
				var pk = $(this).parents("tr").find(".pk")[0].innerHTML
				data = getToken() + "&car_state=" + car_state + "&order_execution=" + order_execution + "&comfort=" + comfort + "&pk=" + pk;
				
				$(this).parents("tr").find(".car_state").remove();
				$(this).parents("tr").find(".order_execution").remove();
				$(this).parents("tr").find(".comfort").remove();
				$(this).parents("tr").find(".post_rating").remove();
			} 
			else {
				var value = $(this).parents("tr").find(".value")[0].value;
				if (!$.isNumeric(value) || parseInt(value) > 5 || parseInt(value) < 0)
					return false;
				var pk = $(this).parents("tr").find(".pk")[0].innerHTML
				data = getToken() + "&value=" + value + "&pk=" + pk;
				$(this).parents("tr").find(".value").remove();
				$(this).parents("tr").find(".post_rating").remove();				
			}
			$.ajax({
				url: "/mark_rating/",
				type: "POST",
				data: data,
				success: function(res) {	
					obj = JSON.parse(res);	
					tds = $("table").find("td[class='pk']");
					for (var i = 0; i < tds.length; i++) {
						if (tds[i].innerHTML == obj.pk){
							$(tds[i]).innerHTML = obj.res;
						}
					}
				}
			});
		});
	});
});

$(function() {
	$(".add_to_favourite").click(function() {
		var pk = $(this).parents("tr").find(".pk")[0].innerHTML
		$.ajax({
			url: "/add_to_favourite/",
			type: "POST",
			data: getToken() + "&pk=" + pk,
			success: function(res) {
				obj = JSON.parse(res);
				if (obj.status != "add") {
					alert("add");
				}
				else if(obj.status != "driver already added") {
					alert("driver already added");
				}
				else {
					alert("error");
				}
			}
		});
	});
});