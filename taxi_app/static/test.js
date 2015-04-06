function getMethod () {
	$.ajax({
	  url: '/api/users/1',
	  data: getToken(),
	  type: 'GET',
	  success: function(data) {
	  	console.log(data);
	  },
	  
	});
}

function getToken() {
	var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
	return 'csrfmiddlewaretoken=' + token;
}