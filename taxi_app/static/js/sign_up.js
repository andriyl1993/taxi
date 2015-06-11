$(function() {
  $("#sign_in").click(function() {
    $.ajax({
      url: "/logging/",
      type: "POST",
      data: getToken() + "&username=" + $("#logging_username").val() + "&password=" + $("#logging_password").val(),
      cached: false,
      success: function(data) {}
    })
  });
});

$(function() {
  $("#client_radiobutton").change(function() {
    $('#client_radiobutton').prop("checked", true);
    $('#driver_radiobutton').prop("checked", false);
    $('#driver_register_form').css("display", "none");
    $('#client_register_form').css("display", "block");
  });
});

$(function() {
  $("#driver_radiobutton").click(function() {
    $('#client_radiobutton').prop("checked", false);
    $('#driver_radiobutton').prop("checked", true);
    $('#driver_register_form').css("display", "block");
    $('#client_register_form').css("display", "none");
  });
});

$(function() {
  $(".btn.btn-primary").click(function() {
    var except = false;
    if ($("#username").val().length < 4) {
      $("#username").addClass("red-border");
      except = true;
    } 
    else {
      $("#username").removeClass("red-border");
    }
    if ($("#first_name").val().length < 1) {
      $("#first_name").addClass("red-border");
      except = true;
    } 
    else {
      $("#first_name").removeClass("red-border");
    }
    if ($("#last_name").val().length < 1) {
      $("#last_name").addClass("red-border");
      except = true;
    } 
    else {
      $("#last_name").removeClass("red-border");
    }
    em1 = $("#email").val().split("@");
    em2 = $("#email").val().split(".");
    if (em1.length < 2 || em2.length < 2 || $("#email").val().length < 1) {
      except = true;
      $("#email").addClass("red-border");
    }
    else {
      $("#email").removeClass("red-border");
    }
    if ($("#reg_form input[type='password']")[0].value.length < 4 || $("#reg_form input[type='password']")[1].value.length < 4 || $("#reg_form input[type='password']")[0].value != $("#reg_form input[type='password']")[1].value) {
      $($("#reg_form input[type='password']")[0]).addClass("red-border");
      $($("#reg_form input[type='password']")[1]).addClass("red-border");
      except = true;
    } 
    else {
      $($("#reg_form input[type='password']")[0]).removeClass("red-border");
      $($("#reg_form input[type='password']")[1]).removeClass("red-border");
    }
    if ($("#driver_radiobutton").is(":checked")) {
      if ($("#rate_min").val().length < 1) {
        $("#rate_min").addClass("red-border");
        except = true;
      } 
      else {
        $("#rate_min").removeClass("red-border");
      }
      if ($("#rate_km_hightway").val().length < 1) {
        $("#rate_km_hightway").addClass("red-border");
        except = true;
      } 
      else {
        $("#rate_km_hightway").removeClass("red-border");
      }
      if ($("#rate_km_city").val().length < 1) {
        $("#rate_km_city").addClass("red-border");
        except = true;
      } 
      else {
        $("#rate_km_city").removeClass("red-border");
      }
      if ($("#rate_min").val().length < 1) {
        $("#rate_min").addClass("red-border");
        except = true;
      } 
      else {
        $("#rate_min").removeClass("red-border");
      }
      if ($("select[name='type_salon']").val() == "Будь-який") {
        $("select[name='type_salon']").addClass("red-border");
        except = true;
      } 
      else {
        $("select[name='type_salon']").removeClass("red-border");
      }
      if ($("#count_places").val().length < 1) {
        $("#count_places").addClass("red-border");
        except = true;
      } 
      else {
        $("#count_places").removeClass("red-border");
      }
    }

    if (except) {
      alert("Заповніть поля відповідно зазначеним вимогам");
      return false;
    }
  });
});