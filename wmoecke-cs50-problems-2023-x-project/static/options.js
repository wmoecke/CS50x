// Saves options to local storage
const saveOptions = () => {
    localStorage.setItem("BinaryClockSkin", document.querySelector('#skin').value);
    localStorage.setItem("BinaryClockSize", document.querySelector('#size').value);

    // Update status to let user know options were saved.
    let status = document.querySelector('#status');
    status.textContent = 'Settings saved!';
    status.style.display = "block";
    setTimeout(() => {
        status.textContent = '';
        status.style.display = "none";
    }, 1500);
};

// Restores select state using the preferences stored in local storage.
const restoreOptions = () => {
    document.querySelector('#save').addEventListener('click', saveOptions);
    document.querySelector('#status').style.display = "none";
    document.querySelector('#skin').value = localStorage.getItem("BinaryClockSkin") || "default";
    document.querySelector('#size').value = localStorage.getItem("BinaryClockSize") || "400px";
};

document.addEventListener('DOMContentLoaded', restoreOptions);
