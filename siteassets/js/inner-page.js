  // Hamburger Menu Js
var BASE_URL = window.location.origin + "/";

$(".hamb_open").click(function () {
  $(".hamburger_menu").addClass("active");
});

$(".close_hamb").click(function () {
  $(".hamburger_menu").removeClass("active");
});
$(".hamb_menu li a").click(function (e) {
  var same = $(this).hasClass("active");
  var siblings = $(this).parent(".hamb_drop").parent().children();
  siblings.find("a.active + .hamb_sub").slideUp();
  siblings.find("a").removeClass("active");
  if ($(this).next().hasClass("hamb_sub") && !same) {
    e.preventDefault();
    $(this).addClass("active");
    $(this).next(".hamb_sub").slideDown();
  }
});
  // Hamburger Menu Js end

    jQuery(function ($) {
    function scrollToHash(hash) {
        var target = $(hash);
        if (!target.length) return;
        $("html,body").animate({ scrollTop: target.offset().top - 150 },
            "linear"
        );
    }
    $('a[href*="#"]:not([href="#"]):not([data-open-enquiry])').click(function () {
        scrollToHash(this.hash);
    });
    $(window).on("load", function () {
        if (location.hash) {
            scrollToHash(location.hash);
        }
    });
});

  $(document).ready(function() {
	$('.popup-youtube').magnificPopup({
    type: 'iframe'
  });
});



if ($("[data-aos]").length) {
  AOS.init({
    easing: "ease-out-back",
    disable: function() {
      // Disable AOS if device width is smaller than 1024px
      return window.innerWidth < 1024;
    },
    duration: 2000,
    once: true
  });
}



    var Homeswiper = new Swiper(".students-alumni-slider", {
        loop: true,
        speed: 1500,
        slidesPerView: 4.5,
        spaceBetween: 16,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        breakpoints: {
             320: {
                slidesPerView: 1,
                spaceBetween: 16
            },
            480: {
                slidesPerView: 1,
                spaceBetween: 16
            },
            767: {
                slidesPerView: 1,
                spaceBetween: 16
            },
            991: {
                slidesPerView: 1.3,
                spaceBetween: 16
            },
            1199: {
                slidesPerView: 2.3,
                spaceBetween: 16
            }
        }
    });



    document.addEventListener('DOMContentLoaded', function () {
  // Initialize Swiper (or use your existing initialization)
  if (!document.querySelector('.students-learners')) return;
  var Homeswiper = new Swiper(".students-learners", {
    loop: true,
    speed: 1500,
    slidesPerView: 2,
    spaceBetween: 30,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      320: { slidesPerView: 1, spaceBetween: 16 },
      480: { slidesPerView: 1, spaceBetween: 16 },
      767: { slidesPerView: 1, spaceBetween: 16 },
      991: { slidesPerView: 2, spaceBetween: 25 },
      1199: { slidesPerView: 3, spaceBetween: 30 }
    }
  });

  // === Helper safely access autoplay API ===
  function autoplayStop() {
    if (Homeswiper && Homeswiper.autoplay && typeof Homeswiper.autoplay.stop === 'function') {
      Homeswiper.autoplay.stop();
      // console.log('[Swiper] autoplay stopped');
    }
  }
  function autoplayStart() {
    if (Homeswiper && Homeswiper.autoplay && typeof Homeswiper.autoplay.start === 'function') {
      Homeswiper.autoplay.start();
      // console.log('[Swiper] autoplay started');
    }
  }

  // Primary element returned by Swiper instance (most reliable)
  var primaryEl = (Homeswiper && Homeswiper.el) ? Homeswiper.el : document.querySelector('.students-learners');

  if (!primaryEl) {
    console.warn('Swiper container ".students-learners" not found.');
    return;
  }

  // Use pointer events (works for mouse + stylus + touch)
  primaryEl.addEventListener('pointerenter', autoplayStop);
  primaryEl.addEventListener('pointerleave', autoplayStart);

  // Also attach to wrapper & slides to catch events if an overlay or child blocks container
  if (Homeswiper && Homeswiper.wrapperEl) {
    Homeswiper.wrapperEl.addEventListener('pointerenter', autoplayStop);
    Homeswiper.wrapperEl.addEventListener('pointerleave', autoplayStart);
  }
  // Attach to each slide
  if (Homeswiper && Homeswiper.slides && Homeswiper.slides.length) {
    Homeswiper.slides.forEach(function(s){
      s.addEventListener('pointerenter', autoplayStop);
      s.addEventListener('pointerleave', autoplayStart);
    });
  }

  // Also pause when nav buttons are focused or hovered (accessibility)
  var navButtons = document.querySelectorAll('.swiper-button-next, .swiper-button-prev');
  navButtons.forEach(function(b){
    b.addEventListener('pointerenter', autoplayStop);
    b.addEventListener('pointerleave', autoplayStart);
    b.addEventListener('focus', autoplayStop);
    b.addEventListener('blur', autoplayStart);
  });

  // Pause on focus within slider (keyboard users)
  primaryEl.addEventListener('focusin', autoplayStop);
  primaryEl.addEventListener('focusout', autoplayStart);

  // Touch: stop on first touch to avoid conflicts with swipe
  primaryEl.addEventListener('touchstart', autoplayStop, {passive:true});

  // Optional: if something else stops autoplay (other code), ensure we can still resume on mouse leave:
  // Return to initial state when page/tab visibility changes
  document.addEventListener('visibilitychange', function(){
    if (document.visibilityState === 'visible') {
      // resume only if autoplay was running; safe to call start()
      autoplayStart();
    } else {
      autoplayStop();
    }
  });

 
});



 
//recruiter_slider

    var Homeswiper = new Swiper(".recruiter_slider", {
    loop: true,
    speed: 800,
    slidesPerView: 4,
    slidesPerGroup: 1, // ðŸ‘ˆ move 4 at once
    spaceBetween: 30,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
        type: "bullets",
    },
    // navigation: {
    //     nextEl: ".swiper-button-next",
    //     prevEl: ".swiper-button-prev",
    // },
    breakpoints: {
        0: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 16 },
        480: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 16 },
        575: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 16 },
        767: { slidesPerView: 2, slidesPerGroup: 1, spaceBetween: 16 },
        991: { slidesPerView: 3, slidesPerGroup: 1, spaceBetween: 16 },
        1199: { slidesPerView: 4, slidesPerGroup: 1, spaceBetween: 16 },
    }
});



