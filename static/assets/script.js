$(document).ready(function(){

    /**
     * This object controls the nav bar. Implement the add and remove
     * action over the elements of the nav bar that we want to change.
     *
     * @type {{flagAdd: boolean, elements: string[], add: Function, remove: Function}}
     */
    var myNavBar = {
    
        flagAdd: true,
    
        elements: [],
    
        init: function (elements) {
            this.elements = elements;
        },
    
        add : function() {
            if(this.flagAdd) {
                for(var i=0; i < this.elements.length; i++) {
                    document.getElementById(this.elements[i]).className += " fixed-theme";
                }
                this.flagAdd = false;
            }
        },
    
        remove: function() {
            for(var i=0; i < this.elements.length; i++) {
                document.getElementById(this.elements[i]).className =
                        document.getElementById(this.elements[i]).className.replace( /(?:^|\s)fixed-theme(?!\S)/g , '' );
            }
            this.flagAdd = true;
        }
    
    };
    
    /**
     * Init the object. Pass the object the array of elements
     * that we want to change when the scroll goes down
     */
    myNavBar.init(  [
        "header",
        "header-container",
        "brand",
        "list",
        "user",
        "bout",
        "tact",
        "mat",
        "search",
        "cart"
    ]);

    
    
    
    /**
     * Function that manage the direction
     * of the scroll
     */
    function offSetManager(){
    
        var yOffset = 0;
        var currYOffSet = window.pageYOffset;
    
        if(yOffset < currYOffSet) {
            myNavBar.add();
        }
        else if(currYOffSet == yOffset){
            myNavBar.remove();
        }
    
    }
    
    /**
     * bind to the document scroll detection
     */
    window.onscroll = function(e) {
        offSetManager();
    }
    
    /**
     * We have to do a first detectation of offset because the page
     * could be load with scroll down set.
     */
    offSetManager();
});



// ...............................................
// image slider ...

let slideIndex = 0;
showSlides();

// Next-previous control
function nextSlide() {
  slideIndex++;
  showSlides();
  timer = _timer; // reset timer
}

function prevSlide() {
  slideIndex--;
  showSlides();
  timer = _timer;
}

// Thumbnail image controlls
function currentSlide(n) {
  slideIndex = n - 1;
  showSlides();
  timer = _timer;
}

function showSlides() {
  let slides = document.querySelectorAll(".mySlides");
  let dots = document.querySelectorAll(".dots");

  if (slideIndex > slides.length - 1) slideIndex = 0;
  if (slideIndex < 0) slideIndex = slides.length - 1;
  
  // hide all slides
  slides.forEach((slide) => {
    slide.style.display = "none";
  });

  
  // show one slide base on index number
  slides[slideIndex].style.display = "block";
  
  dots.forEach((dot) => {
    dot.classList.remove("active");
  });
  
  dots[slideIndex].classList.add("active");
}

// autoplay slides --------
let timer = 7; // sec
const _timer = timer;

// this function runs every 1 second
setInterval(() => {
  timer--;

  if (timer < 1) {
    nextSlide();
    timer = _timer; // reset timer
  }
}, 1000); // 1sec


// .........................
// about us

document.addEventListener("DOMContentLoaded", function() {
  console.log("DOM fully loaded"); // Debugging line

  const title = document.getElementById("about-title");
  
  if (!title) {
      console.error("Element with ID 'about-title' not found.");
      return;
  }

  function checkScroll() {
      const rect = title.getBoundingClientRect();
      
      if (rect.top < window.innerHeight * 0.75 && !title.classList.contains("show")) {
          console.log("Adding 'show' class to the title");
          title.classList.add("show");
          window.removeEventListener("scroll", checkScroll); // Ensures it runs only once
      }
  }

  window.addEventListener("scroll", checkScroll);
});



// ......................................................
// pillow_detail
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".add-to-cart-btn").forEach(button => {
      button.addEventListener("click", function (event) {
          event.preventDefault();
          let form = this.closest("form");
          let formData = new FormData(form);

          fetch(form.action, {
              method: "POST",
              body: formData,
              headers: {
                  "X-Requested-With": "XMLHttpRequest",
                  "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value
              }
          })
          .then(response => response.json())
          .then(data => {
              document.getElementById("cart-count").innerText = data.cart_count;
          });
      });
  });
});


