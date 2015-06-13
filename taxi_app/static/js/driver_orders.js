function getToken() {
  var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  return 'csrfmiddlewaretoken=' + token;
}

$(function() {
  counter = 0;
  get_orders = setInterval(function() {
    $.ajax({
      url: "/get_orders/",
      type: "POST",
      data: getToken(),
      success: function(orders) {
        _orders = JSON.parse(orders)
        add_new_orders(orders);
        if (_orders.length > 0) {
          window.clearInterval(get_orders);
        }
      },
    })
  }, 10000);
});

$(function() {
  my_orders = [];
  setTimeout(function() {}, 4000);
  setInterval(function() {
    cords = my_place();
    $.ajax({
      url: "/post_my_position_in_interval/",
      type: "POST",
      data: getToken() + "&x=" + cords[0] + "&y=" + cords[1],
      cached: false,
    });
  }, 20000);
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
              $(".order-container").append("<div> Замовлення підтверджено </div>");
            } else {
              if (res.status == "clear") {
                $(".order-container").append("<div> Замовлення відмінено </div>");
                window.clearInterval(inter);
                alert("clear");
                window.location.href = window.location.href;
              }
            }
          }
        });
      }, 10000);
    }
  });
}

function clear_order() {
  $.ajax({
    url: "/result_order/",
    type: "POST",
    data: getToken() + "&order=" + my_orders[0] + "&result=clear",
    success: function() {
      clearTimeout(timer);
      window.location.href = window.location.href;
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
    } else {
      start = [order.start_location.x, order.start_location.y];
      end = [order.end_location.x, order.end_location.y];
      way(start, end);
    }
    $(".order-container").append("<div class = 'order" + order.pk + "'></div>")
    var div_val = '.order' + order.pk
    $(div_val).append("<h4><label> Замовлення " + "</label></h4>");
    $(div_val).append("<label class='client'>" + "Клієнт - " + order.client + "</label><br>");
    $(div_val).append("<p><input type='button' class='data-client' value='Дані про клієнта' onclick='user_infa()'></div></p>");
    $(div_val).append("<label class='date'>Дата - " + order.date + "</label><br>");
    is_fast = "";
    if (order.is_fast)
      is_fast = "Так";
    else
      is_fast = "Ні";
    $(div_val).append("<label class='is_fast'>Швидке - " + is_fast + "</label><br>");
    $(div_val).append("<label class='long_travel'>Відстань - " + order.long_travel + "</label><br>");
    $(div_val).append("<label class='time_travel'>Час - " + order.time_travel + "</label><br>");
    $(div_val).append("<label class='cost'>Ціна - " + order.cost + " грн</label><br>");
    $(div_val).append("<input type='button' id='add_order' class='add_order' value='Прийняти' onclick='apply_order()'></input><br>");
    $(div_val).append("<input type='button' class='clear_order' value='Відхилити' onclick='clear_order()'></input><br>");

    my_orders.push(order.pk);
    timer = setTimeout(function() {
      clear_order();
    }, 120000);
  }
}

user_infa = function() {
  $.ajax({
    url: '/profile_to_json/',
    type: 'POST',
    data: getToken() + '&type_user=client&username=' + order.client,
    success: function(res) {
      res = JSON.parse(res);
      $(".user-infa").empty();
      $(".user-infa").append("<table><tbody><tr><td>Користувач </td><td>" + res.username + "</td></tr></tbody></table>");
      $(".user-infa table").append("<tr><td>Рейтинг </td><td>" + res.rating + "</td></tr>");
      $(".user-infa table").append("<tr><td>Дата реєстреції </td><td>" + res.date_registration + "</td></tr>");
    }
  });
  //$(".user-infa").append("<p>User - " + order.client);
}