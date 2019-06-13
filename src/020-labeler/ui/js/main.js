tippy('#label-1-group', {
    content: 'Press digit key <b>1</b> to select this label as default',
    arrow: true,
    delay:[1000, 20],
    flipBehavior: ["bottom", "right"],
    placement:"right"
})
tippy('#label-2-group', {
    content: 'Press digit key <b>2</b> to select this label as default',
    arrow: true,
    delay:[1000, 20],
    flipBehavior: ["bottom", "right"],
    placement:"right"
})
tippy('#label-3-group', {
    content: 'Press digit key <b>3</b> to select this label as default',
    arrow: true,
    delay:[1000, 20],
    flipBehavior: ["bottom", "right"],
    placement:"right"
})

$.fn.center = function () {
    this.css("position","absolute");
    this.css("top", Math.max(0, (
        ($(window).height() - $(this).outerHeight()) / 2) +
        $(window).scrollTop()) + "px"
    );
    this.css("left", Math.max(0, (
        ($(window).width() - $(this).outerWidth()) / 2) +
        $(window).scrollLeft()) + "px"
    );
    return this;
}

$("#overlay").show();
$("#overlay-content").show().center();

setTimeout(function(){
    $("#overlay").fadeOut();
}, 5000);


var currentImage = null;
var currentLabelInput = "label-1"

// create the paint area. The id in the constructor must be
// an existing DIV
var canvas = new draw2d.Canvas("gfx_holder");
var p = new RectangleToolPolicy();
canvas.installEditPolicy(p)
canvas.paper.canvas.style.position="relative";


document.onkeydown = checkKey;
function setSelectedLabel(group){
    $(".selected-label-group").removeClass("selected-label-group");
    $("#"+group).addClass("selected-label-group");
}

function checkKey(e) {

    e = e || window.event;
    if (event.repeat != undefined) {
        allowed = !event.repeat;
    }
    if (!allowed) return;


    if (e.code === 'Digit1') {
        currentLabelInput = "label-1"
        setSelectedLabel("label-1-group")
    }
    else if (e.code === 'Digit2') {
        currentLabelInput = "label-2"
        setSelectedLabel("label-2-group")
    }
    else if (e.code === 'Digit3') {
        currentLabelInput = "label-3"
        setSelectedLabel("label-3-group")
    }
    else if (e.code === 'ArrowLeft') {
        onLastClick()
    }
    else if (e.code === 'ArrowRight') {
        onNextClick()
    }
}

/* called from python */
function js_set_image(src, width, height, labels){
    console.log(labels)
    canvas.clear();
    var reader = new draw2d.io.json.Reader();
    reader.unmarshal(canvas, labels);
    canvas.add(currentImage =new draw2d.shape.basic.Image({
        path:src,
        selectable:false,
        draggable:false,
        x:0,
        y:0,
        width:width,
        height:height
    }));
    currentImage.toBack();
}

function onNextClick() {
    var writer = new draw2d.io.json.Writer();
    writer.marshal(canvas,function(json){
        json = filterJson(json)
        py_next_click_callback(json);
    });
}


function onLastClick() {
    var writer = new draw2d.io.json.Writer();
    writer.marshal(canvas,function(json){
        json = filterJson(json)
        py_last_click_callback(json);
    });
}


function filterJson(json){
    json = json.filter(function (el) {
        return el.type === "LabelRectangle";
    });
    json = json.map(function (rect) {
        return {
            x: rect.x,
            y: rect.y,
            width: rect.width,
            height: rect.height,
            type: rect.type,
            text: rect.text,
            id: rect.id
        };
    })
    return json
}
$("body")
    .scrollTop(0)
    .scrollLeft(0);
