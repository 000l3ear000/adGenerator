function fileChange(){
    var file = document.getElementById('input_img');
    var form = new FormData();
    console.log(file.files[0]);
    form.append("image", "logo.png")
    
    var settings = {
      "url": "https://api.imgbb.com/1/upload?key=609eee1e99ab7ebfb29e67d2a600db98",
      "method": "POST",
      "timeout": 0,
      "processData": false,
      "mimeType": "multipart/form-data",
      "contentType": false,
      "data": form
    };
    
    $.ajax(settings).done(function (response) {
      console.log(response);
      var jx = JSON.parse(response);
      console.log(jx.data.url);
    })
}

async function submit() {
    let blob = await new Promise(resolve => (resolve, 'logo.png'));
    let response = await fetch("https://api.imgbb.com/1/upload?key=609eee1e99ab7ebfb29e67d2a600db98", {
      method: 'POST',
      body: blob
    });

    // the server responds with confirmation and the image size
    let result = await response.json();
    console.log(result.data.url);
    // alert(result.message);
  }