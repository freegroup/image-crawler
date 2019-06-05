// create the paint area. The id in the constructor must be
// an existing DIV
var canvas = new draw2d.Canvas("gfx_holder");
var p = new RectangleToolPolicy();


canvas.installEditPolicy(p)
canvas.paper.canvas.style.position="relative";


// create and add two Node which contains Ports (In and OUT)
var rect = new LabelRectangle({width:100, height:80});
canvas.add( rect, 150,200);

$("body")
    .scrollTop(0)
    .scrollLeft(0);
