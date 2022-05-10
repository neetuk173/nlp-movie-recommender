'use strict';

(function() {

    window.myApp = new Framework7({
        cache: false,
        init: false,
        material: true,
        modalTitle: 'Baruch College',
        notificationCloseButtonText: 'OK',
        scrollTopOnNavbarClick: true,
        tapHold: true,
        tapHoldDelay: 1000,
        modalCloseByOutside: false,
        scrollTopOnNavbarClick: true,
        hideNavbarOnPageScroll: true,
        hideToolbarOnPageScroll: true
    });

    window.mainView = myApp.addView('.view-main');
    window.$$ = Dom7;

})();