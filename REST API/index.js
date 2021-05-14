const express = require('express');
const multer = require('multer');
const {spawn} = require('child_process');
const app = express();
const {PythonShell} = require('python-shell');
const port = 3000;

const path = require('path');
var newFilename;
app.use(express.json());

app.use('/static', express.static('templateImages'))
app.use('/static', express.static('templateMusic'))

app.use((req, res, next) => {
    res.header("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT");
    res.header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, access-control-allow-origin,Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers");
    res.header("Access-Control-Allow-Origin", "*");
    next();
});


const checkTemplateName = ( template_name ) => {
    switch ( template_name ){
        case "template1":
            return "Template_1.webM";
        case "template2":
            return "Template_2.webM";
        case "template3":
            return "Template_3.webM";
        case "template4":
            return "Template_4.webM";
        case "template5":
            return "Template_5.webM";
        case "template6":
            return "Template_6.webM";
        case "template7":
            return "Template_7.webM";
        case "template8":
            return "Template_8.webM";
        case "template9":
            return "Template_9.webM";
        case "template10":
            return "Template_10.webM";
        case "template11":
            return "Template_11.webM";
        case "template12":
            return "Template_12.webM";
        case "template13":
            return "Template_13.webM";
        case "template14":
            return "Template_14.webM";
        case "template15":
            return "Template_15.webM";
        case "template16":
            return "Template_16.webM";
        case "template17":
            return "Template_17.webM";
        case "template18":
            return "Template_18.webM";
        case "template19":
            return "Template_19.webM";
        case "template20":
            return "Template_20.webM";
    }
}
const store = multer.diskStorage({
    destination: (req,file,cb)=>{
        cb(null,'./uploads');
    },
    filename: (req,file,cb)=>{
        newFilename = Date.now()+"--"+file.originalname
        cb(null,newFilename);
    }
});

const modifyTextInput=(arr)=>{
    var st="";
    for(i=0;i<arr.length;i++){
        st+="'"+arr[i]+"'"+",";
    }
    console.log(st);
    return st.slice(0,st.length-1);
}

const upload = multer({  storage: store  });

app.get('/getimage',(req,res)=>{
    res.sendFile(path.join(__dirname, "/uploads/1620348016104--sample-mp4-file.mp4"));
})

app.get('/',(req,res)=>{
    res.sendFile(path.join(__dirname, "index.html"));
})


app.post('/upload', upload.single('input_file') ,(req, res) => {
    req.setTimeout(0);
    console.log("done");
    // running python script
    console.log(newFilename);
    // sleep(5000);
    const data = req.body;
    const temp = JSON.parse( data["inputs"] );
    const uploadedFile = 'uploads/' + newFilename;
    const templateName = checkTemplateName( temp.template_name );
    const templateMusic = 'templateMusic/' + temp.template_music;
    const textInputs = modifyTextInput( temp.text_inputs ); 
    const fontColor = temp.font_color;
    const fontStyle = temp.font_style;
    const fontFade = temp.font_fade;
    const fontSize = temp.font_size;
    // newFilename = Date.now()+"--"+file.originalname
    console.log( templateName, templateMusic, textInputs, fontColor, fontStyle, fontFade );

    console.log(temp);
    // console.log(JSON.parse(temp));
    // console.log(JSON.stringify(data["inputs"]));
    const outputFileName = Date.now()+"--ad"+'.mp4';
    var dataToSend;
    // // spawn new child process to call the python script
    const python = spawn('python', ['testMoviepy.py', templateName, textInputs, uploadedFile, templateMusic, `${ fontSize },${ fontColor },${ fontFade },${ fontStyle },${ outputFileName }`, 1]);
    // const python = spawn('python', ['--version'])
    // // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
        console.log("This is data >>> ", dataToSend);
    });
    // // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        if ( code == 0 ){
            res.json( {
                status : "success",
                fileName : outputFileName
                } );
        }
        else{
            res.json({
                status : "error"
            })
        }
    //     // send data to browser
        // res.json(dataToSend.slice(72, dataToSend.length - 72))
        // res.json(dataToSend)
    });

    // let options = {
    //     mode: 'text',
    //     pythonOptions: ['-u'], // get print results in real-time
    //        //If you are having python_test.py script in same folder, then it's optional.
    //     args: ["Template_16.webM", `"Text 1","Text 2","Text 3",Text 4","Text 5"`, "video1.mp4", "Motive.mp3", `50,green,fadeout,Arial`] //An argument which can be accessed in the script using sys.argv[1]
    // };

    // PythonShell.run('testMoviepy.py', options, function (err, result){
    //     if (err) throw err;
    //     // result is an array consisting of messages collected 
    //     //during execution of script.
    //     console.log('result: ', result.toString());
    //     res.send(result.toString())
    // });
})




app.listen(port, () => console.log(`Example app listening on port ${port}!`))