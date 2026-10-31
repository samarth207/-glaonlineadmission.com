
// UIAP 02011995
(function ($) {
    "use strict"; 
    adjustMaxContent();
    
 const doItNow = (evt, hard) => {
      const direction = Math.sign(lastX - evt.clientX);
      lastX = evt.clientX;
      const particleCount = hard ? r(122, 245) : r(2, 15);
      confetti({
        particleCount,
        angle: r(90, 90 + direction * 30),
        spread: r(45, 80),
        origin: {
          x: evt.clientX / window.innerWidth,
          y: evt.clientY / window.innerHeight
        }
      });
    };

  

    const doIt = (evt) => doItNow(evt, false);
    const doItHard = (evt) => doItNow(evt, true);

    let lastX = 0;

    function r(mi, ma) {
      return parseInt(Math.random() * (ma - mi) + mi);
    }

    document.addEventListener("DOMContentLoaded", () => {
      const target = document.querySelector(".cntre_img");
      if (target) {
        target.addEventListener("mousemove", doIt);
        target.addEventListener("click", doItHard);
      } else {
        console.warn("Element .cntre_img not found.");
      }
    });

    // Home Slider Start

    var Homeswiper = new Swiper(".home_slider", {
        loop: true,
        effect: 'fade',
        autoplay: {
            delay:3000,
            disableOnInteraction: false
        },
        speed: 2000,
        slidesPerView: 1,
        spaceBetween: 0,
        navigation: {
            nextEl: ".home-next",
            prevEl: ".home-prev",
        },
        pagination: {
            el: ".home-swiper-pagination",
            clickable: true,
            type: "bullets",
        },
        
        breakpoints: {
            768: { slidesPerView: 1, spaceBetween: 0,},
            1024: { slidesPerView: 1, spaceBetween: 0, },
        }
    });


    //recruiter_slider

    var Homeswiper = new Swiper(".recruiter_slider", {
    loop: true,
    speed: 800,
    slidesPerView: 4,
    slidesPerGroup: 4, // 👈 move 4 at once
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
        320: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 16 },
        480: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 16 },
        575: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 16 },
        767: { slidesPerView: 2, slidesPerGroup: 2, spaceBetween: 16 },
        991: { slidesPerView: 3, slidesPerGroup: 3, spaceBetween: 16 },
        1199: { slidesPerView: 4, slidesPerGroup: 4, spaceBetween: 16 },
    }
});




//meet the master slider

    var Homeswiper = new Swiper(".master_slider", {
    loop: true,
    speed: 800,
    slidesPerView: 3,
    slidesPerGroup: 1, // 👈 move 4 at once
    spaceBetween: 30,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false
    },
    navigation: {
        nextEl: ".master-next",
        prevEl: ".master-prev",
    },
    // navigation: {
    //     nextEl: ".swiper-button-next",
    //     prevEl: ".swiper-button-prev",
    // },
    breakpoints: {
        320: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 16 },
        414: { slidesPerView: 2, slidesPerGroup: 1, spaceBetween: 16 },
        575: { slidesPerView: 2, slidesPerGroup: 1, spaceBetween: 16 },
        767: { slidesPerView: 3, slidesPerGroup: 1, spaceBetween: 16 },
        991: { slidesPerView: 2, slidesPerGroup: 1, spaceBetween: 16 },
        1199: { slidesPerView: 3, slidesPerGroup: 1, spaceBetween: 16 },
    }
});


  var Homeswiper = new Swiper(".recruiter_slider_new", {
  loop: true,
  speed: 800,
  slidesPerView: 3,
  slidesPerGroup: 1,
  spaceBetween: 30,

  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
    pauseOnMouseEnter: true
  },

  /* ===== Desktop pagination ===== */
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
    type: "bullets",
    enabled: true
  },

  /* ===== Desktop navigation (off by default) ===== */
  navigation: {
    nextEl: ".recruiter-button-next",
    prevEl: ".recruiter-button-prev",
    enabled: false
  },


  

  breakpoints: {
    /* 📱 Mobile */
    0: {
      slidesPerView: 1,
      slidesPerGroup: 1,
      spaceBetween: 16,
      pagination: { enabled: false },
      navigation: { enabled: true }
    },

    575: {
      slidesPerView: 1,
      slidesPerGroup: 1,
      spaceBetween: 16,
      pagination: { enabled: false },
      navigation: { enabled: true }
    },

    /* 📱 Tablet */
    767: {
      slidesPerView: 2,
      slidesPerGroup: 2,
      spaceBetween: 16,
      pagination: { enabled: true },
      navigation: { enabled: false }
    },

    /* 💻 Desktop */
    991: {
      slidesPerView: 3,
      slidesPerGroup: 1,
      spaceBetween: 16,
      pagination: { enabled: true },
      navigation: { enabled: false }
    }
  }
});