document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.querySelector(".before-second-ul");
  const dropdown = document.querySelector(".second-ul");

  if (!toggleBtn || !dropdown) return; // safety check

  // show dropdown on hover
  toggleBtn.addEventListener("mouseenter", () => {
    dropdown.classList.add("show");
  });

  // hide dropdown when mouse leaves button or menu
  toggleBtn.addEventListener("mouseleave", () => {
    dropdown.classList.remove("show");
  });
  dropdown.addEventListener("mouseleave", () => {
    dropdown.classList.remove("show");
  });
  dropdown.addEventListener("mouseenter", () => {
    dropdown.classList.add("show");
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const toggleBtn = document.getElementById('toggle-btn');
  const programList = document.getElementById('program-list');

  if (!toggleBtn || !programList) {
    console.error("âŒ toggle-btn or program-list not found in the DOM");
    return;
  }

  toggleBtn.addEventListener('click', () => {
    programList.classList.toggle('expanded');
    toggleBtn.textContent = programList.classList.contains('expanded') ? "-" : "+";
  });
});

 // program baner Slider Start

    var Homeswiper = new Swiper(".program_baner_slider", {
        loop: true,
        effect: 'fade',
        autoplay: {
            delay: 3000,
            disableOnInteraction: false
        },
        speed: 800,
        slidesPerView: 1,
        spaceBetween: 0,
        navigation: {
            nextEl: ".home-next",
            prevEl: ".home-prev",
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            type: "bullets",
        },
        
        breakpoints: {
            768: { slidesPerView: 1, spaceBetween: 0,},
            1024: { slidesPerView: 1, spaceBetween: 0, },
        }
    });
    
