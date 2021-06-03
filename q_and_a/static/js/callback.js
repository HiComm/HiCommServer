window.addEventListener("load",function(){
    uploadimage();


    document.getElementById("id_input_query").addEventListener("keypress", function(e){
        if (e.key === 'Enter'){
            document.getElementById("id_btn_search").click();
        }
    });

    this.document.getElementById("id_btn_search").onclick = function(){
        var query = document.getElementById("id_input_query").value;
        console.log(encodeURI("/search?query=" + query));
        window.location.href = encodeURI("/search?query=" + query);
        /*
        $.get("./search", {
            query: query,
        });
        */
        /*
        query = query.replace("　", " ");

        var qs = query.split(/ (?=(?:(?:[^"]*"){2})*[^"]*$)/);

        var context = "none";
        var context_next = "none";

        var order = "";
        var subcontext = "none";

        var q = "";
        var q_json = {};

        for(var i = 0; i<qs.length; ++i){
            console.log(qs[i]);
            q = "";
            if(qs[i].length == 0){
                continue;
            }

            //判定部
            switch(context){
                case "none":
                    //tag判定
                    if(qs[i][qs[i].length - 1] == ":"){
                        switch(qs[i].substr(0, qs[i].length-1)){
                            case "tag":
                                context_next = "tag";
                                q_json[context_next] = {};
                                break;
                            case "title":
                                context_next = "title";
                                q_json[context_next] = {};
                                break;
                            case "text":
                                context_next = "text";
                                q_json[context_next] = {};
                                break;
                            case "user":
                                context_next = "user";
                                q_json[context_next] = {};
                                break;
                            default:
                                context_next = "none";
                                break;
                        }
                    }
                    break;
                
                case "tag":
                    if((qs[i].toLowerCase() == "and") || (qs[i].toLowerCase() == "or")){
                        q = qs[i].toLowerCase();
                    }else if(qs[i] == "||"){
                        order = "OR"
                        context_next  = "none";
                    }else if (qs[i] == "&&"){
                        order = "AND"
                        context_next = "none";
                    }else{
                        q = qs[i];
                    }
                    break;

                default:
                    break;
            }
            
            //処理部
            console.log("q:" + q);
            if(context in q_json){
                q_json[context]["query"] += " " + q;
            }else{
                q_json[context] = {}
            }

            //次
            context = context_next;

        }

        alert(JSON.stringify(q_json));

        var list_exactmatch_str = []
        const regex = /"(.*?)"/g;
        while((matched = regex.exec(query)) != null){
            if(matched[1].length>0){
                list_exactmatch_str.push(matched[1]);
            }
        }

        //alert(query.replace(regex, ""));
        */
    };

});
