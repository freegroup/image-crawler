
var currentImage = null;

// create the paint area. The id in the constructor must be
// an existing DIV
var canvas = new draw2d.Canvas("gfx_holder");
var p = new RectangleToolPolicy();
canvas.installEditPolicy(p)
canvas.paper.canvas.style.position="relative";


function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '38') {
        // up arrow
    }
    else if (e.keyCode == '40') {
        // down arrow
    }
    else if (e.keyCode == '37') {
        // left arrow
    }
    else if (e.keyCode == '39') {
        // right arrow
        onNextClick()
    }
}
document.onkeydown = checkKey;


/* called from python */
function js_set_image(src, width, height){
    if(currentImage!==null)
        canvas.remove(currentImage);
    canvas.add(currentImage =new draw2d.shape.basic.Image({path:src, x:0, y:0, width:width, height:height}));
}

function onNextClick() {
    py_search_start_callback("ddd");
}

$("body")
    .scrollTop(0)
    .scrollLeft(0);