var swiper = new Swiper(".logos_slider", {
      loop: true,
        speed: 800,
        slidesPerView: 4,
        spaceBetween: 20,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            type: "bullets",
        },
        breakpoints: {
        320: {
            slidesPerView: 1,
            spaceBetween: 10,
        },
        575: {
            slidesPerView: 2,
            spaceBetween: 10,
        },
        768: {
            slidesPerView: 3,
            spaceBetween: 20,
        },
        1200: {
            slidesPerView: 4,
            spaceBetween: 33,
        }
    }
    });

    // ---------about-page------

var swiper = new Swiper(".about-slider", {
      loop: true,
        speed: 800,
        slidesPerView: 1,
        spaceBetween: 10,
        effect: 'fade',
        autoplay: {
        delay: 3000,
        disableOnInteraction: false
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            type: "bullets",
        },
    });


// faculty_slider start here
document.addEventListener("DOMContentLoaded", function () {

    if (!document.querySelector(".faculty_slider")) return;
    var swiper = new Swiper(".faculty_slider", {
        slidesPerView: 4,
        spaceBetween: 33,
        loop: true,

        autoplay: {
            delay: 2500,
            disableOnInteraction: false,
            pauseOnMouseEnter: true
        },

        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },

        pagination: {
            el: ".swiper-pagination",
            type: "progressbar",
        },

        breakpoints: {
            320: { slidesPerView: 1.5, spaceBetween: 12, pagination: false },
            600: { slidesPerView: 2.5, spaceBetween: 12, pagination: false },
            768: { slidesPerView: 3, spaceBetween: 20 },
            1200: { slidesPerView: 4.95, spaceBetween: 20 }
        }
    });

    // ⛔ stop autoplay initially
    swiper.autoplay.stop();

    // ▶️ Start autoplay when visible
    const observer = new IntersectionObserver((entries, obs) => {
        if (entries[0].isIntersecting) {
            swiper.autoplay.start();
            obs.disconnect();
        }
    }, { threshold: 0.3 });

    observer.observe(document.querySelector(".faculty_slider"));
});






 var swiper = new Swiper(".inr-testimonial-slider", {
      slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
    navigation: {
      nextEl: '.text_btn_nxt',
      prevEl: '.text_btn_prev',
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
});


tabControl();

var resizeTimer;
$(window).on('resize', function(e) {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(function() {
    tabControl();
  }, 250);
});


$(document).ready(function() {
  // When any tab link is clicked
  $('.tabs a').on('click', function(event) {
    event.preventDefault();  // Prevent default anchor behavior

    // Get the target content ID from the href attribute
    var target = $(this).attr('href');

    // Remove the 'active' class from all tabs and all content items
    $('.tabs a').removeClass('active');
    $('.item').removeClass('active');

    // Add 'active' class to the clicked tab and the corresponding content
    $(this).addClass('active');
    $(target).addClass('active');

    console.log("Activated tab:", target); // Debugging: See which tab is clicked
  });
});






function tabControl() {
  var $tabsContainer = $('.faculty_tab');
  var isTabsVisible = $tabsContainer.find('.tabs_sec').is(':visible');

  // Unbind previous event handlers to avoid duplicates
  $tabsContainer.find('.tabs_sec a').off('click');
  $tabsContainer.find('.item_sec').off('click');

  if (isTabsVisible) {
    // Desktop: Tabs
    $tabsContainer.find('.tabs_sec a').on('click', function (event) {
      event.preventDefault();
      var target = $(this).attr('href');
      var $container = $(this).closest('.faculty_tab');

      $container.find('.tabs_sec a').removeClass('active');
      $container.find('.item_sec').removeClass('active');

      $(this).addClass('active');
      $container.find(target).addClass('active');
    });
  } else {
    // Mobile: Accordion
    $tabsContainer.find('.item_sec').on('click', function () {
      var $container = $(this).closest('.faculty_tab');
      var currId = $(this).attr('id');

      $container.find('.item_sec').removeClass('active');
      $container.find('.tabs_sec a').removeClass('active');

      $(this).addClass('active');
      $container.find('.tabs_sec a[href="#' + currId + '"]').addClass('active');
    });
  }
}

// Initial call
tabControl();

// Debounced resize
var resizeTimer;
$(window).on('resize', function () {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(function () {
    tabControl();
  }, 250);
});







var Homeswiper = new Swiper(".specialise-slider", {
        loop: true,
        speed: 1500,
        slidesPerView: 4.5,
        spaceBetween: 16,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            320: {
                slidesPerView: 1.5,
                spaceBetween: 16
            },
            480: {
                slidesPerView: 2,
                spaceBetween: 16
            },
            767: {
                slidesPerView: 2.5,
                spaceBetween: 16
            },
            991: {
                slidesPerView: 1.5,
                spaceBetween: 16
            },
            1199: {
                slidesPerView: 1.5,
                spaceBetween: 16
            },
            1449: {
                slidesPerView: 2.6,
                spaceBetween: 16
            },
            1920: {
                slidesPerView: 3.2,
                spaceBetween: 16
            }
        }
    });
