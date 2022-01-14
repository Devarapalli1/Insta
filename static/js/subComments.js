function displayComments(event, currentObj) {
    element = currentObj.nextElementSibling
    // console.log(element.style.display)
    if (element.style.display == "none") {
        element.style.display = "block"
    } else if (element.style.display == "block") {
        element.style.display = "none"
    }
}