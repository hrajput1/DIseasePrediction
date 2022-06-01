function predictFunction() {
  var dots = document.getElementById("predictdots");
  var moreText = document.getElementById("predictmore");
  var btnText = document.getElementById("predictmyBtn");

  if (dots.style.display === "none") {
    dots.style.display = "inline";
    btnText.innerHTML = "know more"; 
    moreText.style.display = "none";
  } else {
    dots.style.display = "none";
    btnText.innerHTML = "know less"; 
    moreText.style.display = "inline";
  }
}