/* ===== Autoplay hover fix ===== */
const sliderEl = document.querySelector('.recruiter_slider_new');
if (sliderEl && Homeswiper?.autoplay) {
  sliderEl.addEventListener('mouseenter', () => Homeswiper.autoplay.stop());
  sliderEl.addEventListener('mouseleave', () => Homeswiper.autoplay.start());
}



 let swiperInitialized = false;


const sliderSection = document.querySelector('.people_slider');

const observer = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !swiperInitialized) {
      swiperInitialized = true;

      // Initialize Swiper
      var Homeswiper = new Swiper(".people_slider", {
        loop: true,
        speed: 800,
        slidesPerView: 2,
        slidesPerGroup: 1, // 👈 move 4 at once
        spaceBetween: 30,   
        autoplay: {
            delay: 3000,
            disableOnInteraction: false
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
            320: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 25 },
            480: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 25 },
            575: { slidesPerView: 1, slidesPerGroup: 1, spaceBetween: 25 },
            767: { slidesPerView: 2, slidesPerGroup: 1, spaceBetween: 25 },
            991: { slidesPerView: 2.1, slidesPerGroup: 1, spaceBetween: 25 },
            1199: { slidesPerView: 2.1, slidesPerGroup: 1, spaceBetween: 25 },
        }
      });

    // Pause on hover / Resume on leave
      const sliderEl = document.querySelector('.people_slider');

      sliderEl.addEventListener('mouseenter', () => {
        Homeswiper.autoplay.stop();
      });

      sliderEl.addEventListener('mouseleave', () => {
        Homeswiper.autoplay.start();
      });


      // Stop observing after initialization
      observer.unobserve(sliderSection);
    }
  });
}, { threshold: 0.1 }); // 10% visible triggers it

observer.observe(sliderSection);



    document.addEventListener('DOMContentLoaded', function () {
  var Homeswiper = new Swiper(".gharse_globle", {
    loop: true,
    speed: 1500,
    slidesPerView: 1,
    spaceBetween: 0,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false
    },
    effect: 'fade',
    fadeEffect: { crossFade: true },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      320: { slidesPerView: 1 },
      480: { slidesPerView: 1 },
      767: { slidesPerView: 1 },
      991: { slidesPerView: 1 },
      1199:{ slidesPerView: 1 }
    }
  });


  // Use the actual element from the Swiper instance
  var swiperEl = Homeswiper.el || document.querySelector('.gharse_globle');

  if (!swiperEl) {
    console.warn('Swiper element not found.');
    return;
  }

  function debug(msg){ try{ console.log('[Swiper-hover] ' + msg); } catch(e){} }

  // Pause on mouse enter / resume on leave
  swiperEl.addEventListener('mouseenter', function () {
    debug('mouseenter -> stop autoplay');
    if (Homeswiper && Homeswiper.autoplay && Homeswiper.autoplay.stop) Homeswiper.autoplay.stop();
  });
  swiperEl.addEventListener('mouseleave', function () {
    debug('mouseleave -> start autoplay');
    if (Homeswiper && Homeswiper.autoplay && Homeswiper.autoplay.start) Homeswiper.autoplay.start();
  });

  // Also pause on focus (keyboard users) and resume on blur
  swiperEl.addEventListener('focusin', function () {
    debug('focusin -> stop autoplay');
    if (Homeswiper && Homeswiper.autoplay && Homeswiper.autoplay.stop) Homeswiper.autoplay.stop();
  });
  swiperEl.addEventListener('focusout', function () {
    debug('focusout -> start autoplay');
    if (Homeswiper && Homeswiper.autoplay && Homeswiper.autoplay.start) Homeswiper.autoplay.start();
  });

  // On touch devices: optionally stop on touchstart to avoid conflict with swipe
  swiperEl.addEventListener('touchstart', function () {
    debug('touchstart -> stop autoplay (touch)');
    if (Homeswiper && Homeswiper.autoplay && Homeswiper.autoplay.stop) Homeswiper.autoplay.stop();
  });

  // If an overlay or child element intercepts mouse, try adding listeners to that element too:
  // document.querySelectorAll('.gharse_globle *').forEach(el => {
  //   el.addEventListener('mouseenter', () => Homeswiper.autoplay.stop());
  //   el.addEventListener('mouseleave', () => Homeswiper.autoplay.start());
  // });

  debug('hover handlers attached to Swiper element.');
});



    let HomeSwiperInstance = null;

