
// UIAP 02011995
  // -----------search-------
  function openSearch() {
    document.getElementById("myOverlay").style.display = "block";
  }
  
  function closeSearch() {
    document.getElementById("myOverlay").style.display = "none";
  }
  
(function ($) {
  "use strict";

  document.addEventListener('DOMContentLoaded', function () {
    adjustBodyPadding();
    adjustMenuPadding();
    AOS.init();

    // Sticky Header
    const sticky = $(".main_header");
    $(window).on("scroll", function () {
      sticky.toggleClass("sticky", $(this).scrollTop() > 0);
    });


  });


   

  // Responsive Padding Adjustments
  function adjustBodyPadding() {
    const body = document.querySelector('.main');
    const isDesktop = window.innerWidth >= 260;
    const header = document.querySelector(isDesktop ? '.top_header' : '.main_header');
    if (header && body) {
      setTimeout(() => {
        body.style.paddingTop = header.offsetHeight + 'px';
      }, 100);
    }
  }

  function adjustMenuPadding() {
    const header = document.querySelector('.mobile_menu_list');
    const bodies = document.querySelectorAll('.mobile-menu-panel');

    if (header && bodies.length) {
      setTimeout(() => {
        const headerHeight = header.offsetHeight;
        bodies.forEach(menu => {
          menu.style.paddingBottom = headerHeight + 'px';
        });
      }, 100);
    }
  }


  window.addEventListener('load', () => {
    adjustBodyPadding();
    adjustMenuPadding();
  });
  window.addEventListener('resize', () => {
    adjustBodyPadding();
    adjustMenuPadding();
  });

  // GSAP Reveal on Scroll (only for desktop)

  if (window.innerWidth >= 992) {
    function revealImages() {
      const images = [
        { class: '.image', reveal: 'reveal-image' },
        { class: '.image2', reveal: 'reveal-image2' },
        { class: '.image3', reveal: 'reveal-image3' }
      ];

      images.forEach(({ class: selector, reveal }) => {
        document.querySelectorAll(selector).forEach(el => {
          const rect = el.getBoundingClientRect();
          if (rect.top < (window.innerHeight - 200)) {
            el.classList.add(reveal);
          }
        });
      });
    }

    window.addEventListener('load', revealImages);
    window.addEventListener('scroll', revealImages);
    window.addEventListener('resize', revealImages);

    if ($("[data-aos]").length) {
      AOS.init({
        easing: "ease-out-back",
        disable: "mobile",
        duration: 2000,
        once: true
      });
    }    
  } 





//----program-tab----

$(document).ready(function () {
  function isMobile() {
    return $(window).width() <= 992;
  }

  function showTab($container, tabId) {
    $container.find('.tab-content').removeClass('active');
    $container.find('#' + tabId).addClass('active');
  }

  $('.tabs-container').each(function () {
    var $container = $(this);

    // Default: first tab active in each container (only on desktop)
    if (!isMobile()) {
      $container.find('.tab-content').removeClass('active');
      $container.find('.tab-content').first().addClass('active');
      $container.find('.tab-btn').removeClass('active');
      $container.find('.tab-btn').first().addClass('active');
    }

    // Tab button click
    $container.find('.tab-btn').on('click touchstart', function (e) {
      e.preventDefault();
      var tabId = $(this).data('tab');

      $container.find('.tab-btn').removeClass('active');
      $(this).addClass('active');
      showTab($container, tabId);
    });

    // Accordion behavior for mobile
    $container.find('.tab-header').on('click touchstart', function () {
      var $tabContent = $(this).closest('.tab-content');

      if ($tabContent.hasClass('active')) {
        $tabContent.removeClass('active');
      } else {
        $container.find('.tab-content').removeClass('active');
        $tabContent.addClass('active');
      }
    });
  });
});

var BASE_URL = window.location.origin + "/";


function setupReadMore() {
    const readBtn = document.querySelector('.load_btn');
    const orgText = document.querySelector('.org_text');
    const icon = document.getElementById('toggle-icon');

    if (!readBtn || !orgText) return;

    readBtn.addEventListener('click', function () {
      const isExpanded = orgText.classList.toggle('expanded_new');
      orgText.classList.toggle('hidden', !isExpanded);

      // Optional: change icon if you have a different one for "Read Less"
     if (icon) {
        icon.src = isExpanded
          ? ''+BASE_URL+'siteassets/images/minus-circle.svg'
          : ''+BASE_URL+'siteassets/images/plus-circle.svg';
      }

    });
  }

  // Initialize after DOM is ready
  document.addEventListener('DOMContentLoaded', setupReadMore);





 //-----------faculty-video-----
$(document).ready(function () {

  function getSwiperInstance() {
    const el = document.querySelector(".faculty_slider");
    return el && el.swiper ? el.swiper : null;
  }

  /* ==================================================
     ▶️ PLAY TRIGGER
     ================================================== */
  $(document).on(
    "click",
    ".faculty_slider .faculty_item a, .faculty_listing_main .faculty_item .f_link",
    function (e) {
      e.preventDefault();

      const $item  = $(this).closest(".faculty_item");
      const $video = $item.find(".video");
      if (!$video.length) return;

      // Inject buttons once
      if (!$item.find(".video-close").length) {
        $item.css("position", "relative").append(`
          <button class="video-close">✕</button>
          <button class="video-toggle pause">⏸</button>
        `);
      }

      // Stop all videos
      $(".faculty_item .video").each(function () {
        this.pause();
        this.currentTime = 0;
        $(this).hide().removeClass("video_open");
      });

      $(".video-toggle").text("▶").hide();
      $(".video-close").hide();

      // ▶️ PLAY VIDEO (UNCHANGED)
      const videoEl = $video
        .prop("controls", false)
        .addClass("video_open")
        .show()[0];

      videoEl.play();

      // 🛑 STOP SWIPER AUTOPLAY (BULLETPROOF)
      const swiper = getSwiperInstance();
      if (swiper && swiper.autoplay) {
        swiper.autoplay.stop();
      }

      $item.find(".video-toggle").text("⏸").show();
      $item.find(".video-close").show();
    }
  );

  /* ==================================================
     ⏯ PLAY / PAUSE
     ================================================== */
  $(document).on("click", ".video-toggle", function () {
    const $btn = $(this);
    const video = $btn.closest(".faculty_item").find(".video")[0];
    if (!video) return;

    const swiper = getSwiperInstance();

    if (video.paused) {
      video.play();
      $btn.text("⏸");

      if (swiper && swiper.autoplay) {
        swiper.autoplay.stop();
      }
    } else {
      video.pause();
      $btn.text("▶");

      if (swiper && swiper.autoplay) {
        swiper.autoplay.start();
      }
    }
  });


const mobileView = window.matchMedia("(max-width: 992px)");

if (mobileView.matches && document.querySelector(".apply_btn_button:not([data-open-enquiry])") && document.querySelector(".banner_form")) {

    const applyBtn = document.querySelector(".apply_btn_button");
    const bannerForm = document.querySelector(".banner_form");

    applyBtn.addEventListener("click", function(e){
        e.preventDefault();
        e.stopPropagation();

        bannerForm.classList.toggle("active");

        // 👉 Scroll ONLY when opening
        if (bannerForm.classList.contains("active")) {

            const offset = 100; // adjust if you have sticky header
            const formPosition = bannerForm.getBoundingClientRect().top + window.pageYOffset;

            window.scrollTo({
                top: formPosition - offset,
                behavior: "smooth"
            });
        }
    });

    // Prevent closing when clicking inside form
    bannerForm.addEventListener("click", function(e){
        e.stopPropagation();
    });

    // Outside click close
    document.addEventListener("click", function(){
        bannerForm.classList.remove("active");
    });

}


window.addEventListener("load", function() {
    const bannerForm = document.querySelector(".banner_form");
    if (bannerForm) bannerForm.style.visibility = "visible";
});







  /* ==================================================
     ❌ CLOSE VIDEO
     ================================================== */
  $(document).on("click", ".video-close", function () {
    const $item = $(this).closest(".faculty_item");
    const video = $item.find(".video")[0];

    if (video) {
      video.pause();
      video.currentTime = 0;
    }

    $item.find(".video").hide().removeClass("video_open");
    $item.find(".video-toggle, .video-close").hide();

    // ▶️ RESUME SWIPER
    const swiper = getSwiperInstance();
    if (swiper && swiper.autoplay) {
      swiper.autoplay.start();
    }
  });

});






//-----mega-tabs------

document.addEventListener("DOMContentLoaded", function () {
  const tabButtons = document.querySelectorAll(".mega-tab-btn");
  const tabContents = document.querySelectorAll(".mega-tab-content");

  tabButtons.forEach(button => {
    button.addEventListener("mouseenter", function () {
      const tabId = this.getAttribute("data-tab");

      // Remove all active classes
      tabButtons.forEach(btn => btn.classList.remove("active"));
      tabContents.forEach(content => content.classList.remove("active"));

      // Add active class to hovered button and related content
      this.classList.add("active");
      document.getElementById(tabId).classList.add("active");
    });
  });

  // Show the first tab by default
  if (tabButtons.length > 0 && tabContents.length > 0) {
    tabButtons[0].classList.add("active");
    tabContents[0].classList.add("active");
  }
});


// ------accordion------
document.addEventListener('DOMContentLoaded', function () {

  document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', function () {

      const item = this.closest('.accordion-item');
      const body = item.querySelector('.accordion-body');
      const isActive = item.classList.contains('active');

      // Close all others
      document.querySelectorAll('.accordion-item').forEach(other => {
        if (other !== item) {
          other.classList.remove('active');
          const otherBody = other.querySelector('.accordion-body');
          if (otherBody) otherBody.style.maxHeight = null;
        }
      });

      // Toggle current
      if (isActive) {
        item.classList.remove('active');
        body.style.maxHeight = null;
      } else {
        item.classList.add('active');
        body.style.maxHeight = body.scrollHeight + 'px';
      }
    });
  });

  // Keep active open on load
  const activeBody = document.querySelector('.accordion-item.active .accordion-body');
  if (activeBody) {
    activeBody.style.maxHeight = activeBody.scrollHeight + 'px';
  }
});

