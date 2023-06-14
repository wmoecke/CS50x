// Startup of the main application code
const startUp = () => {
    // Render all the background one time
    renderBackground();

    // Get the curent time (HHmmss) and process all of the dots
    setInterval(() => {
        let time = new Date().toTimeString().match("[0-9]{1,2}:[0-9]{2}:[0-9]{2}")[0].replaceAll(":", "")
        processDots(time);
    }, 1000);
}

const processDots = (time) => {
    // Get all the dots
    let dots = document.querySelectorAll(`div[id^="dot"]`);

    // For each dot, we set the digits from the binary time
    dots.forEach(dot => {
        // Get the time part according to dot id in binary,
        // then get the bit (either 0 or 1) that should be set
        var binaryTimePart = convertToBinary(parseInt(time[parseInt(dot.id.substr(3, 1))]));
        var bit = binaryTimePart[parseInt(dot.id.substr(4, 1))];
        // Style each dot according to selected skin setting
        renderDot(dot, bit);
    });
}

const renderDot = (dot, bit) => {
    // Read the skin preset from local settings
    let skin = localStorage.getItem("BinaryClockSkin") || "default";
    let backlit = (localStorage.getItem("BinaryClockBacklit") || "false") === "true";

    // According to selected skin, style the changes appropriately for the current dot
    switch(skin) {
    case "lcd":
    case "default":
        dot.style.backgroundColor = bit == "0" ? skin == "lcd" ? "transparent" : "#eee" : "#000";
        dot.style.borderColor = "#000";
        if(skin == "lcd" && !backlit) {
            dot.style.boxShadow = skin == "lcd" ? bit == "1" ? "2px 2px 2px #aaa" : "2px 2px 2px #aaa, 2px 2px 2px #aaa inset" : null;
        }
        break;
    case "acrylic-red":
    case "brushedSteel-red":
        dot.style.backgroundColor = bit == "0" ? "#b30000" : "#ff5050"
        dot.style.borderColor = bit == "0" ? skin == "brushedSteel-red" ? "#b34444" : "#b30000" : skin == "brushedSteel-red" ? "#ff8080" : "#ff2a2a";
        dot.style.animation = bit == "0" ? skin == "brushedSteel-red" ? "fade-led-red 1s linear infinite" : null : skin == "brushedSteel-red" ? "glow-led-red 1s linear infinite" : null;
        break;
    case "acrylic-green":
    case "brushedSteel-green":
        dot.style.backgroundColor = bit == "0" ? "#00b300" : "#50ff50"
        dot.style.borderColor = bit == "0" ? "#00b300" : "#66ff66";
        dot.style.animation = bit == "0" ? skin == "brushedSteel-green" ? "fade-led-green 1s linear infinite" : null : skin == "brushedSteel-green" ? "glow-led-green 1s linear infinite" : null;
        break;
    case "acrylic-blue":
    case "brushedSteel-blue":
        dot.style.backgroundColor = bit == "0" ? "#0000b3" : "#5050ff"
        dot.style.borderColor = bit == "0" ? "#0000b3" : "#6666ff";
        dot.style.animation = bit == "0" ? skin == "brushedSteel-blue" ? "fade-led-blue 1s linear infinite" : null : skin == "brushedSteel-blue" ? "glow-led-blue 1s linear infinite" : null;
        break;
    }
}

const renderBackground = () => {
    // Read the skin preset and size from local settings
    let skin = localStorage.getItem("BinaryClockSkin") || "default";
    let size = localStorage.getItem("BinaryClockSize") || "400px";
    let backlit = (localStorage.getItem("BinaryClockBacklit") || "false") === "true";

    // Get the container div
    let container = document.querySelector("#container");

    // Get all the table rows
    let rows = document.querySelectorAll("tr");

    // Style the container
    container.style.width = size;
    container.style.height = "208px";

    // According to selected skin, style the changes appropriately for the container
    switch(skin) {
        case "lcd":
        case "default":
            container.backgroundColor = "transparent";
            rows.forEach(row => {
                row.style.borderColor = skin == "lcd" ? "#000" : "#dee2e6";
            });
            break;
        case "acrylic-red":
        case "brushedSteel-red":
            container.style.background = "linear-gradient(to bottom right, #990000, #b32a2a)";
            rows.forEach(row => {
                row.style.borderColor = "#ff1a1a";
                row.style.color = "#ff1a1a";
            });
            break;
        case "acrylic-green":
        case "brushedSteel-green":
            container.style.background = "linear-gradient(to bottom right, #00a300, #66cc66)";
            rows.forEach(row => {
                row.style.borderColor = "#66ff66";
                row.style.color = "#66ff66";
            });
            break;
        case "acrylic-blue":
        case "brushedSteel-blue":
            container.style.background = "linear-gradient(to bottom right, #0000a3, #6666cc)";
            rows.forEach(row => {
                row.style.borderColor = "#6666ff";
                row.style.color = "#6666ff";
            });
            break;
    }

    if(skin == "lcd") {
        container.style.backgroundImage = "linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), url('static/images/brushed_steel.jpg')";
        container.style.backgroundSize = "cover";
        container.style.filter = "sepia(25%)";
        container.style.animation = backlit ? "glow-lcd-backlit 1s linear infinite" : null;
        if(!backlit) {
            document.querySelector(`div:not([id^="dot"])`).style.textShadow = "2px 2px 1px #aaa";            
            rows.forEach(row => {
                row.style.boxShadow = "0 2px 1px #aaa";  
            });
        }
    }

    if(skin.includes("brushedSteel")) {
        container.style.backgroundImage = "url('static/images/brushed_steel.jpg')";
        container.style.backgroundSize = "cover";
        rows.forEach(row => {
            row.style.textShadow = "0 1px 0 #fff";
            row.style.borderStyle = "groove";
            row.style.borderColor = "#dee2e6";
            row.style.color = "#000";
        });
    }
}

const convertToBinary = (decimal) => {
    var binary = "";

    // Extract the binary digits
    while (decimal > 0) {
       if (decimal & 1) {
          binary = "1" + binary;
       } else {
          binary = "0" + binary;
       }
       decimal = decimal >> 1;
    }

    // Pad with zeroes
    for (i = 6 - binary.length; i > 0; i--) {
        binary = "0" + binary;
    }
    return binary;
}

document.addEventListener('DOMContentLoaded', startUp);