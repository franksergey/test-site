(function () {
    /* ————————————— open-form ————————————— */

    // const btn = document.querySelector('.open-form');
    // const form = document.querySelector('.email-form');

    // btn.addEventListener('click', () => {
    //     form.classList.toggle('active');
    // });
    // btn.addEventListener('hover', () => {
    //     form.classList.toggle('hover');
    // });

    const btn = document.querySelector('.open-form');
    const form = document.querySelector('.email-form');

    btn.addEventListener('click', () => {
    btn.classList.toggle('rotated');
    form.classList.toggle('active');
    });
})();