// --------------------carousel-------------------
$(document).ready(function(){
    $("#slider1").owlCarousel({
      items: 4, // Display four items in a row
      loop: true, // Loop the carousel
      margin: 10, // Margin between items
      autoplay: true, // Autoplay the carousel
      autoplayTimeout: 3000, // Autoplay interval in milliseconds
      autoplayHoverPause: true, // Pause autoplay when hovering over the carousel
      responsive: {
        0: {
          items: 1 // Number of items shown on smaller screens
        },
        576: {
          items: 2 // Number of items shown on small screens
        },
        768: {
          items: 3 // Number of items shown on medium-sized screens
        },
        992: {
          items: 4 // Number of items shown on large screens
        }
      }
    });
  });
$(document).ready(function(){
    $("#slider2").owlCarousel({
      items: 4, // Display four items in a row
      loop: true, // Loop the carousel
      margin: 10, // Margin between items
      autoplay: true, // Autoplay the carousel
      autoplayTimeout: 3000, // Autoplay interval in milliseconds
      autoplayHoverPause: true, // Pause autoplay when hovering over the carousel
      responsive: {
        0: {
          items: 1 // Number of items shown on smaller screens
        },
        576: {
          items: 2 // Number of items shown on small screens
        },
        768: {
          items: 3 // Number of items shown on medium-sized screens
        },
        992: {
          items: 4 // Number of items shown on large screens
        }
      }
    });
  });

 $(document).ready(function(){
    $("#slider3").owlCarousel({
      items: 4, // Display four items in a row
      loop: true, // Loop the carousel
      margin: 10, // Margin between items
      autoplay: true, // Autoplay the carousel
      autoplayTimeout: 3000, // Autoplay interval in milliseconds
      autoplayHoverPause: true, // Pause autoplay when hovering over the carousel
      responsive: {
        0: {
          items: 1 // Number of items shown on smaller screens
        },
        576: {
          items: 2 // Number of items shown on small screens
        },
        768: {
          items: 3 // Number of items shown on medium-sized screens
        },
        992: {
          items: 4 // Number of items shown on large screens
        }
      }
    });
  });


// use jquery for not refreshing the page 
$('.plus-cart').click(function(){
    var id= $(this).attr('pid').toString();
    var eml=this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type:"GET",
        url:'/pluscart',
        data:{
            prod_id:id
        },
        success:function(data){
            console.log(data)
            console.log('successs')
            eml.innerText=data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('total_amount').innerText=data.total_amount
        }

    })
    
})

$('.minus-cart').click(function(){
    var id= $(this).attr('pid').toString();
    var eml=this.parentNode.children[2]
    console.log(id)
    $.ajax({
        type:"GET",
        url:'/minuscart',
        data:{
            prod_id:id
        },
        success:function(data){
            console.log(data)
            console.log('successs')
            eml.innerText=data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('total_amount').innerText=data.total_amount
        }

    })
    
})

$('.remove-cart').click(function(){
    var id= $(this).attr('pid').toString();
    var eml=this
    console.log(id)
    $.ajax({
        type:"GET",
        url:'/removecart',
        data:{
            prod_id:id
        },
        success:function(data){
            // console.log(data)
            // console.log('successs')
            // eml.innerText=data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('total_amount').innerText=data.total_amount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }

    })
    
})
