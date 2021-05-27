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
        if(file.size > 1000000){
            alert("ファイルサイズ：" + file.size + "Byte\nファイルサイズは1MB以下にしてください。");
            return;
        }
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = () => { resolve(reader.result); };
    });
}