document.querySelectorAll(".file-input-method").forEach(inputElement => {
  const dropZoneElement = inputElement.closest(".drop-area");
  const form = document.querySelector("form");
  const convert = document.querySelector(".convert_files_button");
  const flash = document.querySelector("#files_dropped_flash");


  // click to upload
  dropZoneElement.addEventListener("click", e => {
    console.log("clicked to upload");
    inputElement.click();
  });

  // Detects dragging files into drop area
  dropZoneElement.addEventListener("dragover", e => {
    console.log("Hovering over drop area");
    e.preventDefault();
  });

  // Detects when the mouse leaves the drop area
  ["dragleave", "dragend"].forEach(type => {
    dropZoneElement.addEventListener(type, e => {
      e.preventDefault();
    });
  });

  // Handles files when dropped and makes a POST request to the flask route
  dropZoneElement.addEventListener("drop", e => {

    flash.textContent = "Files dropped";

    let dt = e.dataTransfer
    var f, files = dt.files

    let formData = new FormData(form)

    for (f of files) {
      formData.append('file', f)
      console.log(f)
    }

    fetch(session_id, {
      method: 'POST',
      body: formData
    })

    console.log("file sent");

    e.preventDefault();
  });

  // Convert files button
  convert.addEventListener("click", e => {
    window.location.replace(redirect_page);
  }); 
  

});

