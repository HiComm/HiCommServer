window.addEventListener("load", function() {
    inputTabInTextarea();
    addShortcutKey();
    removeShortcutKey();
});

// textareaでのTABキー入力
function inputTabInTextarea() {
    document.getElementById('id_body').onkeydown = function(e) {
        if (e.key == "Tab") {
            e.preventDefault();
            var elem = e.target;
            var val = elem.value;
            var pos = elem.selectionStart;
            elem.value = val.substr(0, pos) + '    ' + val.substr(pos, val.length);
            elem.setSelectionRange(pos + 4, pos + 4);
        }
    }
}

/*
// focusの変更を監視
function addFocusListener() {
    addEventListener("focus", validFocusOnTextarea, true);
}

// focusがmarkdownのテキストエリアにあるかをチェック
function validFocusOnTextarea() {
    var focused = document.activeElement;
    if (focused === document.getElementById('input')) addShortcutKey();
    else removeShortcutKey();
}
*/

// textareaのfocusになったらmarkdownのショートカットキーの追加
function addShortcutKey() {
    document.getElementById('id_body').onfocus = function() {
        // "B"ボタン
        shortcut.add("Ctrl+Shift+a", function() {
            $('#mde-buttons div p:nth-child(1) button').click();
        });
        // I ボタン(** **)
        // H ボタン(#)
        // list-ul ボタン(*)
        // list-ol ボタン(1.)
        // linkボタン([]http://)
        // imageボタン(![](hhtp://)
    }
}

// textareaのfocusが外れたらmarkdownのショートカットを削除　
function removeShortcutKey() {
    document.getElementById('id_body').onblur = function() {
        // "B"ボタン
        shortcut.remove("Ctrl+Shift+a");
        // I ボタン(** **)
        // H ボタン(#)
        // list-ul ボタン(*)
        // list-ol ボタン(1.)
        // linkボタン([]http://)
        // imageボタン(![](hhtp://)
    }
}

var mathjaxTimer = null

function markdown2html() {
    document.getElementById('result_6efc3b09-3fc2-0a7a-8ca0-3c3c04b331fc').innerHTML =
    marked(document.getElementById('id_body').value);

    //===============================================
    //@brief  更新毎にシンタックスハイライトの判定します
    //@author matsutake
    //@date   2020/3/9
    //===============================================
    var nodelist = document.querySelectorAll('pre code');
    var node = Array.prototype.slice.call(nodelist,0); 
    node.forEach(function(block){
        hljs.highlightElement(block);
    });

    clearInterval(mathjaxTimer);
    mathjaxTimer = setTimeout(function(){
        MathJax.Hub.Queue(["Typeset",MathJax.Hub,"result_6efc3b09-3fc2-0a7a-8ca0-3c3c04b331fc"]);
    }, 600);
}
