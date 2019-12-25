var links = document.getElementsByClassName('OrderCard-TitleLink');
var array = [];
for(var items of links) {
    array.push(items.href)
}
// noinspection JSAnnotator
return array