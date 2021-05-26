function transition_link(link) {
    var body = document.querySelector('body');
    body.classList.remove('animated-show-active');
    setTimeout(onAnimationComplete, 500);
    function onAnimationComplete() {
        window.location = link;
    }
}

