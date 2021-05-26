
const arr=[];
const data=location.search;
const urlParams = new URLSearchParams(data);
for (const [key, value] of urlParams) {
    console.log(`${key}:${value}`);
    const obj = {}
    obj[key] = value;
    arr.push(obj)
}
var temp = JSON.parse(arr[1].data);
var vidFilename = arr[2].inputFile;
var logoFilename = arr[3].logoFile;
console.log("ISKO DEKHO >>>", temp);
// console.log("this is data sent >>>", file);

window.onload = document.getElementById("preview-src").src = "http://localhost:8080/static/"+arr[0].src


const upload = async () => {
    var data = new FormData()
    data.append('inputs', JSON.stringify(temp));
    console.log(data);
    const result = await fetch( "http://localhost:8080/upload", {
        method: 'POST',
        headers:{
            flag : "true",
            video: vidFilename,
            logo: logoFilename
        },
        body: data
    })
    .then( res => res.json() )
    .then( res => {
        if( res.status == "success" ){
            return res.fileName;
        };
    })
    return result
}

const insertLink = async () => {
    var finalDiv = document.getElementById("finalDiv");
    var vid = document.getElementById("videoGenerated");
    var h1Tag = document.createElement("h1");
    var h4Tag = document.createElement("h4");
    var span = document.createElement("span");
    h1Tag.innerHTML = "Your video is being generated";
    h4Tag.innerHTML = "Please wait for 2-3 mins ...";
    vid.before( h1Tag );
    vid.before( h4Tag );

    var videoLink = document.createElement("a");
    var gifSpinner = document.createElement("img");
    gifSpinner.src = "http://localhost:8080/assets/loading.gif";
    gifSpinner.style.height = "100px";
    gifSpinner.style.width = "100px";
    // gifSpinner.style.marginLeft = "150px";
    vid.appendChild(gifSpinner);
    const link = async () => {
        const result = await upload()
        return result
    }
    (async () => {
        const videoName = await link();
        videoLink.setAttribute('href', "http://localhost:8080/static/" + videoName);
        videoLink.textContent = "here";
        videoLink.style.fontSize = "32px";
        videoLink.style.fontStyle = "bold";
        videoLink.style.display = "inline-block";
        videoLink.setAttribute('download', "download");
        finalDiv.innerHTML = "";
        vid.innerHTML = "";
        h1Tag.innerHTML = "Download your ad ";
        h1Tag.style.display = "inline-block";
        vid.style.whiteSpace = "nowrap";
        vid.style.overflowX = "hidden";
        span.textContent = " ";
        vid.appendChild(h1Tag);
        vid.appendChild(span);
        vid.appendChild(videoLink)
        finalDiv.appendChild(vid);
    })();
}

const stripe = Stripe('pk_test_51IuGGgHPVMu7FaWVTs3zB5xP5jQa1vSjifJMIsJ2LrjHhKQivQM1a0zuiOGlzumm23u6TBVZKrw7U1xO7LvOC4KP00FcfpRmxJ');
const elements = stripe.elements();

const cardElement = elements.create('card');
cardElement.mount('#card-element');

function initializePayment() {
    return fetch('/payments', { method: 'POST' })
        .then(res => res.text())
        .then(JSON.parse);
    }

async function confirmPayment(clientSecret) {
    const result = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
        card: cardElement,
        },
    });
    if (result.error) {
        console.error(result.error);
    } else {
        document.getElementById("card-element").innerHTML = "";
        var btn_pay = document.getElementById("pay-button");
        var parentNode = btn_pay.parentNode;
        parentNode.removeChild(btn_pay);
        insertLink();
    }
}

document.getElementById('pay-button')
.addEventListener('click', async () => {
    const { clientSecret } = await initializePayment();
    confirmPayment(clientSecret);
});
