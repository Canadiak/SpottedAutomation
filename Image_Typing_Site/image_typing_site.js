
function check_overflow(el) {
    var curOverf = el.style.overflow;
    
    if ( !curOverf || curOverf === "visible" )
        el.style.overflow = "hidden";
    
    console.log(el.clientHeight);
    console.log(el.scrollHeight);
    console.log(el.clientWidth);
    
    console.log(el.scrollWidth);
    var isOverflowing = el.clientWidth < el.scrollWidth
        || (el.clientHeight+30) < el.scrollHeight;
    
    el.style.overflow = curOverf;
    
    return isOverflowing;
}

pixels_of_font = 30;
block_div = document.querySelector("#block_div");
block_div.style.fontSize = "30px";
block_div.style.overflow = "visible";

console.log(block_div.style.fontSize)
console.log(typeof block_div.style.fontSize)
console.log(block_div.style.overflow);
console.log(check_overflow(block_div));

while ( check_overflow(block_div) && parseInt(block_div.style.fontSize.replace('px','')) > 20){
    console.log("check");
    block_div.style.fontSize = (parseInt(block_div.style.fontSize.replace('px',''))-2).toString() + "px";
} 
console.log(check_overflow(block_div));
console.log(block_div.style.overflow); 