function initOrDestroySwiper() {
    const screenWidth = window.innerWidth;
    if (screenWidth > 991 && HomeSwiperInstance === null) {
        HomeSwiperInstance = new Swiper(".why_gla", {
            loop: true,
            speed: 1500,
            slidesPerView: 4.5,
            spaceBetween: 16,
            autoplay: {
                delay: 3000,
                disableOnInteraction: false
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
                type: "bullets"
            },
            breakpoints: {
                992: {
                    slidesPerView: 3,
                    spaceBetween: 16
                },
                1199: {
                    slidesPerView: 6,
                    spaceBetween: 16
                },
                1649: {
                    slidesPerView: 6,
                    spaceBetween: 16
                },
                1920: {
                    slidesPerView: 6,
                    spaceBetween: 16
                }
            }
        });
    } else if (screenWidth <= 991 && HomeSwiperInstance !== null) {
        HomeSwiperInstance.destroy(true, true);
        HomeSwiperInstance = null;
    }
}

// Run on load
initOrDestroySwiper();

// Run on resize
window.addEventListener("resize", () => {
    initOrDestroySwiper();
});

   


    //testimonial-video

    var Homeswiper = new Swiper(".testimonial_video_slider", {
        loop: true,
        speed: 800,
        slidesPerView: 1,
        spaceBetween: 10,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
            type: "bullets",
        },
        // breakpoints: {
        //     768: { slidesPerView: 1, spaceBetween: 0,},
        //     1024: { slidesPerView: 1, spaceBetween: 0, },
        // }
    });

//image -text

   




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

var Homeswiper = new Swiper(".wall_distinction_slider", {
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
            }
        }
    });

    var Homeswiper = new Swiper(".alumni_events", {
    loop: true,
    speed: 1500,
    slidesPerView: 2,
    spaceBetween: 30,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },

   

     pagination: {
        el: ".swiper-pagination",
        clickable: true,
        type: "bullets",
    },

    breakpoints: {
         320: { slidesPerView: 1, spaceBetween: 16 },
         480: { slidesPerView: 1, spaceBetween: 16 },
         767: { slidesPerView: 1, spaceBetween: 16 },
         991: { slidesPerView: 2, spaceBetween: 30 },
         1199:{ slidesPerView: 2, spaceBetween: 30 }
    }
});



const slider = document.querySelector('.alumni_events');

slider.addEventListener('mouseenter', function () {
    Homeswiper.autoplay.stop();
});
slider.addEventListener('mouseleave', function () {
    Homeswiper.autoplay.start();
});



    //-------students-testimonials-slider

    var Homeswiper = new Swiper(".students-testimonials-slider", {
        loop: true,
        speed: 1500,
        slidesPerView: 2,
        spaceBetween: 16,
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
            1199: {
                slidesPerView: 2,
                spaceBetween: 16
            }
        }
    });



    //testimonial-text

    var Homeswiper = new Swiper(".testimonial_text_slider", {
        loop: true,
        speed: 800,
        slidesPerView: 1,
        spaceBetween: 0,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false
        },
        navigation: {
            nextEl: ".home-next",
            prevEl: ".home-prev",
        },
        breakpoints: {
            0:{autoHeight: true,},
            768: { slidesPerView: 1, spaceBetween: 0,autoHeight: true,},
            1024: { slidesPerView: 1, spaceBetween: 10, autoHeight: false,},
        }
    });