var swiper = new Swiper(".begin-slider", {
        loop: true,
        speed: 1500,
        slidesPerView: 4.5,
        spaceBetween: 16,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            320: {
                slidesPerView: 1.5,
                spaceBetween: 16
            },
            480: {
                slidesPerView: 2,
                spaceBetween: 16
            },
            767: {
                slidesPerView: 2.5,
                spaceBetween: 16
            },
            991: {
                slidesPerView: 1.5,
                spaceBetween: 16
            },
            1199: {
                slidesPerView: 1.5,
                spaceBetween: 16
            },
            1649: {
                slidesPerView: 3.2,
                spaceBetween: 16
            },
            1920: {
                slidesPerView: 3.2,
                spaceBetween: 16
            }
        }
    });


    //about-slider-vision

    var Homeswiper = new Swiper(".about-slider-vision", {
        loop: true,
        speed: 800,
        slidesPerView: 4,
        spaceBetween: 30,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            type: "bullets",
        },
        breakpoints: {
             320: {
                slidesPerView: 1,
                spaceBetween: 16
            },
            480: {
                slidesPerView: 1,
                spaceBetween: 16
            },
             575: {
                slidesPerView: 1,
                spaceBetween: 16
            },
            767: {
                slidesPerView: 2,
                spaceBetween: 16
            },
            991: {
                slidesPerView: 3,
                spaceBetween: 16
            },
            1199: {
                slidesPerView: 4,
                spaceBetween: 16
            },
            1649: {
                slidesPerView: 4,
                spaceBetween: 16
            },
            1920: {
                slidesPerView: 4,
                spaceBetween: 16
            }
        }
    });



