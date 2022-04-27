let menuButton = document.querySelector(".button-menu");
let container = document.querySelector(".container");
let pageContent = document.querySelector(".page-content");
const allpassGraph=document.getElementById('allpass');
let responsiveBreakpoint = 991;

if (window.innerWidth <= responsiveBreakpoint) {
  container.classList.add("nav-closed");
}

menuButton.addEventListener("click", function () {
  container.classList.toggle("nav-closed");
  allpassGraph.style.visibility='hidden';
});

pageContent.addEventListener("click", function () {
  if (window.innerWidth <= responsiveBreakpoint) {
    container.classList.add("nav-closed");
  }
});


window.addEventListener("resize", function () {
  if (window.innerWidth > responsiveBreakpoint) {
    container.classList.remove("nav-closed");
  }
});