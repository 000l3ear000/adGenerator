// var INPUT_FILE, TEMPLATE_NAME;
var txtLength = 0;
const inputs = {};

const size_type = (e) => {
    const supportedVidExt = ['mp4', 'webM', 'mov', 'mpeg-4', 'flv', 'avi', 'mkv', 'wmv', 'quicktime'];
    const supportedImageExt = ['jpeg', 'png', 'jpg', 'svg'];
    const file = e.target.files[0];
    var arr = file.type.split('/');
    
    if( !(arr[0]=="image" && supportedImageExt.includes(arr[1])) && !(arr[0]=="video" && supportedVidExt.includes(arr[1]))){
        addPara( "File type is not supported" );

    }
    else {
        if( (file.size / 1024) / 1024 > 10 ){
            // addPara( "file is too large, Max file size is 10 MB" );
            var err_msg_div = document.getElementById("err_msg");
            err_msg_div.innerHTML = "file is too large, Max file size is 10 MB";
            setTimeout( () => {
                err_msg_div.innerHTML = '';
            }, 3000);
        }
        else{
            addPara(":)")
            INPUT_FILE = file;
            inputs.input_file = file;
            console.log(inputs);
        }
    }
    // addPara("File " + file.name + " is " + file.size + " bytes in size");
}

function addPara(text) {
    var p = document.createElement("p");
    p.textContent = text;
    document.body.appendChild(p);
}

const getTextInputs = ( len ) => {
    var flag = 1;
    const textArray = [];
    for ( var i = 0; i < len; i++ ){
        const tempTextInput = document.getElementById("Text" + (i + 1));
        if(tempTextInput.value.length < 6){
            flag = 0;
            break
        }
        else{
            textArray.push(tempTextInput.value);
        }
    }
    if(flag){
        inputs["text_inputs"] = textArray;
        return flag;
    }    
}

const validateText = (e) => {
    
    // console.log(e.target.value);
    if ( e.target.value.length < 6 ){
        var err_msg_div = document.getElementById("err_msg");
        err_msg_div.innerHTML = "The Text should be atleast 6 characters long";
        setTimeout( () => {
            err_msg_div.innerHTML = '';
        }, 3000);
    }
}

const checkTrue = (e) => {

    e.path[1].childNodes[0].checked = true;
    // console.log(e.path[1].childNodes[0].value);
    const templateName = e.path[1].childNodes[0].value;

    var textInputLength;
    const getTxt = document.getElementById("textInputs");
    getTxt.innerHTML = "";

    if ( templateName == "template5" || templateName == "template6" ){
        textInputLength = 4;
    }
    else {
        textInputLength = 5;
    }

    txtLength = textInputLength;

    for ( var i = 0; i < textInputLength; i++ ){
        
        var tempTextInput = document.createElement("input");
        tempTextInput.type = "text";
        tempTextInput.id = "Text" + (i + 1);
        tempTextInput.placeholder = "Text" + " " +(i+1); 
        tempTextInput.required = true;
        tempTextInput.maxLength = "20"
        // tempTextInput.oninput = validateText();
        getTxt.appendChild( tempTextInput );
    }

    for ( var i = 0; i < textInputLength; i++ ){     
        // var textInput = document.getElementById( "Text" + (i + 1) );
        document.getElementById( "Text" + (i + 1) ).addEventListener("focusout", validateText);
        document.getElementById( "Text" + (i + 1) ).addEventListener("propertychange", validateText);
        // textInput.onchange = validateText( "Text" + (i + 1) );
    }

    TEMPLATE_NAME = templateName;
    inputs.template_name = templateName;
    console.log(inputs.template_name);
    // inputs["input_text"] = []
}

const createTemplatesDiv = () => {
    
    var templatesDiv = document.getElementById("template_container");
    
    for ( var i = 0; i < 20; i++ ){
        
        var tempDiv = document.createElement("div");
        var tempInput = document.createElement("input");
        tempInput.type = "radio";
        tempInput.name = "template";
        const ppd = "template" + (i + 1);
        tempInput.value = ppd;
        var tempImage = document.createElement("img");
        tempImage.src = "http://localhost:3000/static/temp.jpeg"
        tempImage.onclick = checkTrue;

        tempDiv.classList.add("template_single");
        tempDiv.id = "template_div_single"
        tempDiv.appendChild( tempInput );
        tempDiv.appendChild( tempImage );
        
        templatesDiv.appendChild(tempDiv);
        
    }


}
document.getElementById("plan").addEventListener("change",()=>{
    document.getElementById("templateMusic").src="http://localhost:3000/static/" + document.getElementById("plan").value;
    inputs.template_music = document.getElementById("plan").value;
    console.log(">>>", inputs.template_music)
})



document.getElementById("fileInput").addEventListener("change", size_type);
// console.log(inputs);

// document.getElementById("fontColorPicker").addEventListener("change", printColorCode);
// document.getElementById("template_container").addEventListener("load", createTemplatesDiv);
window.onload = createTemplatesDiv;

// document.getElementById("btn_next").addEventListener("click", console.log(inputs))
const finalInputs = () => {
    if(inputs.input_file && inputs.template_name && inputs.template_music){
        console.log("i am here");
        console.log(txtLength);
        const result = getTextInputs(txtLength);

        inputs.font_color = document.getElementById("fontSizes").value;
        inputs.font_style = document.getElementById("fontStyles").value;
        inputs.font_color = document.getElementById("fontColor").value;
        inputs.font_size = document.getElementById("fontSizes").value;
        inputs.font_fade = document.getElementById("fontFadeEffect").value;
        

        if(result){

            console.log(inputs);
            console.log("navigate now!!")
            const fileObj = inputs.input_file;
            var data = new FormData()
            data.append('input_file', fileObj);
            data.append('inputs', JSON.stringify(inputs));
            
            fetch( "http://localhost:3000/upload", {
                method: 'POST',
                body: data
            })
            .then( res => res.json() )
            .then( data => {
                if( data.status == "success" ) console.log(data.fileName);
            })

            // .then( res => res.json()
            // .then( data => {
            //     if ( data.status == "success" ){
            //         console.log(data)
            //         console.log("video generated >>> ", data.fileName);
            //     }
            // })
            // )
        }        
    }
           
}
