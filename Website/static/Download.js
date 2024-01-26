const convert = document.querySelector(".convert_button");
const download = document.querySelector(".download_button");
const convert_element = document.querySelector("#convert");
const download_element = document.querySelector("#download");

// Convert button
convert.addEventListener("click", e => {
    console.log("Convert more clicked!")
    convert_element.click()
});

// Download button
download.addEventListener("click", e => {
    console.log("Download clicked!")
    download_element.click()
});