document.addEventListener('DOMContentLoaded', function () {
  const containerSelector = '.corporate_slider';
  const container = document.querySelector(containerSelector);

  if (!container) {
    console.warn('Swiper container not found:', containerSelector);
    return;
  }

  const corporateSwiper = new Swiper(containerSelector, {
    loop: true,
    speed: 800,
    slidesPerView: 3,
    autoplay: false,
    spaceBetween: 0,
    autoplay: { 
      delay: 3000,
      disableOnInteraction: false,
    },

    // ✅ Pagination added
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },

    navigation: {
      nextEl: ".home-next",
      prevEl: ".home-prev",
    },

    breakpoints: {
      0: {
        slidesPerView: 1,
        autoHeight: true
      },
      550: {
        slidesPerView: 2,
        spaceBetween: 20,
        autoHeight: true
      },
      1024: {
        slidesPerView: 3,
        spaceBetween: 20,
        autoHeight: false
      },
      1200: {
        slidesPerView: 4,
        spaceBetween: 20,
        autoHeight: false
      }
    }
  });

  // Pause autoplay on mouse enter / leave
  container.addEventListener('mouseenter', () => {
    corporateSwiper.autoplay?.stop();
  });

  container.addEventListener('mouseleave', () => {
    corporateSwiper.autoplay?.start();
  });

  // Touch pause
  container.addEventListener('touchstart', () => {
    corporateSwiper.autoplay?.stop();
  }, { passive: true });

  container.addEventListener('touchend', () => {
    corporateSwiper.autoplay?.start();
  }, { passive: true });
});






var Homeswiper = new Swiper(".mentor_slider", {
    loop: true,
    speed: 800,
    slidesPerView: 1,
    spaceBetween: 0,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false
    },
    navigation: {
        nextEl: ".home-next",
        prevEl: ".home-prev",
    },
    breakpoints: {
        0:{ autoHeight: true },
        768:{ slidesPerView: 1, spaceBetween: 0, autoHeight: true },
        1024:{ slidesPerView: 2, spaceBetween: 40, autoHeight: false },
    }
});

// Pause autoplay on hover
document.querySelector('.mentor_slider').addEventListener('mouseenter', function () {
    Homeswiper.autoplay.stop();
});

// Resume autoplay when mouse leaves
document.querySelector('.mentor_slider').addEventListener('mouseleave', function () {
    Homeswiper.autoplay.start();
});








    // // faculty_slider start here
    // var swiper = new Swiper(".faculty_slider", {
    //     slidesPerView: 5,
    //     spaceBetween: 30,
    //     pagination: {
    //       el: ".swiper-pagination",
    //       type: "progressbar",
    //     },
    //      breakpoints:{
    //         1200: {
    //         spaceBetween: 20
    //         },
    //         1550: {
    //         spaceBetween: 30
    //         }
    //      }
   
    //   });

    document.addEventListener("DOMContentLoaded", function () {
        const observer = new IntersectionObserver(
          (entries, observer) => {
            entries.forEach(entry => {
              if (entry.isIntersecting) {
                if (entry.target.classList.contains("image")) {
                  entry.target.classList.add("reveal-image");
                } else if (entry.target.classList.contains("image2")) {
                  entry.target.classList.add("reveal-image2");
                } else if (entry.target.classList.contains("image3")) {
                  entry.target.classList.add("reveal-image3");
                }
                observer.unobserve(entry.target); // remove if you only want the animation once
              }
            });
          },
          { threshold: 0.1 } // trigger when 10% of the element is visible
        );
    
        document.querySelectorAll('.image, .image2, .image3').forEach(el => {
          observer.observe(el);
        });
      });

    $(window).resize(function () {
        adjustMaxContent();
    });
    function adjustMaxContent() {
        let containerWidth = $(".container").width()
        //console.log([...containerWidth]);
        // containerWidth = $([...containerWidth][2]).width();
        let windowWidth = $("body").width();
        windowWidth = windowWidth > 1920 ? 1920 : windowWidth;
        let maxContentWidth = (windowWidth - (windowWidth - containerWidth) / 2) + 13;

        if (windowWidth >= 1400) {
            $(".max-content-xxl").css("max-width", `${maxContentWidth}px`);
            $(".max-content-xl").css("max-width", `${maxContentWidth}px`);
            $(".max-content-lg").css("max-width", `${maxContentWidth}px`);
            $(".max-content-md").css("max-width", `${maxContentWidth}px`);
            $(".max-content-sm").css("max-width", `${maxContentWidth}px`);
            $(".max-content").css("max-width", `${maxContentWidth}px`);
        } else if (windowWidth >= 1200) {
            $(".max-content-xxl").css("max-width", "");
            $(".max-content-xl").css("max-width", `${maxContentWidth}px`);
            $(".max-content-lg").css("max-width", `${maxContentWidth}px`);
            $(".max-content-md").css("max-width", `${maxContentWidth}px`);
            $(".max-content-sm").css("max-width", `${maxContentWidth}px`);
            $(".max-content").css("max-width", `${maxContentWidth}px`);
        } else if (windowWidth >= 992) {
            $(".max-content-xxl").css("max-width", "");
            $(".max-content-xl").css("max-width", "");
            $(".max-content-lg").css("max-width", `${maxContentWidth}px`);
            $(".max-content-md").css("max-width", `${maxContentWidth}px`);
            $(".max-content-sm").css("max-width", `${maxContentWidth}px`);
            $(".max-content").css("max-width", `${maxContentWidth}px`);
        } else if (windowWidth >= 768) {
            $(".max-content-xxl").css("max-width", "");
            $(".max-content-xl").css("max-width", "");
            $(".max-content-lg").css("max-width", "");
            $(".max-content-md").css("max-width", `${maxContentWidth}px`);
            $(".max-content-sm").css("max-width", `${maxContentWidth}px`);
            $(".max-content").css("max-width", `${maxContentWidth}px`);
        } else if (windowWidth >= 575) {
            $(".max-content-xxl").css("max-width", "");
            $(".max-content-xl").css("max-width", "");
            $(".max-content-lg").css("max-width", "");
            $(".max-content-md").css("max-width", "");
            $(".max-content-sm").css("max-width", `${maxContentWidth}px`);
            $(".max-content").css("max-width", `${maxContentWidth}px`);
        } else {
            $(".max-content-xxl").css("width", "");
            $(".max-content-xl").css("width", "");
            $(".max-content-lg").css("width", "");
            $(".max-content-md").css("width", "");
            $(".max-content-sm").css("width", "");
            $(".max-content").css("width", `${maxContentWidth}px`);
        }
    }




})(jQuery);

