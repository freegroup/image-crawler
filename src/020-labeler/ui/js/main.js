var currentImage = null;
var currentLabelInput = "label-1"
var shortcut_next = "ArrowRight"
var shortcut_back = "ArrowLeft"
var shortcut_label1 = "Digit1"
var shortcut_label2 = "Digit2"
var shortcut_label3 = "Digit3"


tippy('#label-1-group', {
    content: 'Press digit key <b>1</b> to select this label as default',
    arrow: true,
    trigger: "click",
    placement:"right"
})
tippy('#label-2-group', {
    content: 'Press digit key <b>2</b> to select this label as default',
    arrow: true,
    trigger: "click",
    placement:"right"
})
tippy('#label-3-group', {
    content: 'Press digit key <b>3</b> to select this label as default',
    arrow: true,
    trigger: "click",
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

//$("#overlay").show();
//$("#overlay-content").show().center();

$("#preview").focus();

setTimeout(function(){
    $("#overlay").fadeOut();
}, 5000);


// create the paint area. The id in the constructor must be
// an existing DIV
var canvas = new draw2d.Canvas("gfx_holder");
var p = new RectangleToolPolicy();
canvas.installEditPolicy(p)
canvas.paper.canvas.style.position="relative";


$( ".input-group > input" ).on("keyup",function() {
    var values = getAllLabels();
    py_set_labels(values);
});


$( ".input-group > input" ).on("blur",function() {
    $("#preview").focus();
});

function getAllLabels(){
    return $(".input-group > input").map(function(){return $(this).val();}).get();
}

function setSelectedLabel(group){
    $(".selected-label-group").removeClass("selected-label-group");
    $("."+group).addClass("selected-label-group");
}

$("#preview").on("keydown", function(e) {
    e = e || window.event;
    e = e.originalEvent

    if (event.repeat != undefined) {
        allowed = !event.repeat;
    }
    if (!allowed) return;

    console.log(e.code)
    if (e.code === shortcut_back) {
        onBackClick()
    }
    else if (e.code === shortcut_next) {
        onNextClick()
    }
    else if (e.code === shortcut_label1) {
        currentLabelInput = "label-1"
        setSelectedLabel("input-group-1")
    }
    else if (e.code === shortcut_label2) {
        currentLabelInput = "label-2"
        setSelectedLabel("input-group-2")
    }
    else if (e.code === shortcut_label3) {
        currentLabelInput = "label-3"
        setSelectedLabel("input-group-3")
    }
})

/* called from python */
function js_set_image(src, width, height, labels){
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
    $("#preview").scrollLeft(0).scrollTop(0)
}

function js_set_labels(labels){
   labels.forEach(function(e,i){
       $("#label-"+(i+1)).val(e);
   })
}

function js_set_navigation_shortcuts(next_shortcut, back_shortcut, label1, label2, label3){
    shortcut_next = next_shortcut;
    shortcut_back = back_shortcut;
    shortcut_label1 = label1;
    shortcut_label2 = label2;
    shortcut_label3 = label3;
}

function onNextClick() {
    var writer = new draw2d.io.json.Writer();
    writer.marshal(canvas,function(json){
        json = filterJson(json)
        py_next_click_callback(json);
    });
}


function onBackClick() {
    var writer = new draw2d.io.json.Writer();
    writer.marshal(canvas,function(json){
        json = filterJson(json)
        py_back_click_callback(json);
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
            label_index: getAllLabels().indexOf(rect.label_text),
            label_text: rect.label_text,
            id: rect.id
        };
    })
    return json
}
$("body")
    .scrollTop(0)
    .scrollLeft(0);
