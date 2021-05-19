function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function isIE() {
    var userAgent = window.navigator.userAgent.toLowerCase();
    if ( userAgent.indexOf( 'msie' ) !== -1 || userAgent.indexOf( 'trident' ) !== -1 ) {
        return true;
    }
    return false;
}

function showOpenFileDialog(){
    return new Promise(resolve => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.txt, text/plain';
        input.onchange = event => { resolve(event.target.files[0]); };
        input.click();
    });
}

function readAsText(file){
    return new Promise(resolve => {
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = () => { resolve(reader.result); };
    });
}