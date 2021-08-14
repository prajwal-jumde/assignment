document.onreadystatechange = function() { 
    if (document.readyState !== "complete") { 
        startLoader();
    } else { 
        stopLoader();
    } 
}; 

function startLoader() {

    document.querySelector("body").style.visibility = "hidden"; 
    document.querySelector("#loader").style.visibility = "visible"; 
}

function stopLoader() {
    document.querySelector("#loader").style.display = "none"; 
    document.querySelector("body").style.visibility = "visible"; 
}