$(".input-container input").blur(function (event) {
    var inputVal = this.value;

    if (inputVal) {
      this.classList.add("value-exists");
    } else {
      this.classList.remove("value-exists");
    }
  });

 setTimeout(function () {
   $(".content").fadeToggle();
 }, 5500);

 $(document).ready(function() {
  $("#second").hide();
  $("#second").delay(5500).fadeIn(500);
});
