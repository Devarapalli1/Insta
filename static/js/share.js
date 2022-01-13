function displayMessage(event, currentObj) {
    element = currentObj.getElementsByClassName("share-message")[0]
    element.style.display = "block";
    url = currentObj.getElementsByClassName("copy-url")[0].getAttribute("value")
    navigator.clipboard.writeText(window.location.host + url)

    setTimeout(() =>
        element.style.display = "none", 3000)
}