// UIAP 02011995 End




// gla-social-sec slider start

let socialSwiper = null;

function initSocialSlider() {
  const gridEl = document.querySelector(".gla-social_grid");
  if (!gridEl) return;

  const wrapperEl = gridEl.parentElement;
  const isMobile = window.innerWidth <= 991;

  // Cleanup old Swiper
  if (socialSwiper) {
    socialSwiper.destroy(true, true);
    socialSwiper = null;

    wrapperEl.classList.remove("swiper");
    gridEl.classList.remove("swiper-wrapper");
    gridEl.querySelectorAll("figure").forEach((fig) => {
      fig.classList.remove("swiper-slide");
    });
  }

  // Only initialize on mobile
  if (isMobile) {
    wrapperEl.classList.add("swiper");
    gridEl.classList.add("swiper-wrapper");
    gridEl.querySelectorAll("figure").forEach((fig) => {
      fig.classList.add("swiper-slide");
    });

    socialSwiper = new Swiper(".gla-social-sec .swiper", {
      slidesPerView: 1,
      slidesPerGroup: 1,
      loop: true,
      loopAdditionalSlides: 1,
      spaceBetween: 0,
      navigation: {
        nextEl: ".gla-sliderBtn .swiper-button-next",
        prevEl: ".gla-sliderBtn .swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
            0:{spaceBetween:10, autoHeight: true,},
            768:{slidesPerView: 2,spaceBetween: 10,},
            992:{slidesPerView: 2,spaceBetween: 10,},
        }
    });
  }
}

window.addEventListener("load", initSocialSlider);
window.addEventListener("resize", initSocialSlider);





document.addEventListener("DOMContentLoaded", function () {
	new Swiper(".recruiters-slider", {
		slidesPerView: 1,
		spaceBetween: 0,
		loop: true,
		autoplay: {
			delay: 3000,
			disableOnInteraction: false,
		},
		navigation: {
			nextEl: ".recruiters-btn .swiper-button-next",
			prevEl: ".recruiters-btn .swiper-button-prev",
		},
		pagination: {
			el: ".recruiters-slider .swiper-pagination",
			clickable: true,
		},
         breakpoints: {
            480: {
                slidesPerView: 1,
                spaceBetween: 16
            },
            767: {
                slidesPerView: 1,
                spaceBetween: 16
            },
            991: {
                slidesPerView: 4,
                spaceBetween: 16
            },
          
            1920: {
                slidesPerView: 5,
                spaceBetween: 16
            }
        }
	});
});

