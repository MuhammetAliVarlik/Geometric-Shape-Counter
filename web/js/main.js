/*----------------------------------------------------------------------------------------------------------------*/
let globalResult;
function changeImage(event)
{
  // read file 
  var file = event.target.files[0];
  var imgInput = document.getElementById("inputImage");
  var imgOutput = document.getElementById("outputImage");
  var imgGray = document.getElementById("grayImage");
  var imgThresh = document.getElementById("thresholdImage");
  disableInputs();
  if (file)
  {
    var reader = new FileReader();
  reader.onload = function(e)
  {
    imgInput.src = e.target.result;
    globalResult = e.target.result;
    eel.initializeImage(
      e.target.result,
      document.getElementById("epsilon").value,
      document.getElementById("threshold").value,
      document.getElementById("checkBoxSettingsClosed").checked,
      document.getElementById("checkBoxSettingsText").checked,
      document.getElementById("checkBoxSettingsFill").checked,
      document.getElementById("checkBoxSettingsLog").checked,
      )
      (
        function(response)
        {
          if (response!="error"){
          [out,count,thresh,gray]=response; 
          imgOutput.src = out; 
          imgGray.src = gray; 
          imgThresh.src = thresh;  
          document.getElementById("triangle").innerHTML=count["triangle"];
          document.getElementById("rectangle").innerHTML=count["rectangle"];
          document.getElementById("pentagon").innerHTML=count["pentagon"];
          document.getElementById("hexagon").innerHTML=count["hexagon"];
          document.getElementById("circle").innerHTML=count["circle"];
          document.getElementById("logIframeObject").data="../output_log.txt";
          enableInputs();
      
          for(let i=3; i<8;i++)
          {
            let id_text;
            let id_colorPickerFill;
            let id_FontScale;
            let id_colorPickerText;
            let id_Thickness;
            let id_checkBoxFill;
            let id_checkBoxText;
            switch(i) 
            {
              case 3:
                id_text="t_text";
                id_colorPickerFill="t_colorPickerFill";
                id_FontScale="t_FontScale";
                id_colorPickerText="t_colorPickerText";
                id_Thickness="t_Thickness";
                id_checkBoxFill="t_checkBoxFill";
                id_checkBoxText="t_checkBoxText";
                break;
              case 4:
                id_text="r_text";
                id_colorPickerFill="r_colorPickerFill";
                id_FontScale="r_FontScale";
                id_colorPickerText="r_colorPickerText";
                id_Thickness="r_Thickness";
                id_checkBoxFill="r_checkBoxFill";
                id_checkBoxText="r_checkBoxText";
                break;
              case 5:
                id_text="p_text";
                id_colorPickerFill="p_colorPickerFill";
                id_FontScale="p_FontScale";
                id_colorPickerText="p_colorPickerText";
                id_Thickness="p_Thickness";
                id_checkBoxFill="p_checkBoxFill";
                id_checkBoxText="p_checkBoxText";
                break;
              case 6:
                id_text="h_text";
                id_colorPickerFill="h_colorPickerFill";
                id_FontScale="h_FontScale";
                id_colorPickerText="h_colorPickerText";
                id_Thickness="h_Thickness";
                id_checkBoxFill="h_checkBoxFill";
                id_checkBoxText="h_checkBoxText";
                break;
              case 7:
                id_text="c_text";
                id_colorPickerFill="c_colorPickerFill";
                id_FontScale="c_FontScale";
                id_colorPickerText="c_colorPickerText";
                id_Thickness="c_Thickness";
                id_checkBoxFill="c_checkBoxFill";
                id_checkBoxText="c_checkBoxText";
                break;
            }
            getDefaultsFromJSON(String(i), "text", function(response) {
              if (response!="error"){
                document.getElementById(id_text).value = response;
              }
              else{
                errorCallback()
              }
            });
            getDefaultsFromJSON(String(i), "color", function(response) {
              if (response!="error"){
                    document.getElementById(id_colorPickerFill).value = response;
              }
              else{
                errorCallback()
              }
            });
            getDefaultsFromJSON(String(i), "fontScale", function(response) {
              if(response!="error"){
                    document.getElementById(id_FontScale).value = response;
              }
                    else{
                      errorCallback()
                    }        
            });
            getDefaultsFromJSON(String(i), "fontColor", function(response) {
                  if(response!="error"){
                    document.getElementById(id_colorPickerText).value = response;
                    }
                    else{
                      errorCallback()
                    }
            });
            getDefaultsFromJSON(String(i), "thickness", function(response) {
                    if(response!="error"){
                    document.getElementById(id_Thickness).value = response;
                    }
                    else{
                      errorCallback()
                    }
            });
            getDefaultsFromJSON(String(i), "fillChoice", function(response) {
              if(response!="error"){
                if(response==1)
                {
                  document.getElementById(id_checkBoxFill).checked = true;
                }
                else
                {
                  document.getElementById(id_checkBoxFill).checked = false;
                }
              }
              else{
                errorCallback()
              }
            });
            getDefaultsFromJSON(String(i), "textChoice", function(response) {
              if(response!="error"){
              if(response==1){
                document.getElementById(id_checkBoxText).checked = true;
              }
              else{
                document.getElementById(id_checkBoxText).checked = false;
              }  
            }
            else{
              errorCallback()
            }
            });
          };
        }
        else{
          errorCallback()
        }
      }
      )
    }
    reader.readAsDataURL(file);
  }
  document.getElementById("chooseFile").value = "";
}
/*----------------------------------------------------------------------------------------------------------------*/
function changeOnImage()
{
  eel.initializeImage(
    globalResult,
    document.getElementById("epsilon").value,
    document.getElementById("threshold").value,
    document.getElementById("checkBoxSettingsClosed").checked,
    document.getElementById("checkBoxSettingsText").checked,
    document.getElementById("checkBoxSettingsFill").checked,
    document.getElementById("checkBoxSettingsLog").checked,
    )
    (function(response)
    { 
      if(response!="error"){
      var imgOutput = document.getElementById("outputImage");
      var imgGray = document.getElementById("grayImage");
      var imgThresh = document.getElementById("thresholdImage");
      [out,count,thresh,gray]=response; 
      imgOutput.src = out; 
      imgGray.src = gray; 
      imgThresh.src = thresh;   
      document.getElementById("triangle").innerHTML=count["triangle"];
      document.getElementById("rectangle").innerHTML=count["rectangle"];
      document.getElementById("pentagon").innerHTML=count["pentagon"];
      document.getElementById("hexagon").innerHTML=count["hexagon"];
      document.getElementById("circle").innerHTML=count["circle"];
    }
    else{
      errorCallback()
    }
  }
  );
}
/*----------------------------------------------------------------------------------------------------------------*/
function getDefaultsFromJSON(key, property_name, callback) {

  eel.getDefaults(key, property_name)(function(response) {
    callback(response);
  });

}
/*----------------------------------------------------------------------------------------------------------------*/
function updateDefaultsFromJSON(key, property_name,tag, callback) {
  point=parseInt(key);
  let id_text;
  let id_colorPickerFill;
  let id_FontScale;
  let id_colorPickerText;
  let id_Thickness;
  let id_checkBoxFill;
  let id_checkBoxText;
  switch(point)
  {
    case 3:
      id_text="t_text";
      id_colorPickerFill="t_colorPickerFill";
      id_FontScale="t_FontScale";
      id_colorPickerText="t_colorPickerText";
      id_Thickness="t_Thickness";
      id_checkBoxFill="t_checkBoxFill";
      id_checkBoxText="t_checkBoxText";
      break;
    case 4:
      id_text="r_text";
      id_colorPickerFill="r_colorPickerFill";
      id_FontScale="r_FontScale";
      id_colorPickerText="r_colorPickerText";
      id_Thickness="r_Thickness";
      id_checkBoxFill="r_checkBoxFill";
      id_checkBoxText="r_checkBoxText";
      break;
    case 5:
      id_text="p_text";
      id_colorPickerFill="p_colorPickerFill";
      id_FontScale="p_FontScale";
      id_colorPickerText="p_colorPickerText";
      id_Thickness="p_Thickness";
      id_checkBoxFill="p_checkBoxFill";
      id_checkBoxText="p_checkBoxText";
      break;
    case 6:
      id_text="h_text";
      id_colorPickerFill="h_colorPickerFill";
      id_FontScale="h_FontScale";
      id_colorPickerText="h_colorPickerText";
      id_Thickness="h_Thickness";
      id_checkBoxFill="h_checkBoxFill";
      id_checkBoxText="h_checkBoxText";
      break;
    case 7:
      id_text="c_text";
      id_colorPickerFill="c_colorPickerFill";
      id_FontScale="c_FontScale";
      id_colorPickerText="c_colorPickerText";
      id_Thickness="c_Thickness";
      id_checkBoxFill="c_checkBoxFill";
      id_checkBoxText="c_checkBoxText";
      break;
  }
  let text=document.getElementById(id_text).value;
  let color=document.getElementById(id_colorPickerFill).value;
  let fontScale=document.getElementById(id_FontScale).value;
  let fontColor=document.getElementById(id_colorPickerText).value;
  let thickness=document.getElementById(id_Thickness).value;
  let fillChoice;
  let textChoice;
  
  if(document.getElementById(id_checkBoxFill).checked==true)
  {
    fillChoice=1;
  }
  else
  {
    fillChoice=0;
  };
  if(document.getElementById(id_checkBoxText).checked==true)
  {
    textChoice=1;
  }
  else{
    textChoice=0;
  };
  eel.updateDefaults(
    key,
    property_name,point, 
    color,
    text, 
    parseFloat(fontScale), 
    parseFloat(thickness), 
    fontColor,
    fillChoice,
    textChoice)(function(response) 
    {
      eel.initializeImage(
        globalResult,
        document.getElementById("epsilon").value,
        document.getElementById("threshold").value,
        document.getElementById("checkBoxSettingsClosed").checked,
        document.getElementById("checkBoxSettingsText").checked,
        document.getElementById("checkBoxSettingsFill").checked,
        document.getElementById("checkBoxSettingsLog").checked,
      )(function(response)
      { 
        if(response!="error"){
        var imgOutput = document.getElementById("outputImage");
        [out,count]=response; 
        imgOutput.src = out;  
        document.getElementById("triangle").innerHTML=count["triangle"];
        document.getElementById("rectangle").innerHTML=count["rectangle"];
        document.getElementById("pentagon").innerHTML=count["pentagon"];
        document.getElementById("hexagon").innerHTML=count["hexagon"];
        document.getElementById("circle").innerHTML=count["circle"];
        }else{
          errorCallback()
        }
      })
  });

}

