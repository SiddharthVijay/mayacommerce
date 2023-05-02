$(document).ready(function(){
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

function BudgeUpdate(){
       $.ajax({
           url: '/Products/supdate/',
           type: 'get',
           data: {},
//            // handle a successful response
           success : function(data) {
//                console.log(data)
               sc = data.length
               $("#scount").text(sc)
//                console.log('The Number'+s)

               $('#cart-dropdown').html('')

           },
           error : function() {
               console.log('Not yet'); // provide a bit more info about the error to the console
           }
       });
   };







   $('#add_cart').click(function(event){
     alert("0");
     var item = 1;
     //$('#vari_select option:selected').val()
     var qnt = 1;
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
          //   BudgeUpdate();
             alert('Cart item Added');
         },

         error : function() {
             alert('Failed Adding Item to cart');
         }

     });
 });




});
