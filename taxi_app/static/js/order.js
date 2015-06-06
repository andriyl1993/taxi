function getToken() {
  var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  return 'csrfmiddlewaretoken=' + token;
}

$(function() {
  ref = window.location.href.split('/');
  if (ref.length == 5) {
    $("#driver_name").attr("value", ref[4]);
  }
});


$(function() {
  $("input[name='is_coords']").change(function() {
    if (this.checked) {
      $("#order_form").append("<input type='hidden' name='x_start' value=''>");
      $("#order_form").append("<input type='hidden' name='y_start' value=''>");
      $("#order_form").append("<input type='hidden' name='x_end' value=''>");
      $("#order_form").append("<input type='hidden' name='y_end' value=''>");
      $("#order_form").append("<input type='hidden' name='distance' value=''>");
      $("#order_form").append("<input type='hidden' name='duration' value=''>");
      $("#order_form").append("<input type='button' onclick='click_on_map()' value='остроить точками'>");
    } else {
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

$(function() {
  if (this.checked) {
    interval = setInterval(function() {
      if (typeof end[0] !== "undefined") {
        $("#order_form input[name='x_start']").attr("value", start[0]);
        $("#order_form input[name='y_start']").attr("value", start[1]);
        $("#order_form input[name='x_end']").attr("value", end[0]);
        $("#order_form input[name='y_end']").attr("value", end[1]);
        clearInterval(interval);
        create_way_from_points();
      }
    }, 1000)
  }
});

$(function() {
  $("#end").change(function() {
    interval = setInterval(function() {
      $("#order_form").append("<input type='hidden' name='distance' value=''>");
      $("#order_form").append("<input type='hidden' name='duration' value=''>");
      create_way_from_names_of_places();
      clearInterval(interval);
    }, 1000);
  });
});

$(function() {
  timeout = setTimeout(function() {
    if ($("#start").val() != "" && $("#end").val() != "") {
      $("#order_form").append("<input type='hidden' name='distance' value=''>");
      $("#order_form").append("<input type='hidden' name='duration' value=''>");
      create_way_from_names_of_places();
    }
    clearTimeout(timeout);
  }, 2000);
});

$(function() {
  $("#create_order").click(function() {
    var except = false;
    if ($("input[name='start']").val() == "") {
      $("input[name='start']").addClass("red-border");
      except = true;
    } else {
      $("input[name='start']").removeClass("red-border");
    }
    if ($("input[name='end']").val() == "") {
      $("input[name='end']").addClass("red-border");
      except = true;
    } else {
      $("input[name='end']").removeClass("red-border");
    }
    if ($("input[type='date']").val() == "") {
      $("input[type='date']").addClass("red-border");
      except = true;
    } else {
      $("input[type='date']").removeClass("red-border");
    }
    if ($("input[type='time']").val() == "") {
      $("input[type='time']").addClass("red-border");
      except = true;
    } else {
      $("input[type='time']").removeClass("red-border");
    }
    if (except == true) {
      return false;
    }
  });
});