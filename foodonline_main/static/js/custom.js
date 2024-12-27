let autocomplete;

function initAutoComplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("id_address"),
    {
      types: ["geocode", "establishment"],
      //default in this app is "IN" - add your country code
      componentRestrictions: { country: ["us"] },
    }
  );
  // function to specify what should happen when the prediction is clicked
  autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
  var place = autocomplete.getPlace();

  // User did not select the prediction. Reset the input field or alert()
  if (!place.geometry) {
    document.getElementById("id_address").placeholder = "Start typing...";
  } else {
    console.log("place name=>", place.name);
  }
  // get the address components and assign them to the fields

  var geocoder = new google.maps.Geocoder();
  var address = document.getElementById("id_address").value;
  geocoder.geocode({ address: address }, function (res, status) {
    
    if (status == google.maps.GeocoderStatus.OK) {
      var latitude = res[0].geometry.location.lat();
      var longitude = res[0].geometry.location.lng();

      $("#id_latitude").val(latitude);
      $("#id_longitude").val(longitude);
    }
  });
  for (var i = 0; i < place.address_components.length; i++) {
    for (var j = 0; j < place.address_components[i].types.length; j++) {
      if (place.address_components[i].types[j] == "country") {
        $("#id_country").val(place.address_components[i].long_name);
      }
      if (
        place.address_components[i].types[j] == "administrative_area_level_1"
      ) {
        $("#id_state").val(place.address_components[i].long_name);
      }
      if (place.address_components[i].types[j] == "locality") {
        $("#id_city").val(place.address_components[i].long_name);
      }
      if (place.address_components[i].types[j] == "postal_code") {
        $("#id_pin_code").val(place.address_components[i].long_name);
      } else {
        $("#id_pin_code").val("");
      }
    }
  }
}

