$(document).ready(function(){
    var burger = $('.burger');
    var menu = $('#' + burger.data('target'));
    burger.on('click', function() {
      burger.toggleClass('is-active');
      menu.toggleClass('is-active');
    });
  });

function bold_button(){
    var editor = document.getElementById("id_body");
    var pos_start = editor.selectionStart;
    var pos_end = editor.selectionEnd;
    var sentence = editor.value;
    var len      = sentence.length;

    var before   = sentence.substr(0, pos_start);
    var word_pre = '**';
    var content  = sentence.substr(pos_start, pos_end-pos_start);
    var word_post = '**';
    var after    = sentence.substr(pos_end, len);
    
    sentence = before + word_pre + content + word_post + after;
    editor.value = sentence;
    
    editor.focus();
    if(pos_start == pos_end){
        editor.setSelectionRange(pos_end+2, pos_end+2);
    }else{
        editor.setSelectionRange(pos_end+content.length+2, pos_end+content.length+2);
    }
    markdown2html();
}
function italic_button(){
    var editor = document.getElementById("id_body");
    var pos_start = editor.selectionStart;
    var pos_end = editor.selectionEnd;
    var sentence = editor.value;
    var len      = sentence.length;

    var before   = sentence.substr(0, pos_start);
    var word_pre = '*';
    var content  = sentence.substr(pos_start, pos_end-pos_start);
    var word_post = '*';
    var after    = sentence.substr(pos_end, len);
    
    sentence = before + word_pre + content + word_post + after;
    editor.value = sentence;
    
    editor.focus();
    if(pos_start == pos_end){
        editor.setSelectionRange(pos_end+1, pos_end+1);
    }else{
        editor.setSelectionRange(pos_end+content.length+1, pos_end+content.length+1);
    }
    markdown2html();
}

function header_button(){
    var editor = document.getElementById("id_body");
    var pos_start = editor.selectionStart;
    var pos_end = editor.selectionEnd;
    var sentence = editor.value;
    var len      = sentence.length;

    var before   = sentence.substr(0, pos_start);
    var after    = sentence.substr(pos_start, len);
    
    var rows = before.split("\n");
    var addchar = ""
    if(rows[rows.length-1].substr(0,6) != "######"){
        if(rows[rows.length-1][0]=="#"){
            addchar = "#";
        }else{
            addchar = "# "
        }
    }
    rows[rows.length-1] = addchar + rows[rows.length-1];
    

    var presentence = ""
    for(var i = 0; i<rows.length-1;++i){
        presentence += rows[i] + "\n"
    }
    presentence += rows[rows.length-1];
    editor.value = presentence + after;
    
    editor.focus();
    editor.setSelectionRange(pos_end+addchar.length, pos_end+addchar.length);
    
    markdown2html();
}

function itemize_button(){
    var editor = document.getElementById("id_body");
    var pos_start = editor.selectionStart;
    var pos_end = editor.selectionEnd;
    var sentence = editor.value;
    var len      = sentence.length;

    var before   = sentence.substr(0, pos_start);
    var after    = sentence.substr(pos_start, len);
    var diff = 0;
    
    var rows = before.split("\n");
    if(rows[rows.length-1].substr(0,2) != "* "){
        rows[rows.length-1] = "* " + rows[rows.length-1];
        diff = 2;
    }else{
        rows[rows.length-1] = rows[rows.length-1].substr(2);
        diff = -2;
    }

    var presentence = ""
    for(var i = 0; i<rows.length-1;++i){
        presentence += rows[i] + "\n"
    }
    presentence += rows[rows.length-1];
    editor.value = presentence + after;
    
    editor.focus();
    editor.setSelectionRange(pos_end+diff, pos_end+diff);
    
    markdown2html();
}

function numeric_button(){
    var editor = document.getElementById("id_body");
    var pos_start = editor.selectionStart;
    var pos_end = editor.selectionEnd;
    var sentence = editor.value;
    var len      = sentence.length;

    var before   = sentence.substr(0, pos_start);
    var after    = sentence.substr(pos_start, len);
    var diff = 0;
    
    var rows = before.split("\n");
    if(rows[rows.length-1].substr(0,3) != "1. "){
        rows[rows.length-1] = "1. " + rows[rows.length-1];
        diff = 3;
    }else{
        rows[rows.length-1] = rows[rows.length-1].substr(3);
        diff = -3;
    }

    var presentence = ""
    for(var i = 0; i<rows.length-1;++i){
        presentence += rows[i] + "\n"
    }
    presentence += rows[rows.length-1];
    editor.value = presentence + after;
    
    editor.focus();
    editor.setSelectionRange(pos_end+diff, pos_end+diff);
    
    markdown2html();
}

function quote_button(){
    var editor = document.getElementById("id_body");
    var pos_start = editor.selectionStart;
    var pos_end = editor.selectionEnd;
    var sentence = editor.value;
    var len      = sentence.length;

    var before   = sentence.substr(0, pos_start);
    var after    = sentence.substr(pos_start, len);
    var diff = 0;
    
    var rows = before.split("\n");
    if(rows[rows.length-1].substr(0,2) != "> "){
        rows[rows.length-1] = "> " + rows[rows.length-1];
        diff = 2;
    }else{
        rows[rows.length-1] = rows[rows.length-1].substr(2);
        diff = -2;
    }

    var presentence = ""
    for(var i = 0; i<rows.length-1;++i){
        presentence += rows[i] + "\n"
    }
    presentence += rows[rows.length-1];
    editor.value = presentence + after;
    
    editor.focus();
    editor.setSelectionRange(pos_end+diff, pos_end+diff);
    
    markdown2html();
}

function link_button(){
    var editor = document.getElementById("id_body");
    var pos_start = editor.selectionStart;
    var pos_end = editor.selectionEnd;
    var sentence = editor.value;
    var len      = sentence.length;

    var before   = sentence.substr(0, pos_start);
    var after    = sentence.substr(pos_start, len);

    editor.value = before + "[見出し](https://)" + after;
    
    editor.focus();
    editor.setSelectionRange(pos_end+15, pos_end+15);
    markdown2html();
}

function image_button(url="https://画像へのURL"){
    var editor = document.getElementById("id_body");
    var pos_start = editor.selectionStart;
    var pos_end = editor.selectionEnd;
    var sentence = editor.value;
    var len      = sentence.length;

    var before   = sentence.substr(0, pos_start);
    var after    = sentence.substr(pos_start, len);

    var insertTxt = '\n![置換テキスト](' + url + ' "タイトル")\n';
    editor.value = before + insertTxt + after;
    
    editor.focus();
    editor.setSelectionRange(pos_end+insertTxt.length, pos_end+insertTxt.length);
    markdown2html();
}


function question_button() {
    document.getElementById('id_body').focus();

    var result = document.getElementById('result_6efc3b09-3fc2-0a7a-8ca0-3c3c04b331fc');
    var sheet = document.getElementById('cheat-sheet');

    if (sheet.classList.contains('is-hidden')) {
        sheet.classList.remove('is-hidden');
        result.style.width = '25%';
    } else {
        hiddenCheatSheet();
    }
}

function hiddenCheatSheet() {
    document.getElementById('cheat-sheet').classList.add('is-hidden');
    document.getElementById('result_6efc3b09-3fc2-0a7a-8ca0-3c3c04b331fc').style.width = '50%';
}