// function adjustContainerMaxWidth() {
//     let e = $(".container").width() + 15,
//         t = $("body").width();
//     t = t > 1920 ? 1920 : t;
//     let n = e + (t - e) / 2;
//     t >= 1400 ? ($(".max-content-xxl").css("max-width", `${n}px`), $(".max-content-xl").css("max-width", `${n}px`), $(".max-content-lg").css("max-width", `${n}px`), $(".max-content-md").css("max-width", `${n}px`), $(".max-content-sm").css("max-width", `${n}px`), $(".max-content").css("max-width", `${n}px`)) : t >= 1200 ? ($(".max-content-xxl").css("max-width", ""), $(".max-content-xl").css("max-width", `${n}px`), $(".max-content-lg").css("max-width", `${n}px`), $(".max-content-md").css("max-width", `${n}px`), $(".max-content-sm").css("max-width", `${n}px`), $(".max-content").css("max-width", `${n}px`)) : t >= 992 ? ($(".max-content-xxl").css("max-width", ""), $(".max-content-xl").css("max-width", ""), $(".max-content-lg").css("max-width", `${n}px`), $(".max-content-md").css("max-width", `${n}px`), $(".max-content-sm").css("max-width", `${n}px`), $(".max-content").css("max-width", `${n}px`)) : t >= 768 ? ($(".max-content-xxl").css("max-width", ""), $(".max-content-xl").css("max-width", ""), $(".max-content-lg").css("max-width", ""), $(".max-content-md").css("max-width", `${n}px`), $(".max-content-sm").css("max-width", `${n}px`), $(".max-content").css("max-width", `${n}px`)) : t >= 575 ? ($(".max-content-xxl").css("max-width", ""), $(".max-content-xl").css("max-width", ""), $(".max-content-lg").css("max-width", ""), $(".max-content-md").css("max-width", ""), $(".max-content-sm").css("max-width", `${n}px`), $(".max-content").css("max-width", `${n}px`)) : ($(".max-content-xxl").css("width", ""), $(".max-content-xl").css("width", ""), $(".max-content-lg").css("width", ""), $(".max-content-md").css("width", ""), $(".max-content-sm").css("width", ""), $(".max-content").css("width", `${n}px`))
// }







 // tabbed content
    // http://www.entheosweb.com/tutorials/css/tabs.asp
    $(".tabs_prog_wrapper").hide();
    $(".tabs_prog_wrapper:first").show();

  /* if in tab mode */
    $(".tabs_program_nav li").click(function() {
		
      $(".tabs_prog_wrapper").hide();
      var activeTab = $(this).attr("rel"); 
      $("#"+activeTab).fadeIn();		
		
      $(".tabs_program_nav li").removeClass("active");
      $(this).addClass("active");

	  $(".tab_drawer_heading").removeClass("d_active");
	  $(".tab_drawer_heading[rel^='"+activeTab+"']").addClass("d_active");
	  
    /*$(".tabs").css("margin-top", function(){ 
       return ($(".tab_container").outerHeight() - $(".tabs").outerHeight() ) / 2;
    });*/
    });
    $(".tab_container").css("min-height", function(){ 
      return $(".tabs").outerHeight() + 50;
    });
	/* if in drawer mode */
	$(".tab_drawer_heading").click(function() {
      
      $(".tabs_prog_wrapper").hide();
      var d_activeTab = $(this).attr("rel"); 
      $("#"+d_activeTab).fadeIn();
	  
	  $(".tab_drawer_heading").removeClass("d_active");
      $(this).addClass("d_active");
	  
	  $(".tabs_program_nav li").removeClass("active");
	  $("tabs_program_nav li[rel^='"+d_activeTab+"']").addClass("active");
    });
	
	
	/* Extra class "tab_last" 
	   to add border to bottom side
	   of last tab 
	$('ul.tabs li').last().addClass("tab_last");*/
	
$(function () {
    function isMobile() {
      return window.innerWidth <= 768;
    }

    $('.tabs').each(function () {
      const $tabs = $(this);

      // Desktop tab button click
      $tabs.find('.tab-buttons button').on('click', function () {
        if (!isMobile()) {
          const tabId = $(this).data('tab');

          $tabs.find('.tab-buttons button').removeClass('active');
          $(this).addClass('active');

          $tabs.find('.tab-content').removeClass('active');
          $tabs.find('#' + tabId).addClass('active');
        }
      });

      // Mobile accordion click
      $tabs.find('.accordion-header').on('click', function () {
        if (isMobile()) {
          const $parent = $(this).closest('.tab-content');
            
          if ($parent.hasClass('active')) {
            $parent.removeClass('active');
          } else {
            $tabs.find('.tab-content').removeClass('active');
            $parent.addClass('active');
          }
        }
      });
    });

  });

  //highlights-slider----------

        var Homeswiper = new Swiper(".highlights-slider", {
            loop: true,
            speed: 1500,
            slidesPerView: 4.5,
            spaceBetween: 16,
            // autoplay: {
            //     delay: 3000,
            //     disableOnInteraction: false
            // },
            autoplay: false, // This disables autoplay
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                320: {
                    slidesPerView: 1,
                    spaceBetween: 16
                },
                480: {
                    slidesPerView: 1,
                    spaceBetween: 16
                },
                600: {
                    slidesPerView: 1.2 ,
                    spaceBetween: 16
                },
                767: {
                    slidesPerView: 2,
                    spaceBetween: 16
                },
                1199: {
                    slidesPerView: 2,
                    spaceBetween: 16
                },
                1280: {
                    slidesPerView: 3,
                    spaceBetween: 16
                },
                1449: {
                    slidesPerView: 3.3,
                    spaceBetween: 16
                },
                1649: {
                    slidesPerView: 3.2,
                    spaceBetween: 16
                },

            }
        });
	

        document.addEventListener("DOMContentLoaded", function () {
    const trigger = document.querySelector(".triger_icon");
    const banner = document.querySelector(".banner_form");

    if (trigger && banner) {
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        banner.classList.toggle("active");
        console.log("clicked!"); // debug
      });
    } else {
      console.error("Element not found!");
    }
  });

  
