
console.log("This is a secret message ;)");
$(document).ready(function() {


   $('#about-me-par').mouseenter(function() {
       $(this).fadeTo('fast', 1);
   });

   $('#about-me-par').mouseleave(function() {
       $(this).fadeTo('fast', 0.2);
   });

   $('.group1').mouseenter(function() {
       $('#opening-quote1').fadeTo('fast', 0.8);
       $('#opening-quote2').delay(1200).fadeTo('fast', 0.8);
       $('#opening-quote3').delay(1200).fadeTo('slow', 0.8);
   });

   // $('.group1').mouseleave(function() {
   //    $('#opening-quote1').fadeTo('slow', 0);
   //    $('#opening-quote2').fadeTo('slow', 0);
   //    $('#opening-quote3').fadeTo('slow', 0);
   // });


   $('.group5').mouseenter(function() {
       $('#ending-quote1').fadeTo('slow', 0.8);
       $('#ending-quote2').delay(1200).fadeTo('slow', 0.8);
       $('#ending-quote3').delay(1500).fadeTo('slow', 0.8);
       $('#ending-quote3').delay(1800).fadeTo('slow', 0.8);
       $('#ending-quote4').delay(2100).fadeTo('slow', 0.8);
       $('#ending-quote5').delay(2100).fadeTo('slow', 0.8);
   });

   // $('.group5').mouseleave(function() {
   //     $('#ending-quote1').fadeTo('fast', 0);
   //     $('#ending-quote2').fadeTo('fast', 0);
   //     $('#ending-quote3').fadeTo('fast', 0);
   //     $('#ending-quote4').fadeTo('fast', 0);
   //     $('#ending-quote5').fadeTo('fast', 0);
   // });


   $('.project').mouseenter(function() {
       $(this).fadeTo('fast', 0.8);
   });

   $('.project').mouseleave(function() {
       $(this).fadeTo('fast', 0.1);
   });

   // $('div').mouseleave(function() {
   //     $(this).animate({
   //         height: '-=10px'
   //     }); 
   // });
   // $('div').click(function() {
   //     $(this).toggle(1000);
   // }); 
});

