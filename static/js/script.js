const uploading2 = document.getElementById("uploading2");
const error2 = document.getElementById("error2");
const uploaded2 = document.getElementById("uploaded2");

const Loading1 = document.getElementById("Loading1");
const Loading2 = document.getElementById("Loading2");
const Loading3 = document.getElementById("Loading3");
const Loaded = document.getElementById("Loaded");

const gotLangModel = document.getElementById("gotLangModel");
const getLangModel = document.getElementById("getLangModel");

const gotAcoModel = document.getElementById("gotAcoModel");
const getAcoModel = document.getElementById("getAcoModel");
const scrollClass = document.getElementById("scrollClass");
const transcriptHere = document.getElementById("transcriptHere");
const speakerHere = document.getElementById("speakerHere");
const summaryHere = document.getElementById("summaryHere");
const summaryHere2 = document.getElementById("summaryHere2");
const summaryHere3 = document.getElementById("summaryHere3");
const summaryHere4 = document.getElementById("summaryHere4");
const summaryHere5 = document.getElementById("summaryHere5");
const keywordHere = document.getElementById("keywordHere");

const removeThis = document.getElementById('removeThis');
const progressMsg = document.getElementById("myP");
const tabsHere = document.getElementById("tabsHere");
const tabs = document.getElementById("tabs");
const videoHere = document.getElementById("videoHere");
const submitButton = document.getElementById("Upload");

var fileN;

var videoTime = 0;
var startTimes = [];
var endTimes = [];
var speakersList = [];

$(document).ready(() => {
    uploaded2.style.display = "none";
    error2.style.display = "none";
    uploading2.style.display = "none";
    videoHere.style.display = "none";
    gotAcoModel.style.display = "none";
    gotLangModel.style.display = "none";
    Loading1.style.display = "none";
    Loading2.style.display = "none";
    Loading3.style.display = "none";
    tabsHere.style.display = "block";

    videoHere.ontimeupdate = () => { myFunction() };

    getSTTModels('language', 'select-id1');
    getSTTModels('acoustic', 'select-id2');
});

const isEmpty = (el) => {
    return !$.trim(el.html())
};

const myFunction = () => {
    num = videoHere.currentTime;
    videoTime = num.toFixed(2);
    for (i = 0; i < startTimes.length; i++) {
        if (videoTime > startTimes[i] && videoTime < endTimes[i])
            console.log(speakersList[i]);
    }
};

Array.prototype.contains = (v) => {
    for (var i = 0; i < this.length; i++) {
        if (this[i] === v) return true;
    }
    return false;
};

Array.prototype.unique = () => {
    var arr = [];
    for (var i = 0; i < this.length; i++) {
        if (!arr.contains(this[i])) {
            arr.push(this[i]);
        }
    }
    return arr;
};

const getSTTModels = async (model_type, select_id) => {
    let url = '';
    if (model_type == "acoustic")
        url = '/api/v1.0/transcribe/acoustic';
    else if (model_type == "language")
        url = '/api/v1.0/transcribe/language';

    await fetch(url, {timeout:false}).then(async (response) => {
        data = await response.json();

        var dynamicSelect = document.getElementById(select_id);

        data.customizations.forEach(element => {

            var newOption = document.createElement("option");
            newOption.text = element.name.toString(); 
            newOption.value = element.customization_id.toString(); 

            dynamicSelect.add(newOption);
        });

        if (model_type == "acoustic") {
            getAcoModel.style.display = "none";
            gotAcoModel.style.display = "block";
        }
        else if (model_type == "language") {
            getLangModel.style.display = "none";
            gotLangModel.style.display = "block";
        }
    });
};
var toChunk = false;

submitButton.onclick = () => {
    // tabs.style.display = "block";
    Loading1.style.display = "block";
    Loading2.style.display = "block";
    Loading3.style.display = "block";
    uploaded2.style.display = "none";
    uploading2.style.display = "block";

    if (isEmpty($('#myFiles'))) {
        uploading2.style.display = "none";
        error2.style.display = "block";
    } else {

        var file = $('.bx--file-filename').html();

        progressMsg.style.color = 'green';
        progressMsg.innerHTML = "uploading " + file + "...";

        let SttModel = {
            file: file,
            langModel: document.getElementById("select-id1").value,
            acoModel: document.getElementById("select-id2").value
        };

        if (document.getElementById("chunk").checked) toChunk = true;
        else toChunk = false;

        formData = new FormData($('form')[0]);
        formData.append("SttModel", JSON.stringify(SttModel));
        formData.append("toChunk", toChunk);

        error2.style.display = "none";

        $.ajax({
            url: '/api/v1.0/uploadVideo',
            type: 'POST',
            data: formData,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            timeout: false,
            success: (response) => {
                data = response;
                if (data.flag == 1) {
                    progressMsg.className = "w3-text-green w3-animate-opacity";
                    progressMsg.innerHTML = "Successfully Uploaded.";
                    if (file.split('.')[1] === 'mp4' || file.split('.')[1] === 'mov')
                        videoPlayer = `<source src="static/videos/${file.split('.')[0].replace(
                            / /g, "-").replace(/'/g, "").toLowerCase()}.${file.split('.')[1]}" type="video/${file.split('.')[1]}">Your browser does not support HTML video.`;
                    else {
                        videoPlayer = `<source src="static/videos/${file.split('.')[0].replace(
                            / /g, "-").replace(/'/g, "").toLowerCase()}.${file.split('.')[1]}" type="audio/${file.split('.')[1]}">Your browser does not support HTML audio.`;
                    }                            
                    videoHere.innerHTML = videoPlayer;
                    videoHere.style.display = "block";

                    uploading2.style.display = "none";
                    uploaded2.style.display = "block";
                    Convert(data.filename);
                } else if (data.flag == 0) {
                    uploading2.style.display = "none";
                    error2.style.display = "block";
                }
            },
            error: () => {
                error2.style.display = "block";
            }
        });
    }

};