/*----------------------------------------------------------------------------------------------------------------*/

let rangeEpsilon=document.getElementById("epsilonSlider");
let numberEpsilon=document.getElementById("epsilon")

rangeEpsilon.addEventListener("change",(e)=>
{
  numberEpsilon.value=e.target.value;
});

numberEpsilon.addEventListener("onkeyup",(e)=>
{
  rangeEpsilon.value=e.target.value;
});

/*----------------------------------------------------------------------------------------------------------------*/
let rangeThreshold=document.getElementById("thresholdSlider");
let numberThreshold=document.getElementById("threshold")

rangeThreshold.addEventListener("change",(e)=>
{
  numberThreshold.value=e.target.value;
});
numberThreshold.addEventListener("onkeyup",(e)=>
{
  rangeThreshold.value=e.target.value;
});
/*----------------------------------------------------------------------------------------------------------------*/
function controlLogPanel()
{
  status=document.getElementById("checkBoxSettingsLog").checked;
if(status=="true")
{
  document.getElementById("log").style.display="block";
}
else
{
  document.getElementById("log").style.display="none";
}
}
/*----------------------------------------------------------------------------------------------------------------*/
let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
showSlides(slideIndex += n);
}

function currentSlide(n) {
showSlides(slideIndex = n);
}

function showSlides(n) {
let i;
let slides = document.getElementsByClassName("mySlides");
let dots = document.getElementsByClassName("dot");
if (n > slides.length) {slideIndex = 1}    
if (n < 1) {slideIndex = slides.length}
for (i = 0; i < slides.length; i++) {
slides[i].style.display = "none";  
}
for (i = 0; i < dots.length; i++) {
dots[i].className = dots[i].className.replace(" active", "");
}
slides[slideIndex-1].style.display = "block";  
dots[slideIndex-1].className += " active";
}
/*----------------------------------------------------------------------------------------------------------------*/
function disableInputs(){
document.getElementById("t_text").disabled=true;
document.getElementById("t_colorPickerFill").disabled=true;
document.getElementById("t_FontScale").disabled=true;
document.getElementById("t_colorPickerText").disabled=true;
document.getElementById("t_Thickness").disabled=true;
document.getElementById("t_checkBoxFill").disabled=true;
document.getElementById("t_checkBoxText").disabled=true;

document.getElementById("r_text").disabled=true;
document.getElementById("r_colorPickerFill").disabled=true;
document.getElementById("r_FontScale").disabled=true;
document.getElementById("r_colorPickerText").disabled=true;
document.getElementById("r_Thickness").disabled=true;
document.getElementById("r_checkBoxFill").disabled=true;
document.getElementById("r_checkBoxText").disabled=true;

document.getElementById("p_text").disabled=true;
document.getElementById("p_colorPickerFill").disabled=true;
document.getElementById("p_FontScale").disabled=true;
document.getElementById("p_colorPickerText").disabled=true;
document.getElementById("p_Thickness").disabled=true;
document.getElementById("p_checkBoxFill").disabled=true;
document.getElementById("p_checkBoxText").disabled=true;

document.getElementById("h_text").disabled=true;
document.getElementById("h_colorPickerFill").disabled=true;
document.getElementById("h_FontScale").disabled=true;
document.getElementById("h_colorPickerText").disabled=true;
document.getElementById("h_Thickness").disabled=true;
document.getElementById("h_checkBoxFill").disabled=true;
document.getElementById("h_checkBoxText").disabled=true;

document.getElementById("c_text").disabled=true;
document.getElementById("c_colorPickerFill").disabled=true;
document.getElementById("c_FontScale").disabled=true;
document.getElementById("c_colorPickerText").disabled=true;
document.getElementById("c_Thickness").disabled=true;
document.getElementById("c_checkBoxFill").disabled=true;
document.getElementById("c_checkBoxText").disabled=true;


document.getElementById("epsilonSlider").disabled=true;
document.getElementById("epsilon").disabled=true;
document.getElementById("thresholdSlider").disabled=true;
document.getElementById("threshold").disabled=true;

document.getElementById("checkBoxSettingsClosed").disabled=true;
document.getElementById("checkBoxSettingsText").disabled=true;
document.getElementById("checkBoxSettingsFill").disabled=true;
document.getElementById("checkBoxSettingsLog").disabled=true;

}
/*----------------------------------------------------------------------------------------------------------------*/
function enableInputs(){
document.getElementById("t_text").disabled=false;
document.getElementById("t_colorPickerFill").disabled=false;
document.getElementById("t_FontScale").disabled=false;
document.getElementById("t_colorPickerText").disabled=false;
document.getElementById("t_Thickness").disabled=false;
document.getElementById("t_checkBoxFill").disabled=false;
document.getElementById("t_checkBoxText").disabled=false;

document.getElementById("r_text").disabled=false;
document.getElementById("r_colorPickerFill").disabled=false;
document.getElementById("r_FontScale").disabled=false;
document.getElementById("r_colorPickerText").disabled=false;
document.getElementById("r_Thickness").disabled=false;
document.getElementById("r_checkBoxFill").disabled=false;
document.getElementById("r_checkBoxText").disabled=false;

document.getElementById("p_text").disabled=false;
document.getElementById("p_colorPickerFill").disabled=false;
document.getElementById("p_FontScale").disabled=false;
document.getElementById("p_colorPickerText").disabled=false;
document.getElementById("p_Thickness").disabled=false;
document.getElementById("p_checkBoxFill").disabled=false;
document.getElementById("p_checkBoxText").disabled=false;

document.getElementById("h_text").disabled=false;
document.getElementById("h_colorPickerFill").disabled=false;
document.getElementById("h_FontScale").disabled=false;
document.getElementById("h_colorPickerText").disabled=false;
document.getElementById("h_Thickness").disabled=false;
document.getElementById("h_checkBoxFill").disabled=false;
document.getElementById("h_checkBoxText").disabled=false;

document.getElementById("c_text").disabled=false;
document.getElementById("c_colorPickerFill").disabled=false;
document.getElementById("c_FontScale").disabled=false;
document.getElementById("c_colorPickerText").disabled=false;
document.getElementById("c_Thickness").disabled=false;
document.getElementById("c_checkBoxFill").disabled=false;
document.getElementById("c_checkBoxText").disabled=false;


document.getElementById("epsilonSlider").disabled=false;
document.getElementById("epsilon").disabled=false;
document.getElementById("thresholdSlider").disabled=false;
document.getElementById("threshold").disabled=false;

document.getElementById("checkBoxSettingsClosed").disabled=false;
document.getElementById("checkBoxSettingsText").disabled=false;
document.getElementById("checkBoxSettingsFill").disabled=false;
document.getElementById("checkBoxSettingsLog").disabled=false;

}
/*----------------------------------------------------------------------------------------------------------------*/
function refreshPage(){
location.reload();
}
/*----------------------------------------------------------------------------------------------------------------*/
function saveImage() {
// Get the image element by its ID
var image = document.getElementById('outputImage');

// Create a canvas element to draw the image
var canvas = document.createElement('canvas');
canvas.width = image.width;
canvas.height = image.height;

var ctx = canvas.getContext('2d');

// Draw the image onto the canvas
ctx.drawImage(image, 0, 0);

// Convert the canvas content to a data URL
// This will be used as the href for the download link
var dataURL = canvas.toDataURL('image/jpeg'); // Or 'image/png' for PNG images

// Create a download link
var downloadLink = document.createElement('a');
downloadLink.href = dataURL;
downloadLink.download = 'image.jpg'; // Specify the file name here

// Trigger the download
downloadLink.click();
}

/*----------------------------------------------------------------------------------------------------------------*/
const slideShowArea = document.getElementById('slideShow');
const coordinates = document.getElementById('text');

slideShowArea.addEventListener('mousemove', function(event) {
const x = event.clientX - slideShowArea.offsetLeft;
const y = event.clientY - slideShowArea.offsetTop;
coordinates.textContent = `X: ${x}, Y: ${y}`;
});

function errorCallback() {
  alert("An error occurred");
  location.reload();

}