//-----------Load More----

// const toggleBtn = document.getElementById("toggleBtn");
//   const moreContent = document.getElementById("moreContent");

//   let expanded = false;

//   toggleBtn.addEventListener("click", () => {
//     expanded = !expanded;

//     if (expanded) {
//       moreContent.style.maxHeight = moreContent.scrollHeight + "px";
//       toggleBtn.textContent = "Load Less";
//     } else {
//       moreContent.style.maxHeight = "0";
//       toggleBtn.textContent = "Load More";
//     }
//   });

  document.addEventListener("DOMContentLoaded", function () {
  // Loop through all student-text blocks
  document.querySelectorAll('.student-text').forEach(block => {
    const content = block.querySelector('.student-content');
    const button = block.querySelector('.read-more-btn');

    // If content or button doesn't exist, skip
    if (!content || !button) return;

    // Count all paragraphs inside .student-content
    const paragraphCount = content.querySelectorAll('p').length;

    // Hide button if there are 1 or 2 paragraphs
    if (paragraphCount <= 2) {
      button.style.display = 'none';
    } else {
      // Otherwise, show button
      button.style.display = 'inline-flex';
    }
  });
});

	
$(document).ready(function() {
  $('.moreless-button_3').click(function() {
    // Toggle the hidden text
    $('.moretext_3').slideToggle();

    // Define your icon paths
    const plusIcon = '<img src="'+BASE_URL+'siteassets/images/h-minus-icon.svg" alt="Read more" />';
    const minusIcon = '<img src="'+BASE_URL+'siteassets/images/h-pluse-icon.svg" alt="Read less" />';

    // Toggle icons based on active state
    if ($(this).hasClass('active')) {
      $(this).removeClass('active').html(plusIcon);
    } else {
      $(this).addClass('active').html(minusIcon);
    }
  });
});




// ===============Program videos============

document.addEventListener("DOMContentLoaded", function () {

    const video = document.getElementById("courseVideo");
    const button = document.querySelector(".video_play_btn");
    const thumbnail = document.querySelector(".vimeo_thumbnail");

    if (!video || !button) return;

    // Load Vimeo API
    const vimeoScript = document.createElement("script");
    vimeoScript.src = BASE_URL + "_external/player.vimeo.com/api/player.js";

    vimeoScript.onload = function () {

        const player = new Vimeo.Player(video);

        // Play
        player.on("play", function () {

            button.classList.add("playing");

            button.setAttribute(
                "aria-label",
                "Pause video"
            );

            // Hide thumbnail
            if (thumbnail) {
                thumbnail.classList.add("hide");
            }
        });

        // Pause
        player.on("pause", function () {

            button.classList.remove("playing");

            button.setAttribute(
                "aria-label",
                "Play video"
            );
        });

        // End
        player.on("ended", function () {

            button.classList.remove("playing");

            button.setAttribute(
                "aria-label",
                "Play video"
            );

            if (thumbnail) {
                thumbnail.classList.remove("hide");
            }
        });


        // Button click
        button.addEventListener("click", function () {

            player.getPaused().then(function (paused) {

                if (paused) {
                    player.play().catch(function (error) {
                        console.log("Vimeo play error:", error);
                    });
                } else {
                    player.pause();
                }

            });

        });

    };

    document.head.appendChild(vimeoScript);

});



// =============page load popup=============

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("videoModal");
    const closeBtn = document.querySelector(".close-btn");
    const iframe = document.getElementById("youtubeVideo");
    if (!modal || !closeBtn || !iframe) return;

    // Show popup
    modal.style.display = "flex";

    // Close popup and stop video
    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";

        // Stop the video
        iframe.src = "";
    });
});






  