//-------select--------
$(document).ready(function () {
  const $selectTrigger = $('#select-trigger');
  const $optionsContainer = $('#options-container');
  const $options = $('.custom-option');

  // Toggle dropdown visibility when selectTrigger is clicked
  $selectTrigger.on('click', function () {
    $optionsContainer.toggle();
  });

  // Option selection
  $options.on('click', function () {
    const selectedText = $(this).text();
    $selectTrigger.text(selectedText);
    
    // Remove 'selected' class from all options and add to clicked option
    $options.removeClass('selected');
    $(this).addClass('selected');
    
    // Hide the options container
    $optionsContainer.hide();
  });

  // Close the dropdown if clicking outside
  $(document).on('click', function (e) {
    if (!$(e.target).closest('.custom-select-wrapper').length) {
      $optionsContainer.hide();
    }
  });
});


$(document).ready(function () {
  $('.mega-menu').hover(
    function () {
      // Mouse enters mega menu
      $("body").addClass('mega_bg');
    },
    function () {
      // Mouse leaves mega menu
      $("body").removeClass('mega_bg');
      $("body").removeClass('mega_close');
    }
  );
  $('.mega-close').on("click", function () {
    $("body").addClass('mega_close');
  },
);
});







// Scroll back to top
    // var progressPath = document.querySelector(".progress-wrap path");
    // var pathLength = progressPath.getTotalLength();

    // progressPath.style.transition = progressPath.style.WebkitTransition = "none";
    // progressPath.style.strokeDasharray = pathLength + " " + pathLength;
    // progressPath.style.strokeDashoffset = pathLength;
    // progressPath.getBoundingClientRect();
    // progressPath.style.transition = progressPath.style.WebkitTransition = "stroke-dashoffset 10ms linear";

    // var updateProgress = function () {
    //     var scroll = $(window).scrollTop();
    //     var height = $(document).height() - $(window).height();
    //     var progress = pathLength - (scroll * pathLength) / height;
    //     progressPath.style.strokeDashoffset = progress;
    // };

    // updateProgress();
    // $(window).scroll(updateProgress);

    // var offset = 50;
    // var duration = 550;

    // jQuery(window).on("scroll", function () {
    //     if (jQuery(this).scrollTop() > offset) {
    //         jQuery(".progress-wrap").addClass("active-progress");
    //     } else {
    //         jQuery(".progress-wrap").removeClass("active-progress");
    //     }
    // });

    // jQuery(".progress-wrap").on("click", function (event) {
    //     event.preventDefault();
    //     jQuery("html, body").animate({ scrollTop: 0 }, duration);
    //     return false;
    // });


      $(document).ready(function() {
              $('.modal-link:not([data-open-enquiry])').on('click', function() {
              $('body').addClass("modal-open");
          });
          $('.close-modal').on('click', function() {
              $('body').removeClass("modal-open");
          });
      });

      $(document).ready(function() {
              $('.modal-link2:not([data-open-enquiry])').on('click', function() {
              $('body').addClass("modal-open2");
          });
          $('.close-modal2').on('click', function() {
              $('body').removeClass("modal-open2");
          });
      });

})(jQuery);





