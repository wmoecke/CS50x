function editEntry(id, name, month, day) {
    // Get the input fields and button
    var nameInput = document.querySelector('#name');
    var monthInput = document.querySelector('#month');
    var dayInput = document.querySelector('#day');
    var submit = document.querySelector('#submit');

    // Set the current values to the input fields and change button text
    nameInput.value = name;
    monthInput.value = month;
    dayInput.value = day;
    submit.innerText = "Save Birthday";

    // Get the h2 header and change the text
    var h2 = document.querySelector('#addOrEditHeader');
    h2.innerText = "Edit a Birthday";

    // Get the form and change the action so we can call it later
    var form = document.querySelector('#addOrEditForm');
    form.action = "/update";

    // Create a hidden input 'id' field
    var hiddenInput = document.createElement('input');
    hiddenInput.type = "hidden";
    hiddenInput.value = id;
    hiddenInput.name = "birthdayId"

    // Attach the input to the form so we can retrieve its value later
    form.appendChild(hiddenInput);

    nameInput.focus();
}