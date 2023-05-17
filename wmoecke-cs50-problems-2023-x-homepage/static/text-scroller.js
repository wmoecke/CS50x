window.addEventListener("load", function() {
    // Get the input field
    var input = document.querySelector('#textToScroll');
    var button = document.querySelector('#submitBtn');

    // Execute a function when the user presses a key on the keyboard
    input.addEventListener("keypress", function(event) {
        // If the user presses the "Enter" key on the keyboard
        if (event.key === "Enter") {
            // Cancel the default action, if needed
            event.preventDefault();
            // Trigger the button element with a click
            button.click();
        }
    });
});

function sendScroll(value) {
    // Get the input field
    var input = document.querySelector('#textToScroll');
    // Get the 'wrapper' div
    var wrapper = document.querySelector('#wrapper');

    // Create child element, give it a classname and set its HTML with the input value
    var div = document.createElement('div');
    div.className = 'scroll';
    div.innerHTML = '<p>' + input.value + '</p>';

    // Cleanup
    input.value = '';
    wrapper.innerHTML = '';

    // Append child to wrapper
    wrapper.appendChild(div);
    // Focus on the input element
    input.focus();
}