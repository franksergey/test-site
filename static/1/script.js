const story = document.querySelector(".client-pain");
const texts = document.querySelectorAll(".p-accent");

window.addEventListener("scroll", () => {

    const rect = story.getBoundingClientRect();

    const progress =
        -rect.top / (story.offsetHeight - window.innerHeight);

    let index = 0;

    if (progress > 0.66) {
        index = 2;
    } else if (progress > 0.33) {
        index = 1;
    }

    texts.forEach((text, i) => {
        text.classList.toggle("p-active", i === index);
    });

});

const trigger = document.querySelector(".decision");
const button = document.querySelector(".button-sticky");

window.addEventListener("scroll", () => {

    const triggerTop = trigger.getBoundingClientRect().top;

    if (triggerTop < window.innerHeight * 0.8) {

        button.classList.add("visible");

    } else {

        button.classList.remove("visible");

    }

});