const Convert = async (filename) => {
    progressMsg.className = "w3-text-green w3-animate-opacity";
    progressMsg.innerHTML = "Extracting Audio from Video...";
    
    let SttModel = {
        langModel: document.getElementById("select-id1").value,
        acoModel: document.getElementById("select-id2").value
    };
    
    let url = `/api/v1.0/uploadVideo?filename=${filename}&extract=True`;
    console.log(filename);
    await fetch(url, {timeout:false}).then(async (response) => {
        data = await response.json();
        if (data.flag == 1) {
            progressMsg.style.color = 'green';
            progressMsg.innerHTML = "Successfully extracted.";
            console.log("Successfully extracted");
            if (toChunk) Chunk(data.filename, SttModel);
            else SpeechToText(data.filename, SttModel);
        } else if (data.flag == 0) {
            console.log("Failed to extract");
            progressMsg.style.color = 'red';
            progressMsg.innerHTML = "Failed to extract";
            Loading1.style.display = "none";
            Loading3.style.display = "none";
            Loading2.style.display = "none";
        }
    });
};

const Chunk = async (filename, SttModel) => {
    progressMsg.className = "w3-text-green w3-animate-opacity";
    progressMsg.innerHTML = "Processing the audio...";
    
    let url = `/api/v1.0/uploadVideo?filename=${filename}&chunk=True`;
    console.log(filename);
    await fetch(url,{timeout:false}).then(async (response) => {
        data = await response.json();
        if (data.flag == 1) {
            progressMsg.className = "w3-text-green w3-animate-opacity";
            progressMsg.innerHTML = `Found ${data.pauses} long pauses in the video.`;
            
            const ids = [];
            for (let i = 0; i <= data.pauses; i++) { 
                ids.push(i);
            }   
            let trans = [];
            let spearkers = [];
            
            for(const id of ids){
                let percentage = parseInt(id/ids.length * 100);    
                setTimeout(()=>{
                    progressMsg.style.color = 'green';
                    progressMsg.innerHTML = `Transcribing...`;    
                },3000);
                progressMsg.style.color = 'blue';
                progressMsg.innerHTML = `${percentage}% completed...`;
                const data = await fetch(`/api/v1.0/transcribe/stt?filename=chunk${id}.wav&toChunk=True&langModelId=${SttModel.langModel}&acoModelId=${SttModel.acoModel}`, {timeout:false});
                const json = await data.json();
                
                speakerHere.innerHTML += json.speaker;
                transcriptHere.innerHTML += json.transcript;
                
                spearkers.push(json.speaker);
                trans.push(json.transcript);

               
            }

            Loading1.style.display = "none";
            Loading3.style.display = "none";
            summarize();
        } else if (data.flag == 0) {
            console.log("Failed to optimize");
            progressMsg.style.color = 'red';
            progressMsg.innerHTML = "Failed to optimize";
            Loading2.style.display = "none";
            Loading1.style.display = "none";
            Loading3.style.display = "none";
        }
    });
};

const SpeechToText = async (filename, SttModel) => {
    filename = filename.split('.')[0];
    progressMsg.className = "w3-text-green w3-animate-opacity";
    progressMsg.innerHTML = "Transcribing audio...";
    
    let trans = [];
    let spearkers = [];

    const data = await fetch(`/api/v1.0/transcribe/stt?filename=${filename}.wav&toChunk=False&langModelId=${SttModel.langModel}&acoModelId=${SttModel.acoModel}`, {timeout:false});
    const json = await data.json();
    
    
    speakerHere.innerHTML += json.speaker;
    transcriptHere.innerHTML += json.transcript;
    
    spearkers.push(json.speaker);
    trans.push(json.transcript);

    Loading1.style.display = "none";
    Loading3.style.display = "none";
    summarize();
};

const summarize = async () => {
    progressMsg.className = "w3-text-green w3-animate-opacity";
    progressMsg.innerHTML = "Summarizing...";
    
    let text = transcriptHere.innerHTML;
    text = text.replace("<br>", "");
    console.log(text);
    let summary = "";
    let keywords = [];
    let options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            text: text
        }),
        timeout: false
    };
    // post text data to the server
    const data = await fetch('/api/v1.0/summarize', options);
    const json = await data.json();
    
    summary = json.gensimsSummary;
    keywords = json.gensimKeywords;

    summaryHere.innerHTML = summary;
    keywordHere.innerHTML = ",".concat(keywords.join(", "));

    for (let i = 0; i < keywords.length; i++) {
        let keyword_ = keywords[i].replace(/ /g, "-").replace(/'/g, "").toLowerCase();
        let keyword_regex = new RegExp(keyword_, 'g');
        console.log(keyword_regex+" will be replaced with "+keywords[i]);
        if (keyword_regex != "") summaryHere.innerHTML = summaryHere.innerHTML.replace(keyword_regex, `<button class="bx--tag bx--tag--cyan"><span class="bx--tag__label">${keywords[i]}</span></button>`);
    } 

    summaryHere2.innerHTML = json.gpt2Summary;
    summaryHere3.innerHTML = json.xlnetSummary;
    summaryHere4.innerHTML = "".concat(json.bertKeywords.join("<br>"));
    summaryHere5.innerHTML = "".concat(json.additionalKeywords.join("<br>"));
    Loading2.style.display = "none";
    Loaded.style.display = "block";
    progressMsg.className = "w3-text-green w3-animate-opacity";
    progressMsg.innerHTML = `Successfully Summarized!`;
};