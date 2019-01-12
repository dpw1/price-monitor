document.addEventListener('DOMContentLoaded', () => {

    var mobileMenu = function(){
      const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

          if ($navbarBurgers.length > 0) {

            $navbarBurgers.forEach( el => {
              el.addEventListener('click', () => {

                const target = el.dataset.target;
                const $target = document.getElementById(target);

                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');

              });
            });
          }
    };

    var monitorCardsDropdown = function(){
        var $monitors = document.querySelectorAll('.card-header-icon'),
			$thisMonitor;
		for (var i = 0; i < $monitors.length; i++) {
	    $thisMonitor = $monitors[i];
	    $thisMonitor.addEventListener('click', function(e) {
	        e.preventDefault();
	        $thisMonitor = this.closest('.card');
			$thisMonitor.querySelector('.card-container').classList.toggle('card-container--hidden');
			$thisMonitor.querySelector('.icon > svg').classList.toggle('icon-svg--rotate');


		});
	}
    };

    var init = function(){
        mobileMenu();
        monitorCardsDropdown();
    };

    init();
});