$(document).ready(function() {
  $(".entry-toggle").click(function() {     
    $(this).siblings(".entry-content").slideToggle();
  });
});