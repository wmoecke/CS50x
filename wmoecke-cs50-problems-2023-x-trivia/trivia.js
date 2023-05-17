function checkButton(id) {
    var el = document.querySelector('#' + id);
    if (id.includes('correct')) {
        el.value = 'Correct!';
        el.style.backgroundColor = 'green';
    } else {
        el.value = 'Incorrect';
        el.style.backgroundColor = 'red';
    }
}

function checkText() {
    var txt = document.querySelector('#txtQuestion');
    var par = document.querySelector('p');
    if (txt.value.toLowerCase().includes('syfo dyas')) {
        par.innerHTML = 'Correct!';
        txt.style.backgroundColor = 'green';
    } else {
        par.innerHTML = 'Incorrect';
        txt.style.backgroundColor = 'red';
    }
}