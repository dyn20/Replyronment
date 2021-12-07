const btnshow = document.querySelector(".btn");
const elementshow = document.getElementById('show');
console.log(elementshow)
btnshow.onclick = () => {
    if (elementshow.style.display !== 'none') {
        elementshow.style.display = 'none'
    } else {
        elementshow.style.display = 'inline'
    }
}