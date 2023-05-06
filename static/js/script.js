$(document).ready(function(){
    window.cartItems = [];

console.log(window.sessionStorage.getItem("cart_items"));
// window.sessionStorage.removeItem("cart_items")
    if(window.sessionStorage.getItem("cart_items")!=null && JSON.parse(window.sessionStorage.getItem("cart_items")).length<=0)
    {
        window.cartItems = JSON.parse(sessionStorage.getItem("cart_items"));
    }


    let update_cart_count = () => {
       if(sessionStorage.getItem("cart_items")!=null)
       {
         window.cartItems = JSON.parse(sessionStorage.getItem("cart_items"));
         document.getElementById('cart_count').innerHTML= cartItems.length;
       }
       else {
         document.getElementById('cart_count').innerHTML= '0';

       }

    }


    cartcountUpdate();

    $(document).on('click','.incr-btn',function(){
        dataaction = $(this).attr('data-action');
        product_id = $(this).attr('data-p');
        let currentqty = parseInt($('#inpqty_'+product_id).attr('value'));
        console.log(currentqty);

        if(dataaction=='decrease'&&currentqty>0)
        {
        currentqty = currentqty - 1;

        }
        else if(dataaction=='increase'&&currentqty<100)
        {
          currentqty = currentqty + 1;
        }

        $('#inpqty_'+product_id).attr("value",currentqty);
        $('#inpqty_'+product_id).val(currentqty);

        calc_total();

    });



    var calc_total = () => {
      accInline = 0;

      $('.quantity').each(function(){


        console.log($(this).attr('data-price'))
        console.log($(this).val())

          var new_inline = (parseFloat($(this).val()))*(parseFloat($(this).attr('data-price')));
          accInline +=new_inline


      });
      var tot = $('#total').text('Cad '+parseFloat(accInline).toFixed( 2 ));
    }


    $('.item-remove').click(function(event){
          event.preventDefault()
          $(this).attr('data-delete','True');

          $('#inpqty_'+$(this).attr('data-p')).attr("value",0);

          $(this).parent().hide();
          calc_total();
      });



    $('#update').click(function(event){
        event.preventDefault()
        //$(this).fadeOut(300);
        console.log("a");
        send_ = []
        $('.count-input').each(function(){
            send = {}
            //console.log('Div object: ', $(this).children())
//            console.log('flag value: ', $(this).parent().next().attr('data-delete'))
            input = $(this).children()[1]
            qnt = $(input).val()
            id_value = $(input).attr('data-p')
            price = $(input).attr('data-price')
            del = $(this).parent().next().attr('data-delete')
//            console.log('value, id_value, del', qnt, id_value, del)
            send.id = id_value
            send.qnt = qnt
            send.price = price
            send.del = del
            send_.push(send)
        })


//        console.log(send_)
        $.ajax({
            url: '/cart_edit/',
            type: 'post',
            data: { 'csrfmiddlewaretoken' : csrftoken, 'send':JSON.stringify(send_)},

            success : function(data) {
                console.log('Cart items Updated');
//                console.log('success');
            },

            error : function() {
                console.log('Failed Adding Item to cart');
            }

        });
    });









        $('#checkout').click(function(event){
            event.preventDefault()
    //        console.log('Hello')
            var fname = $('#firstname').val();
            var lname = $('#lname').val();
            var email = $('#em').val();
            var add1 = $('#add1').val();
            var add2 = $('#add2').val();
            var ph = $('#phone').val();
            var co = $('#co').val();
            var county = $('#county').val();
            var state = $('#state').val();
            var city = $('#ci').val();
            var zip = $('#zip').val();

            $.ajax({
                url: '/checkoutcommit/',
                type: 'post',
                data: { 'csrfmiddlewaretoken' : csrftoken, 'firstname' : fname, 'lastname' : lname, 'email' : email, 'phone' : ph, 'address1' : add1, 'address2' : add2, 'company' : co, 'country' : county, 'state' : state, 'city' : city, 'zip' : zip },
    //
                success : function(data) {
    //                console.log(data)
    //                console.log('fname'+fname)
    //                console.log('lname'+lname)
    //                console.log('email'+em)
    //                console.log('add1'+add1)
    //                console.log('add2'+add2)
    //                console.log('phone'+phone)
    //                console.log('company'+co)
    //                console.log('county'+county)
    //                console.log('city'+city)
    //                console.log('zipcode'+zip)
    //
                    console.log('Proccede to payment');
                    window.location = "/payment/";
    //                console.log('success');
                },

                error : function() {
                    console.log('Failed Adding Item to cart');
                }

            });
        });





  // using jQuery
     function getCookie(name) {
         var cookieValue = null;
         if (document.cookie && document.cookie !== '') {
             var cookies = document.cookie.split(';');
             for (var i = 0; i < cookies.length; i++) {
                 var cookie = jQuery.trim(cookies[i]);
                 // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) === (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
     }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

function cartcountUpdate(){




           $.ajax({
               url: '/cartcount/',
               type: 'get',
               data: {},
       //            // handle a successful response
               success : function(data) {
       //                console.log(data)
                   sc = data.length;
                   console.log(sc);

                   $("#cart_count").text(sc)
       //                console.log('The Number'+s)

                   $('#cart-dropdown').html('')

               },
               error : function() {
                   console.log('Not yet'); // provide a bit more info about the error to the console
               }
           });




   };






   $('#add_cart').click(function(event){


     var url = window.location.href;
     var result= url.split('/');
     var param = result[result.length-2];

     var item = param;
     var qnt = 1;
/*
     if(window.sessionStorage.getItem("cart_items")!= null)
     {
       window.cartItems = JSON.parse(sessionStorage.getItem("cart_items"));
       if(window.cartItems.length>0)
       {
         var product_found = 0;
         for (var i = 0; i < window.cartItems.length; i++) {
             if(window.cartItems[i]['product']==item){
               //product exists
               window.cartItems[i]['quantity']+=qnt;
               product_found = 1;
               break;
             }
         }
         if(product_found==0)
         {
           //product does not exist
           cartItem = {"product" : item, "quantity" : qnt};
           window.cartItems.push(cartItem);
         }

       }
     }
     else {
        //product does not exist
        cartItem = {"product" : item, "quantity" : qnt};
        window.cartItems.push(cartItem);
      }


      window.sessionStorage.setItem("cart_items", JSON.stringify(window.cartItems));
      update_cart_count();
*/
     //$('#qnt').val();


//        console.log('item: '+item)
//        console.log('qnt: '+qnt)



     $.ajax({
         url: '/add/',
         type: 'post',
         data: { 'csrfmiddlewaretoken' : csrftoken, 'item':item,'qnt':qnt},

//            success : function(data) {
//                alert('Cart item Added');
//                console.log('success');
//            },
         success: function(data){
            cartcountUpdate();
             console.log('Cart item Added');
             $('.alert').alert()

         },

         error : function() {
             console.log('Failed Adding Item to cart');
         }

     });
 });




});
