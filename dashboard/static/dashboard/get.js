$(init);
        function init(){
            var canvas = $(".canvas");
            var diagram = [];
            var tool = $(".tool");
            $(".tool").draggable({
                helper:"clone"
            });
            $(".canvas").droppable({
                drop: function(event, ui){
                    //alert("tool was dropped");
                    var node = {
                        _id : (new Date).getTime(),
                        position : ui.helper.position()
                        
                        
                    }
                    node.position.left -= tool.width();
                    if(ui.helper.hasClass("tool-1")){
                        node.type = "tool-1";
                        node.source = $(".card-1 img").attr("src");
                        console.log(node);
                    }else if(ui.helper.hasClass("tool-2")){
                        node.type = "tool-2";
                        node.source = $(".card-2 img").attr("src");
                        console.log(node);
                    }else if(ui.helper.hasClass("tool-3")){
                        node.type = "tool-3";
                       
                        node.source = $(".card-3 img").attr("src");
                        console.log(node);
                    }else if(ui.helper.hasClass("tool-4")){
                        node.type = "tool-4";
                        //node.source = $(".card img").attr("src");
                        console.log(node);
                    }else{
                        return;
                    }
                    diagram.push(node);
                    renderDiagram(diagram);
                }
            });

            function renderDiagram(diagram) {
                canvas.empty();
                for(var d in diagram){
                    var node = diagram[d];
                    var html="";
                    if(node.type=="tool-1"){
                        html = "<img src = \" "+ node.source +  "\" width = 200px height = 200px>";
                    }else  if(node.type=="tool-2"){
                        html = "<img src = \" "+ node.source +  "\" width = 200px height = 200px>";
                    }else  if(node.type=="tool-3"){
                        html = "<img src = \" "+ node.source +  "\" width = 200px height = 200px>";
                        console.log(node);
                    }else  if(node.type=="tool-4"){
                        html = "<img src = \" "+ node.source +  "\" width = 200px height = 200px>";
                    }
                    var dom = $(html).css({
                        "position":"absolute",
                        "top":node.position.top,
                        "left":node.position.left
                    }).draggable({
                        stop:function(event,ui){
                            console.log(ui);
                            var id = ui.helper.attr("id");
                            for(var i in diagram){
                                if(diagram[i]._id == id){
                                        diagram[i].position.top = ui.position.top;
                                        diagram[i].position.left = ui.position.left;
                                }
                            }
                        }
                    }).attr("id", node._id);
                    canvas.append(dom);
                }

            }
        }