document.addEventListener("DOMContentLoaded", function () {
	new Swiper(".placement-slider", {
		slidesPerView: 1,
		slidesPerGroup: 1,
		loop: true,
		spaceBetween: 0,
		autoplay: {
			delay: 3000,
			disableOnInteraction: false,
		},
		pagination: {
			el: ".swiper-pagination",
			clickable: true,
		},
		navigation: {
			nextEl: ".swiper-button-next",
			prevEl: ".swiper-button-prev",
		},
        breakpoints: {
            480: {
                slidesPerView: 1,
                spaceBetween: 0
            },
            767: {
                slidesPerView: 2,
                spaceBetween: 16
            },
        },
	});
});


   


 /** document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".counter-number");

  counters.forEach(counter => {
    const target = parseInt(counter.getAttribute("data-target"));
    const suffix = counter.getAttribute("data-suffix") || "";
    const suffixlast = counter.getAttribute("data-suffix-last") || ""; // fixed typo
    
    let count = 0;

    const duration = 2000; // total animation time in ms
    const frameRate = 60; // frames per second
    const totalFrames = Math.round((duration / 1000) * frameRate);
    const increment = target / totalFrames;

    const updateCount = () => {
      count += increment;
      if (count < target) {
        counter.innerHTML = `${Math.round(count)}${suffix}${suffixlast}`;
        requestAnimationFrame(updateCount);
      } else {
        counter.innerHTML = `${target}${suffix}${suffixlast}`;
      }
    };

    updateCount();
  });
});**/



// document.addEventListener("DOMContentLoaded", () => {
//   const counters = document.querySelectorAll(".counter-number");

//   const runCounter = (counter) => {
//     const target = parseFloat(counter.getAttribute("data-target"));
//     const suffix = counter.getAttribute("data-suffix") || "";
//     const suffixlast = counter.getAttribute("data-suffix-last") || "";
//     let count = 0;
//     const duration = 2000;
//     const frameRate = 60;
//     const totalFrames = Math.round((duration / 1000) * frameRate);
//     const increment = target / totalFrames;
//     const showDecimal = !Number.isInteger(target);

//     const updateCount = () => {
//       count += increment;
//       if (count < target) {
//         counter.innerHTML = `${showDecimal ? count.toFixed(1) : Math.round(count)}${suffix}${suffixlast}`;
//         requestAnimationFrame(updateCount);
//       } else {
//         counter.innerHTML = `${showDecimal ? target.toFixed(1) : Math.round(target)}${suffix}${suffixlast}`;
//       }
//     };

//     updateCount();
//   };

//   const observer = new IntersectionObserver((entries, obs) => {
//     entries.forEach(entry => {
//       if (entry.isIntersecting) {
//         runCounter(entry.target);
//         obs.unobserve(entry.target); 
//       }
//     });
//   }, {
//     threshold: 0.6
//   });

//   counters.forEach(counter => {
//     observer.observe(counter);
//   });
// });


document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".counter-number");

  const runCounter = (counter) => {
    const target = parseFloat(counter.getAttribute("data-target"));
    const suffix = counter.getAttribute("data-suffix") || "";
    const prefix = counter.getAttribute("data-prefix") || "";
    const suffixlast = counter.getAttribute("data-suffix-last") || "";
    let count = 0;
    const duration = 2000;
    const frameRate = 60;
    const totalFrames = Math.round((duration / 1000) * frameRate);
    const increment = target / totalFrames;
    const showDecimal = !Number.isInteger(target);

    const updateCount = () => {
      count += increment;
      if (count < target) {
        counter.innerHTML = `${prefix}${showDecimal ? count.toFixed(1) : Math.round(count)}${suffix}${suffixlast}`;
        requestAnimationFrame(updateCount);
      } else {
        counter.innerHTML = `${prefix}${showDecimal ? target.toFixed(1) : Math.round(target)}${suffix}${suffixlast}`;
      }
    };

    updateCount();
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        runCounter(entry.target);
        obs.unobserve(entry.target); // Run only once
      }
    });
  }, {
    threshold: 0.6 // Adjust depending on when you want it to start
  });

  counters.forEach(counter => {
    observer.observe(counter);
  });
});





document.addEventListener("DOMContentLoaded", function () {

    const iframe = document.getElementById('alumniVideo');
    const playBtn = document.getElementById('playPauseBtn');
    if (!iframe || !playBtn) return;
    const player = new Vimeo.Player(iframe);

    playBtn.addEventListener('click', async () => {
        const paused = await player.getPaused();

        if (paused) {
            await player.setVolume(1); // 🔥 important
            await player.play();
            playBtn.innerHTML = "⏸";
        } else {
            await player.pause();
            playBtn.innerHTML = "▶️";
        }
    });

    player.on('play', () => {
        playBtn.innerHTML = "⏸";
    });

    player.on('pause', () => {
        playBtn.innerHTML = "▶️";
    });

});


