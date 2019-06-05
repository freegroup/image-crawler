
var check_image_timer =0;

document.onkeydown = checkKey;

tippy('#search-button', {
    content: 'Enter a search term and press the search button to get suggestions for new pictures promoted by Bing Image Search.',
    arrow: true,
    delay:[1000, 20],
    flipBehavior: ["bottom", "right"],
    placement:"bottom"
})

tippy('#arrow_counter_candidates', {
    content: 'Valid search result and ready for downloading from the web',
    arrow: true,
    delay:[500, 20],
    placement:"bottom"
})
tippy('#arrow_counter_review', {
    content: 'Images downloaded from the web and ready for user rating',
    arrow: true,
    delay:[500, 20],
    placement:"bottom"
})
tippy('#arrow_counter_pool', {
    content: 'Already downloaded images and as good voted',
    arrow: true,
    delay:[500, 20],
    placement:"bottom"
})

py_check_image_callback();

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
        document.getElementById("search-animation").style.visibility = "visible";
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
        document.getElementById("search-animation").style.visibility="hidden";
        input.disabled = false;
        button.innerText ="Search"
        py_search_stop_callback();
        js_set_image("");
    }
}



/* called from python */
function js_set_image(src){
    var disabled = src===""
    document.getElementById("preview_image").src = src;
    document.getElementById("button_skip").disabled = disabled;
    document.getElementById("button_keep").disabled = disabled;
}

function js_set_counter(elementId, value){
    document.getElementById(elementId).innerText = value;
}

