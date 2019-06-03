
function onSkipClick() {
    py_skip_image_callback();
}

function onKeepClick() {
    py_keep_image_callback();
}

function onSearchClick() {
    var term = document.getElementById("search-term").value
    py_search_image_callback(term);
}


/* called from python */
function js_set_image(src){
    document.getElementById("preview_image").src = src;
}

/* called from python */
function js_init_image_check_timer(){
    setInterval(function(){
        py_check_image_callback();
    },500)
}

function js_set_counter(elementId, value){
    document.getElementById(elementId).innerText = value;
}