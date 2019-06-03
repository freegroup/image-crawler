
var check_image_timer =0;

document.onkeydown = checkKey;

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
        onSkipClick()
    }
    else if (e.keyCode == '39') {
        // right arrow
        onKeepClick()
    }
}

function onSkipClick() {
    py_skip_image_callback();
}

function onKeepClick() {
    py_keep_image_callback();
}

function onSearchClick() {
    var input = document.getElementById("search-term");
    var button = document.getElementById("search-button");
    if(input.disabled===false ) {
        document.getElementById("search-animation").style.display = "block";
        input.disabled = true;
        button.innerText ="Stop"
        check_image_timer = setInterval(function(){
            py_check_image_callback();
        },500)
        py_search_start_callback(input.value);
    }
    else{
        clearInterval(check_image_timer);
        js_set_counter("counter_candidates", "--")
        js_set_counter("counter_review", "--")
        document.getElementById("search-animation").style.display="none";
        input.disabled = false;
        button.innerText ="Search"
        py_search_stop_callback();
        js_set_image("");
    }
}



/* called from python */
function js_set_image(src){
    console.log("set_oimage", src, src!=="")
    document.getElementById("preview_image").src = src;
    document.getElementById("button_skip").disabled = src==="";
    document.getElementById("button_keep").disabled = src==="";
}

function js_set_counter(elementId, value){
    document.getElementById(elementId).innerText = value;
}

