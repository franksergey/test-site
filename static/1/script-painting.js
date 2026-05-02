(function () {
    const canvas = document.getElementById("background");
    if (!canvas || !(canvas instanceof HTMLCanvasElement)) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let isDrawing = false;
    let prev = { x: 0, y: 0 };

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function clear() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    function getPos(e) {
        if (e.touches) {
            return {
                x: e.touches[0].clientX,
                y: e.touches[0].clientY
            };
        } else {
            return {
                x: e.clientX,
                y: e.clientY
            };
        }
    }

    function draw(e) {
        if (!isDrawing) return;

        const pos = getPos(e);

        ctx.beginPath();
        ctx.lineWidth = 2;
        ctx.lineCap = "round";
        ctx.strokeStyle = "#000000";

        ctx.moveTo(prev.x, prev.y);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();

        prev = pos;
    }

    canvas.addEventListener("mousedown", (e) => {
        isDrawing = true;
        prev = getPos(e);
    });

    canvas.addEventListener("mousemove", draw);

    canvas.addEventListener("mouseup", () => {
        isDrawing = false;
    });

    canvas.addEventListener("mouseleave", () => {
        isDrawing = false;
    });

    canvas.addEventListener("touchstart", (e) => {
        isDrawing = true;
        prev = getPos(e);
    });

    canvas.addEventListener("touchmove", (e) => {
        draw(e);
        e.preventDefault();
    });

    canvas.addEventListener("touchend", () => {
        isDrawing = false;
    });

    window.addEventListener("resize", resize);

    resize();
})();