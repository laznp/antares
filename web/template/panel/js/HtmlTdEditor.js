function HtmlTdEditor(Object){
    this.Object = Object;
    
    this.getHtmltags = function(){
        var tags = "<td ";
        tags += "class=";
        tags += "'"+this.Object+"'";
        tags += ">";
        tags += "<div class='name'>";
        tags += this.Object.name;
        tags += "</div>";
        tags += '</td>';
        
        this.tags = tags;
        return tags;
    };
}

