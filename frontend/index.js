const operation_name_map = {
  "Edge Detection": "edge_detection",
  "Corner Detection": "corner_detection",
  "Gaussian Blur": "gaussian_blur",
  "Median Blur": "median_blur",
  "Fourier Transform": "fourier_transform",
  "Contrast Enhancement": "contrast_enhancement",
  "Background Removal": "background_removal",
  "Color Inversion": "color_inversion",
};

document.querySelector('input[type="file"]').addEventListener("change", function (event) {
  let imageFiltersDiv = document.getElementById("imageFilters");
  imageFiltersDiv.innerHTML = "";

  let files = event.target.files;
  for (let i = 0; i < files.length; i++) {
    let select = document.createElement("select");
    select.name = "imageFilters[]";
    select.style.display = "block";
    let options = [
      "Edge Detection",
      "Corner Detection",
      "Gaussian Blur",
      "Median Blur",
      "Fourier Transform",
      "Contrast Enhancement",
      "Background Removal",
      "Color Inversion",
      "All Operations",
    ];
    for (let j = 0; j < options.length; j++) {
      let option = document.createElement("option");
      option.value = options[j];
      option.text = options[j];
      select.appendChild(option);
    }
    let placeholderOption = document.createElement("option");
    placeholderOption.value = "";
    placeholderOption.text = "Please choose operation for Image " + (i + 1);
    placeholderOption.disabled = true;
    placeholderOption.selected = true;
    select.insertBefore(placeholderOption, select.firstChild);
    imageFiltersDiv.appendChild(select);
  }

  let uploadedImagesDiv = document.getElementById("uploadedImages");
  uploadedImagesDiv.innerHTML = "";
  for (let i = 0; i < files.length; i++) {
    let image = document.createElement("img");
    image.classList.add("uploaded-image");
    image.src = URL.createObjectURL(files[i]);
    uploadedImagesDiv.appendChild(image);
  }
});

document.getElementById("uploadForm").addEventListener("submit", function (event) {
  event.preventDefault();

  let files = document.querySelector('input[type="file"]').files;
  let selects = document.querySelectorAll('select[name="imageFilters[]"]');

  Array.from(files).forEach((file, i) => {
    let operation = selects[i].value;

    if (operation === 'All Operations') {
      Object.keys(operation_name_map).forEach((key) => {
        if (key !== 'Background Removal') {
          sendRequest(file, operation_name_map[key], i);
        }
      });
    } else {
      sendRequest(file, operation_name_map[operation], i);
    }
  });
});

function sendRequest(file, operation, index) {
  let formData = new FormData();
  formData.append("image", file);
  formData.append("operation", operation);

  const REQUEST_NUMBER = 3; // Number of retry attempts
  let requestCount = 0; // Counter for the number of requests made

  function makeRequest() {
    fetch("http://application-and-web-server-LB-570742999.eu-north-1.elb.amazonaws.com:8000/process-image", {
      method: "POST",
      body: formData,
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.blob();
    })
    .then((blob) => {
      let image_url = URL.createObjectURL(blob);
      let a = document.createElement("a");
      a.href = image_url;
      a.download = `image ${index + 1} ${operation}`;
      document.body.appendChild(a);
      a.click();
      URL.revokeObjectURL(image_url);
    })
    .catch((error) => {
      requestCount++;
      if (requestCount < REQUEST_NUMBER) {
        // Retry the request
        makeRequest();
      } else {
        // Display error message to user screen
        alert("Processing Image number " + (index + 1) + " Failed");
      }
    });
  }

  // Call the makeRequest function to initiate the request
  makeRequest();
}
