
class TreeSelect {

    constructor(element, json){
        var self = this;

        this.element = element;
        this.input = document.createElement("INPUT");
        this.input.setAttribute('type','text');
        this.input.setAttribute('class','w3-dysplay-container w3-import w3-rounded treeSearchInput');
        this.input.onfocus = function(){
            console.log("gaaaaaaaaaaa");
            self.div.style.display='block';
        }

        element.appendChild(this.input);

        this.div = document.createElement("NAV");
        this.div.setAttribute("class","w3-card tree-div-selector")
        this.onclick =
        element.appendChild(this.div);

        this.data = "None";
        this.path = [];

        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                self.data = JSON.parse(this.responseText);
                //self.path.push(self.data);
                self.loadLevel(self.data);
            }
            else{
                console.warn("error at loading the json: "+this.status);
            }
        };
        xmlhttp.open("GET", json, true);
        xmlhttp.send();
    }


    loadLevel(level){
        self = this;
        self.path.push(level);
        this.div.innerHTML = "";
        console.log(self);

        //header
        if(this.path.length > 1){
            var nav = document.createElement("DIV");

            for(var i=0;i<this.path.length-1;i++){
                var textNode = document.createElement("SPAN");
                textNode.setAttribute("class","w3-button")
                textNode.appendChild(document.createTextNode(this.path[i].text));
                console.log(i);
                textNode.onclick = (function(){
                    var cont=i;
                    return function(event){
                        level = self.path[cont];
                        self.path.length = cont;
                        self.loadLevel(level);
                        event.stopPropagation();
                    };
                })();

                nav.appendChild(textNode);

                var arrow = document.createElement("SPAN");
                var arrowIcon = document.createElement("I");
                arrowIcon.setAttribute("class","fa fa-angle-right");
                //arrows.setAttribute("style","font-size:24px");
                arrow.appendChild(arrowIcon);
                nav.appendChild(arrow);
            }

            var lastNode = document.createElement("SPAN");
            lastNode.setAttribute("class","w3-button")
            lastNode.appendChild(document.createTextNode(this.path[this.path.length-1].text));
            nav.appendChild(lastNode);

            this.div.appendChild(nav);
        }

        //body
        for (var i=0; i<level.children.length; i++){

            var child = level.children[i];
            var line = document.createElement("DIV");
            line.setAttribute("class","w3-bar");

            var text = document.createElement("SPAN");
            text.appendChild(document.createTextNode(child.text));
            text.setAttribute("class","w3-left w3-button");
            text.onclick = function(){

            }
            line.appendChild(text);

            if(child.children.length > 0){
                var arrows = document.createElement("I");
                arrows.setAttribute("class","w3-right w3-button fa fa-angle-double-right");
                arrows.setAttribute("style","font-size:24px");
                arrows.onclick = (function(){
                    let nextLevel = child;
                    return function(event){
                        self.loadLevel(nextLevel);
                        event.stopPropagation();
                    };
                })();
                line.appendChild(arrows);

            }

            this.div.appendChild(line);
        }
    }


}

var selectors=[];
var selectorsDivs=[];
window.addEventListener("load",function(event) {
    var divs = document.getElementsByClassName("tree_select");

    for (var i=0; i<divs.length; i++){
        selectors.push(new TreeSelect(divs[i],'/static/json/hierarchy.json'));
        selectorsDivs.push(selectors[i].element);
    }
},false);

document.addEventListener("click", function(e){
    var target = (e && e.target) || (event && event.srcElement);
    var display = -1;

    while (target.parentNode) {
        console.log("gaaaaaaaa");

        display=selectorsDivs.indexOf(target);
        if (display>=0) {
            console.log("gaaaaaaaa3");
            break;
        }
        target = target.parentNode;
    }
    if(display<0){
        for(let i = 0; i < selectors.length; i++) {
            console.log("gaaaaaaaa2");
            selectors[i].div.style.display = "none";
        }
    }

});
