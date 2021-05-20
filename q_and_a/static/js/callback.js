window.addEventListener("load",function(){
    
    this.document.getElementById("id_btn_search").onclick = function(){
        var query = document.getElementById("id_input_query").value;
        var list_exactmatch_str = []
        const regex = /"(.*?)"/g;
        while((matched = regex.exec(query)) != null){
            if(matched[1].length>0){
                list_exactmatch_str.push(matched[1]);
            }
        }

        alert(query.replace(regex, ""));

    };

});