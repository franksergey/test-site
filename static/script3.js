const canvas = document.getElementById('background');
const ctx = canvas.getContext('2d');

let painting = false;

// 📏 делаем canvas адаптивным
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// 📍 универсальная функция координат (мышь + тач)
function getPos(e) {
    if (e.touches) {
        return {
            x: e.touches[0].clientX - canvas.offsetLeft,
            y: e.touches[0].clientY - canvas.offsetTop
        };
    }
    return {
        x: e.clientX - canvas.offsetLeft,
        y: e.clientY - canvas.offsetTop
    };
}

// ▶️ начать рисовать
function startPosition(e) {
    painting = true;
    draw(e);
}

// ⛔ остановить рисование
function finishedPosition() {
    painting = false;
    ctx.beginPath(); // сброс линии
}

// 🎨 рисование
function draw(e) {
    if (!painting) return;

    const pos = getPos(e);

    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';

    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

// 🖱️ мышь
canvas.addEventListener('mousedown', startPosition);
canvas.addEventListener('mouseup', finishedPosition);
canvas.addEventListener('mouseleave', finishedPosition);
canvas.addEventListener('mousemove', draw);

// 📱 мобильные
canvas.addEventListener('touchstart', startPosition);
canvas.addEventListener('touchend', finishedPosition);
canvas.addEventListener('touchmove', (e) => {
    draw(e);
    e.preventDefault(); // отключает скролл
});