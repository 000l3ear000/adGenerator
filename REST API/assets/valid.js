
var txtLength = 0;
const inputs = {};
const tooltips = [
    " 0-3 seconds means the wow factor ",
    "3-6 seconds showing a problem.", 
    " 6-9 seconds telling the solution of this product.", 
    "9-12 seconds tell the benefits of this product.", 
    "12-15 seconds tell one extra benefit or solution."
];

const size_type = (e) => {
    const supportedVidExt = ['mp4', 'webM', 'mov', 'mpeg-4', 'flv', 'avi', 'mkv', 'wmv', 'quicktime'];
    const supportedImageExt = ['jpeg', 'png', 'jpg', 'svg'];
    const file = e.target.files[0];
    var arr = file.type.split('/');
    
    if( !(arr[0]=="image" && supportedImageExt.includes(arr[1])) && !(arr[0]=="video" && supportedVidExt.includes(arr[1]))){
        addPara( "File type is not supported" );

    }
    else {
        if( (file.size / 1024) / 1024 > 20 ){
            // addPara( "file is too large, Max file size is 10 MB" );
            var err_msg_div = document.getElementById("err_msg");
            err_msg_div.innerHTML = "file is too large, Max file size is 20 MB";
            setTimeout( () => {
                err_msg_div.innerHTML = '';
            }, 3000);
        }
        else{
    
            inputs.input_file = file;
            console.log(inputs);
        }
    }
}


const logo_size_type = (e) => {
    const supportedLogoExt = ['jpeg', 'png', 'jpg', 'svg'];
    const file = e.target.files[0];
    var arr = file.type.split('/');
    
    if( !(arr[0]=="image" && supportedLogoExt.includes(arr[1]) )){
        addPara( "File type is not supported" );

    }
    else {
        if( (file.size / 1024) / 1024 > 5 ){
            // addPara( "file is too large, Max file size is 10 MB" );
            var err_msg_div = document.getElementById("err_msg");
            err_msg_div.innerHTML = "file is too large, Max file size is 5 MB";
            setTimeout( () => {
                err_msg_div.innerHTML = '';
            }, 3000);
        }
        else{
    
            inputs.logo_file = file;
            console.log(inputs);
        }
    }
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
    
    if ( e.target.value.length < 6 ){
        var err_msg_div = document.getElementById("err_msg");
        err_msg_div.innerHTML = "<h3>The Text should be atleast 6 characters long</h3>";
        setTimeout( () => {
            err_msg_div.innerHTML = '';
        }, 4000);
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

    // var mainDiv = document.createElement("div");
    getTxt.classList.add("vad_list_content_holder");

    for ( var i = 0; i < textInputLength; i++ ){
        
        var tempTextInput = document.createElement("input");
        var div = document.createElement("div");
        var divText = document.createElement("div");
        var iTag = document.createElement("i");
        var span = document.createElement("span");
        div.classList.add("vad_text_tooltip");
        divText.classList.add("vad_text_field");
        iTag.classList.add("fas");
        iTag.classList.add("fa-info-circle");
        iTag.classList.add("vad-tooltip-icon");
        span.classList.add("vad-tooltip-text");
        span.textContent = tooltips[i];
        iTag.appendChild(span);
        div.appendChild(iTag);
        tempTextInput.type = "text";
        tempTextInput.id = "Text" + (i + 1);
        tempTextInput.placeholder = "Text" + " " +(i+1); 
        tempTextInput.required = true;
        tempTextInput.maxLength = "20";
        tempTextInput.classList.add("vad_text_input");
        divText.appendChild( tempTextInput );
        divText.appendChild( div );
        getTxt.appendChild( divText );
        // getTxt.appendChild( tempTextInput );
        // mainDiv.appendChild(divText);
    }
    for ( var i = 0; i < textInputLength; i++ ){     
       
        document.getElementById( "Text" + (i + 1) ).addEventListener("focusout", validateText);
        document.getElementById( "Text" + (i + 1) ).addEventListener("propertychange", validateText);
        
    }

    TEMPLATE_NAME = templateName;
    inputs.template_name = templateName;
    console.log(inputs.template_name);
}

const createTemplatesDiv = () => {
    
    var templatesDiv = document.getElementById("template_container");
    
    for ( var i = 0; i < 20; i++ ){
        var textDiv = document.createElement("div");
        var imgInputDiv = document.createElement("div");
        var text = document.createElement("h3");
        text.textContent="Template "+ (i + 1);
        text.style.fontFamily = 'Muli-Black';
        textDiv.appendChild(text);
        var tempDiv = document.createElement("div");
        var tempInput = document.createElement("input");
        tempInput.type = "radio";
        tempInput.name = "template";
        const ppd = "template" + (i + 1);
        tempInput.value = ppd;
        var tempImage = document.createElement("img");
        tempImage.src = "http://localhost:8080/static/template" + ( i + 1 ) + ".png";
        tempImage.onclick = checkTrue;

        tempDiv.classList.add("template_single");
        tempDiv.id = "template_div_single"
        imgInputDiv.appendChild( tempInput );
        imgInputDiv.appendChild( tempImage );
        imgInputDiv.classList.add("imgInput")

        tempDiv.appendChild( imgInputDiv );
        tempDiv.appendChild(textDiv);
        
        templatesDiv.appendChild(tempDiv);
    }
}

document.getElementById("plan").addEventListener("change",()=>{
    inputs.template_music = document.getElementById("plan").value;
    document.getElementById("templateMusic").src="http://localhost:8080/static/" + document.getElementById("plan").value;
    console.log(">>>", inputs.template_music)
})



document.getElementById("fileInput").addEventListener("change", size_type);
document.getElementById("fileLogo").addEventListener("change", logo_size_type);
window.onload = createTemplatesDiv;


const finalInputs = () => {

    inputs.template_music = document.getElementById("plan").value;
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
            const btn=document.querySelector('#btn_next');
            btn.disabled=true;
            btn.textContent = "Generating..."
            
            
            console.log(inputs);
            console.log("navigate now!!")
            const fileObj = inputs.input_file;
            const logoObj = inputs.logo_file;
            var data = new FormData()
            data.append('input_file', logoObj);
            data.append('input_file', fileObj);
            data.append('inputs', JSON.stringify(inputs));
            console.log("This is data being sent >>>" , data);

            
            fetch( "http://localhost:8080/upload", {
                method: 'POST',
                body: data
            })
            .then( res => res.json() )
            .then( res => {
                if( res.status == "success" ){

                    window.location.href = `http://localhost:8080/navigate/navigate.html?src=${res.fileName}&data=${JSON.stringify(inputs)}&inputFile=${res.file_video}&logoFile=${res.file_logo}`;

                };
            })
            btn.style.backgroundColor = "rgb(26, 24, 24)";
            btn.style.color = "#29f2e4";

        }        
    }
    
}
           