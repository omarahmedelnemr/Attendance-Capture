const sleepNow = (delay) => new Promise((resolve) => setTimeout(resolve, delay))


// Click on the Form Enywhare
function uploadOnClick(){
    document.getElementById("uploadButton").click()
}

// Submit the Form on Change
async function submitForm() {
    event.preventDefault(); // Prevent the default form submission
    var form = document.getElementById('uploadForm');

    var formData = new FormData(form)
    var xhr = new XMLHttpRequest();
    document.getElementById("LoadingScreen").classList.remove("hidden")
    document.getElementById("loadingStatus").innerHTML = "Uploading"
    await sleepNow(100)
    document.getElementById("LoadingScreen").style.opacity = 1

    xhr.open('POST', '/upload', true);
    xhr.onreadystatechange = async function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log('File uploaded successfully!');
            console.log(xhr.response)
            document.getElementById("org_image").src = "/file/"+xhr.response
            document.getElementById("imageName").innerHTML = xhr.response
            document.getElementById("org_image").classList.remove("hidden")
            document.getElementById("file_upload").classList.add("hidden")

        }
        document.getElementById("LoadingScreen").style.opacity = 0
        await sleepNow(100)
        document.getElementById("LoadingScreen").classList.add("hidden")
    };
    xhr.send(formData);
}

// Send to Detect Faces (Click on Detect)
async function sendPredict(){
    // Read the imageName attribute from the img element
    var imageName = document.getElementById('org_image').getAttribute('src');

    // Check if the Image not Yet Uploaded
    if (imageName == './'){
        document.getElementById("ShowError").classList.remove('hidden')
        document.getElementById("ShowError").innerHTML = "You Have To Upload a File First"
        return 
    }else if(document.getElementById("classNameInput").value == ''){
        document.getElementById("ShowError").classList.remove('hidden')
        document.getElementById("ShowError").innerHTML = "You Must Write The Class Code"
        return 
    }
    // document.getElementById("mainBody").classList.add("dark")
    document.getElementById("ShowError").classList.add('hidden')
    document.getElementById("LoadingScreen").classList.remove("hidden")
    document.getElementById("loadingStatus").innerHTML = "Proccessing"
    await sleepNow(100)
    document.getElementById("LoadingScreen").style.opacity = 1
    // Make an AJAX request to the /predict endpoint
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/predict', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Set up the data to send in the request body
    var data = JSON.stringify({ imageName: imageName, classCode : document.getElementById("classNameInput").value.toUpperCase() });

    xhr.onreadystatechange =async  function() {
        document.getElementById("body").classList.add("dark")

        if (xhr.readyState == 4) {
            if (xhr.status == 200) {

                document.getElementById("classNameInput").value = document.getElementById("classNameInput").value.toUpperCase()
                document.getElementById("classNameInput").style.pointerEvents = 'none'
                document.getElementById("classNameInput").disabled = true
                document.getElementById("loadingStatus").innerHTML = "Extracting Faces"
                var  newName = document.getElementById("imageName").innerHTML.split(".")[0]
                document.getElementById("predicted_image").src =  "/file/"+ newName + "_predicted.jpg"
                var counter = 0
                document.getElementById("faces_container").innerHTML = ''
                const container = document.getElementById("faces_container")
                
                for (var i of JSON.parse(xhr.responseText)){

                    var item = document.createElement("div");
                    item.className = "face_image";
                    item.innerHTML = `
                            <img src="/file/${i.image_path}" />
                            <label class=''>${i.label}</label>
                    `;
                    container.appendChild(item);
                    
                    counter+=1;
                }
                var allE = document.getElementsByClassName("face_image")
                for(var i = 0;i< allE.length;i++){
                    await sleepNow(300)
                    document.getElementsByClassName("face_image")[i].style.opacity = 1;
                    // if(i>16 & i%2 ==0){
                    if(i>9){
                        document.getElementById("faces_container_frame").scrollTop += 95

                    }
                }
                document.getElementById("showPredictedButton").classList.remove("hidden")
                document.getElementById("showPredictedButton").click()
                document.getElementById("loadingStatus").innerHTML = "All Done"
                await sleepNow(300)
                document.getElementById("LoadingScreen").style.opacity = 0
                await sleepNow(100)
                document.getElementById("LoadingScreen").classList.add("hidden")
                document.getElementById("DownloadSheetButton").classList.remove("hidden")
                document.getElementById("DownloadCSVSheetButton").classList.remove("hidden")
            } else {
                console.error('Error:', xhr.status);
            }
        }
    };

    // Send the request
    xhr.send(data);
}

// Show the Predicted Image
function showPredicted(){
    
    document.getElementById("predicted_image").classList.remove("hidden")
    document.getElementById("org_image").classList.add("hidden")

    document.getElementById("showOriginalButton").classList.remove("hidden")
    document.getElementById("showPredictedButton").classList.add("hidden")

}

// Show the Original Image
function showOriginal(){
    document.getElementById("predicted_image").classList.add("hidden")
    document.getElementById("org_image").classList.remove("hidden")

    document.getElementById("showPredictedButton").classList.remove("hidden")
    document.getElementById("showOriginalButton").classList.add("hidden")

}


// Download The Final Sheet
function downloadSheet() {
    // Define the URL for the /downloadSheet endpoint
    const url = '/downloadSheet';

    // Create a FormData object and append the textToSend to it
    const formData = new FormData();
    formData.append('classCode', document.getElementById("classNameInput").value);

    // Make a fetch request to the server
    fetch(url, {
        method: 'POST',  // Use 'POST' method since you are sending data
        body: formData    // Attach the FormData object as the request body
    })
    .then(response => {
        // Check if the request was successful (status code 200)
        if (response.ok) {
            // Convert the response to blob
            return response.blob();
        } else {
            // Handle the error
            throw new Error('Failed to download sheet');
        }
    })
    .then(blob => {
        // Create a link element
        const link = document.createElement('a');

        // Set the href attribute to a Blob URL representing the data
        link.href = URL.createObjectURL(blob);

        // Set the download attribute with the desired filename
        link.download = document.getElementById("classNameInput").value + '_Attendance_sheet.xlsx';

        // Append the link to the document body
        document.body.appendChild(link);

        // Programmatically trigger a click event on the link to start the download
        link.click();

        // Remove the link from the document body
        document.body.removeChild(link);
    })
    .catch(error => {
        console.error(error);
    });
}

// Download The Final Sheet
function downloadCSVSheet() {
    // Define the URL for the /downloadSheet endpoint
    const url = '/downloadCSV';

    // Create a FormData object and append the textToSend to it
    const formData = new FormData();
    formData.append('classCode', document.getElementById("classNameInput").value);

    // Make a fetch request to the server
    fetch(url, {
        method: 'POST',  // Use 'POST' method since you are sending data
        body: formData    // Attach the FormData object as the request body
    })
    .then(response => {
        // Check if the request was successful (status code 200)
        if (response.ok) {
            // Convert the response to blob
            return response.blob();
        } else {
            // Handle the error
            throw new Error('Failed to download sheet');
        }
    })
    .then(blob => {
        // Create a link element
        const link = document.createElement('a');

        // Set the href attribute to a Blob URL representing the data
        link.href = URL.createObjectURL(blob);

        // Set the download attribute with the desired filename
        link.download = document.getElementById("classNameInput").value + '_Attendance_sheet.csv';

        // Append the link to the document body
        document.body.appendChild(link);

        // Programmatically trigger a click event on the link to start the download
        link.click();

        // Remove the link from the document body
        document.body.removeChild(link);
    })
    .catch(error => {
        console.error(error);
    });
}

