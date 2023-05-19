// Saves options to local storage
const saveOptions = () => {
    localStorage.setItem("BinaryClockSkin", document.querySelector('#skin').value);
    localStorage.setItem("BinaryClockSize", document.querySelector('#size').value);
    localStorage.setItem("BinaryClockBacklit", document.querySelector('#backlight').checked ? "true" : "false");

    // Update status to let user know options were saved.
    let status = document.querySelector('#status');
    status.textContent = 'Settings saved!';
    status.style.display = "block";
    setTimeout(() => {
        status.textContent = '';
        status.style.display = "none";
    }, 1500);
};

const toggleCheckboxVisibilityOnSkinChange = () => {
    document.querySelector('#backlight-wrapper').style.display = document.querySelector('#skin').value == "lcd" ? "block" : "none";
};

// Restores select state using the preferences stored in local storage.
const restoreOptions = () => {
    document.querySelector('#save').addEventListener('click', saveOptions);
    document.querySelector('#skin').addEventListener('change', toggleCheckboxVisibilityOnSkinChange);
    document.querySelector('#status').style.display = "none";
    document.querySelector('#skin').value = localStorage.getItem("BinaryClockSkin") || "default";
    document.querySelector('#size').value = localStorage.getItem("BinaryClockSize") || "400px";
    document.querySelector('#backlight').checked = (localStorage.getItem("BinaryClockBacklit") || "false") === "true";
    document.querySelector('#backlight-wrapper').style.display = document.querySelector('#skin').value == "lcd" ? "block" : "none";
};

document.addEventListener('DOMContentLoaded', restoreOptions);
