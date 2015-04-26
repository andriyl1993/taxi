function getToken() {
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	return 'csrfmiddlewaretoken=' + token;
}

$(function(){
	$("input[name='is_coords']").change(function() {
		if(this.checked){
			$("#order_form").append("<input type='hidden' name='x_start' value=''>");
			$("#order_form").append("<input type='hidden' name='y_start' value=''>");
			$("#order_form").append("<input type='hidden' name='x_end' value=''>");
			$("#order_form").append("<input type='hidden' name='y_end' value=''>");
			$("#order_form").append("<input type='hidden' name='distance' value=''>");
			$("#order_form").append("<input type='hidden' name='duration' value=''>");
			$("#order_form").append("<input type='button' onclick='click_on_map()' value='остроить точками'>");
		}
		else{
			$("#order_form input[name='x_start']").remove();
			$("#order_form input[name='y_start']").remove();
			$("#order_form input[name='x_end']").remove();
			$("#order_form input[name='y_end']").remove();
			$("#order_form input[name='distance']").remove();
			$("#order_form input[name='duration']").remove();
			$("#order_form input[type='button']").remove();
		}
	});
});

$(function(){
	if(this.checked) {
		interval = setInterval(function() {
			if (typeof end[0] !== "undefined"){
				$("#order_form input[name='x_start']").attr("value", start[0]);
				$("#order_form input[name='y_start']").attr("value", start[1]);
				$("#order_form input[name='x_end']").attr("value", end[0]);
				$("#order_form input[name='y_end']").attr("value", end[1]);
				clearInterval(interval);
				create_way_from_points();
			}},  1000)
	}
});

$(function() {
	$("#end").change(function() {
		interval = setInterval( function() {
			$("#order_form").append("<input type='hidden' name='distance' value=''>");
			$("#order_form").append("<input type='hidden' name='duration' value=''>");
			create_way_from_names_of_places(); 
			clearInterval(interval); 
		}, 1000);
	});
});