$(document).ready(function () {
  //Addtothe cart
  $(".add_to_cart").on("click", function (e) {
    e.preventDefault();

    food_id = $(this).attr("data_id");
    url = $(this).attr("data_url");
    data = {
      food_id: food_id,
    };
    $.ajax({
      type: "GET",
      url: url,
      data: data,
      success: function (response) {
       
        if (response.status == "login required") {
          //add sweet alert
          // swal("title", "subtitle", "info");
          swal(response.message, "", "info").then(function () {
            window.location = "/accounts";
          });
        } else if (response.status == "failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty_" + food_id).html(response.qty);

          //calculate the subtotal, tax and grand total
          applyCartAmount(
            response.cart_amount["subtotal"],
            response.cart_amount["tax_dict"],
            response.cart_amount["grand_total"]
           
          );
        //  console.log(response.cart_amount["tax_dict"])
        }
      },
    });
  });
  //place the cart item quantity on load
  $(".item_qty").each(function () {
    var the_id = $(this).attr("id");
    var qty = $(this).attr("data_qty");
    $("#" + the_id).html(qty);
  });

  //Decrease the cart
  $(".decrease_cart").on("click", function (e) {
    e.preventDefault();

    food_id = $(this).attr("data_id");
    cart_id = $(this).attr("id");

    url = $(this).attr("data_url");
    data = {
      food_id: food_id,
    };
    $.ajax({
      type: "GET",
      url: url,
      data: data,
      success: function (response) {
        
        if (response.status == "login required") {
          //add sweet alert
          // swal("title", "subtitle", "info");
          swal(response.message, "", "info").then(function () {
            window.location = "/accounts";
          });
        } else if (response.status == "failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(response.cart_counter["cart_count"]);
          $("#qty_" + food_id).html(response.qty);
          if (window.location.pathname == "/cart/") {
            removeCartItem(response.qty, cart_id);
            checkEmptyCart();
            applyCartAmount(
              response.cart_amount["subtotal"],
            response.cart_amount["tax_dict"],
            response.cart_amount["grand_total"]
            );
          }
        }
      },
    });
  });

  //delete the cart
  $(".delete_cart").on("click", function (e) {
    cart_id = $(this).attr("data_id");

    url = $(this).attr("data_url");

    $.ajax({
      type: "GET",
      url: url,

      success: function (response) {
       
        if (response.status == "login required") {
          swal(response.message, "", "info").then(function () {
            window.location = "/accounts";
          });
        } else if (response.status == "failed") {
          swal(response.message, "", "error");
        } else {
          $("#cart_counter").html(
            response.cart_counter ? response.cart_counter["cart_count"] : 0
          );
          $("#qty_" + cart_id).html(response.qty);
          swal(response.status, response.message, "success");
          removeCartItem(0, cart_id);
          checkEmptyCart();
          applyCartAmount(
            response.cart_amount["subtotal"],
            response.cart_amount["tax_dict"],
            response.cart_amount["grand_total"]
          );
        }
      },
    });
  });

  //delete the cart element if the qty is 0
  function removeCartItem(cartitemqty, cart_id) {
    if (cartitemqty <= 0) {
      //remove the cart element
      document.getElementById("cart-item-" + cart_id).remove();
    }
  }

  // check ifthe cart is empty
  function checkEmptyCart() {
    var cart_counter = document.getElementById("cart_counter").innerHTML;
    if (cart_counter == 0) {
      document.getElementById("empty-cart").style.display = "block";
    }
  }

  //apply the cart amount
  function applyCartAmount(subtotal, tax_dict, grandtotal) {
    if (window.location.pathname == "/cart/") {
      $("#subtotal").html(subtotal);

      $("#total").html(grandtotal);
      for (key1 in tax_dict) {
        
        for (key2 in tax_dict[key1]) {
          $('#tax-'+key1).html(tax_dict[key1][key2]);
        }
      }
    }
  }

  //Add the opening hours
  $(".add-hour").on("click", function (e) {
    e.preventDefault();
    var day = document.getElementById("id_day").value;
    var url = document.getElementById("add_hour_url").value;

    var from_hour = document.getElementById("id_from_hour").value;
    var to_hour = document.getElementById("id_to_hour").value;
    var is_closed = document.getElementById("id_is_closed").checked;
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    if (is_closed) {
      is_closed = "True";
      condition = "day!=''";
    } else {
      is_closed = "False";
      condition = "day!='', from_hour!='', to_hour!=''";
    }
    if (eval(condition)) {
      $.ajax({
        type: "POST",
        url: url,
        data: {
          day: day,
          from_hour: from_hour,
          to_hour: to_hour,
          is_closed: is_closed,
          csrfmiddlewaretoken: csrf_token,
        },
        success: function (response) {
          if (response.status == "success") {
            if (response.is_closed == "closed") {
              html = `<tr id="hour-${response.id}">
                          <td><b>${response.day}</b></td>
                          <td><b>closed</b></td>
                          <td><a href="#" class="remove-hour" data-url="/accounts/vendor/opening_hours/remove/${response.id}/">Remove</a></td>
                      </tr>`;
            } else {
              html = `<tr id="hour-${response.id}">
                <td><b>${response.day}</b></td>
                <td><b>${response.from_hour}-${response.to_hour}</b></td>
                <td> <a href="#" class = "remove-hour" data-url = "/accounts/vendor/opening_hours/remove/${response.id}/">Remove</a></td>
              </tr>`;
            }

            $(".opening_hours").append(html);
            document.getElementById("opening_hours").reset();
          } else {
           
            swal(response.message, "", "error");
          }
        },
      });
    } else {
      swal("please fill the filds", "", "info");
    }
    
  });

  //Remove opening hour
  // $(document).on("click", ".remove-hour", function (e) {
  //   e.preventDefault();

  //   url = $(this).attr("data-url");
  //   console.log(url);
  //   $.ajax({
  //     type: "GET",
  //     url: url,

  //     success: function (response) {
  //       console.log(response);
  //       if (response.status == "success") {
  //         document.getElementById("hour-" + response.id).remove();
  //       }
  //     },
  //   });
  // });

  $(document).on("click", ".remove-hour", function (e) {
    e.preventDefault();

    let url = $(this).attr("data-url");
    let row = $(this).closest("tr"); // Get the closest table row to remove
    
    $.ajax({
      type: "GET",
      url: url,
      success: function (response) {
        if (response.status === "success") {
          row.remove(); // Remove the row directly without relying on ID
        } else {
          swal(response.message, "", "error");
        }
      },
      error: function () {
        swal("Failed to remove the opening hour.", "", "error");
      },
    });
  });
  // document read closed here
});