$('.menu-button').on('click', function () {
  let target = $(this).data('target'); console.log(target)
  if ($(this).hasClass('active')) { $(this).removeClass('active'); $(target).removeClass('show') } else {
      $(this).siblings('.menu-button').removeClass('active')
      $(this).addClass('active'); $('.mobile-menu.show').removeClass('show'), $(target).addClass('show')
  }
})




// Select all spans inside your counter_section
const counters = document.querySelectorAll('.counter_section ul li span');
const counterSection = document.querySelector('.counter_section');

function startCounting() {
  counters.forEach(span => {
    const text = span.textContent.trim();
    const regex = /^(\d+)([KM]?)$/i;
    const match = text.match(regex);

    if (!match) return;

    const baseNumber = parseInt(match[1], 10);
    const suffix = match[2].toUpperCase();

    let target = baseNumber;
    if (suffix === 'K') target = baseNumber * 1000;
    else if (suffix === 'M') target = baseNumber * 1000000;

    let count = 0;
    const duration = 2000;
    const intervalTime = 20;
    const steps = duration / intervalTime;
    const increment = target / steps;

    span.textContent = '0' + suffix;

    const counter = setInterval(() => {
      count += increment;
      if (count >= target) {
        count = target;
        clearInterval(counter);
      }

      let displayNumber = count;
      if (suffix === 'K') displayNumber = Math.floor(count / 1000);
      else if (suffix === 'M') displayNumber = Math.floor(count / 1000000);
      else displayNumber = Math.floor(count);

      span.textContent = displayNumber + suffix;
    }, intervalTime);
  });
}

// Intersection Observer to detect when counter_section enters viewport
const observer = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      startCounting();
      observer.unobserve(entry.target); // Run once and stop observing
    }
  });
}, { threshold: 0.1 }); // 10% visible

if (counterSection) observer.observe(counterSection);




const video = document.getElementById("alumniVideo");
const soundBtn = document.getElementById("soundToggle");

if (video instanceof HTMLVideoElement && soundBtn) {
video.muted = true;
soundBtn.innerHTML = "🔇";

soundBtn.addEventListener("click", () => {
  video.muted = !video.muted;
  soundBtn.innerHTML = video.muted ? "🔇" : "🔊";
});
}



