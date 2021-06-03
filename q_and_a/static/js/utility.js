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

function sendimage(_data){
    var url_server = "http://172.19.115.160:8082"
    $.ajax({
        url: url_server + "/api/image/post/",//TODO:画像サーバー
        type: "POST",
        data: _data,
        contentType: "text/plain",
        timeout: 2000,
    }).done((data)=>{
        var link = url_server + data;
        image_button(link);
    })
}

function uploadimage(){

    var element =  document.querySelector("textarea");
    
    element.addEventListener("paste", function(e){
        e.preventDefault();
        var idx = e.clipboardData.types.indexOf("Files");
        if(idx < 0){
            ;//do nothing
        }else{
            // ファイルとして得る
            var imageFile = e.clipboardData.items[idx].getAsFile();
            var fr = new FileReader();
            fr.onload = function(e) {
                var base64 = e.target.result;
                sendimage(base64);
            };
            fr.readAsDataURL(imageFile);
            
        }
    });

    element.addEventListener("drop", function(e){
        e.preventDefault();
        var files = e.dataTransfer.files;
        for(var i=0; i<files.length; ++i){
            if(files[i].size > 10000000){
                alert("file size is too large.");
                continue;
            }
            var fr = new FileReader();
            fr.onload = function(e) {
                var base64 = e.target.result;
                sendimage(base64);
            };
            fr.readAsDataURL(files[i]);
        }
    });
}