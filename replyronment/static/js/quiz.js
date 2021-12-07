function getParameterByName(name, url = window.location.href) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}
var query = getParameterByName('q')
console.log(query)
if (query == 'bat-dau-quiz' || query === null) {
    document.getElementById('submitbtn').style.display = 'inline'
}