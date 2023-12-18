document.getElementById("inputImage").addEventListener("click", function(e) {
    e.preventDefault();
    document.getElementById("chooseFile").click();
  });
  let globalResult;
  function changeImage(event) {
    var file = event.target.files[0];
    var imgInput = document.getElementById("inputImage");
    var imgOutput = document.getElementById("outputImage");
  
    if (file) {
      var reader = new FileReader();
  
      reader.onload = function(e) {
        imgInput.src = e.target.result;
        globalResult = e.target.result;
        eel.initializeImage(e.target.result,
            document.getElementById("epsilon").value,
            document.getElementById("threshold").value,
            document.getElementById("checkBoxSettingsClosed").checked,
            document.getElementById("checkBoxSettingsText").checked,
            document.getElementById("checkBoxSettingsFill").checked,
            document.getElementById("checkBoxSettingsLog").checked,
            )(function(response){  
            [out,count]=response; 
            imgOutput.src = out;  
            document.getElementById("triangle").innerHTML=count["triangle"];
            document.getElementById("rectangle").innerHTML=count["rectangle"];
            document.getElementById("pentagon").innerHTML=count["pentagon"];
            document.getElementById("hexagon").innerHTML=count["hexagon"];
            document.getElementById("circle").innerHTML=count["circle"];
            
            for(let i=3; i<8;i++){
              let id_text;
              let id_colorPickerFill;
              let id_FontScale;
              let id_colorPickerText;
              let id_Thickness;
              let id_checkBoxFill;
              let id_checkBoxText;
              switch(i) {
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
                        document.getElementById(id_text).value = response;
                    });
                getDefaultsFromJSON(String(i), "color", function(response) {
                        document.getElementById(id_colorPickerFill).value = response;
                    });
                getDefaultsFromJSON(String(i), "fontScale", function(response) {
                        document.getElementById(id_FontScale).value = response;
                    });
                getDefaultsFromJSON(String(i), "fontColor", function(response) {
                        document.getElementById(id_colorPickerText).value = response;
                    });
                getDefaultsFromJSON(String(i), "thickness", function(response) {
                        document.getElementById(id_Thickness).value = response;
                    });
                getDefaultsFromJSON(String(i), "fillChoice", function(response) {
                  if(response==1){
                    document.getElementById(id_checkBoxFill).checked = true;
                  }
                  else{
                    document.getElementById(id_checkBoxFill).checked = false;
                  }
                    });
                getDefaultsFromJSON(String(i), "textChoice", function(response) {
                  if(response==1){
                    document.getElementById(id_checkBoxText).checked = true;
                  }
                  else{
                    document.getElementById(id_checkBoxText).checked = false;
                  }
                        
                    });

            }


              })
      }
  
      reader.readAsDataURL(file);
    }
    // Dosyayı seçtikten sonra inputu temizleyelim
    document.getElementById("chooseFile").value = "";
  }
  
  function changeOnImage(){
    eel.initializeImage(globalResult,
        document.getElementById("epsilon").value,
        document.getElementById("threshold").value,
        document.getElementById("checkBoxSettingsClosed").checked,
        document.getElementById("checkBoxSettingsText").checked,
        document.getElementById("checkBoxSettingsFill").checked,
        document.getElementById("checkBoxSettingsLog").checked,
        )(function(response){ 
        var imgOutput = document.getElementById("outputImage");
        [out,count]=response; 
        imgOutput.src = out;  
        document.getElementById("triangle").innerHTML=count["triangle"];
        document.getElementById("rectangle").innerHTML=count["rectangle"];
        document.getElementById("pentagon").innerHTML=count["pentagon"];
        document.getElementById("hexagon").innerHTML=count["hexagon"];
        document.getElementById("circle").innerHTML=count["circle"];
          })
  }

function getDefaultsFromJSON(key, property_name, callback) {
    eel.getDefaults(key, property_name)(function(response) {
        callback(response);
    });
}
function updateDefaultsFromJSON(key, property_name,tag, callback) {
  point=parseInt(key);
  let id_text;
  let id_colorPickerFill;
  let id_FontScale;
  let id_colorPickerText;
  let id_Thickness;
  let id_checkBoxFill;
  let id_checkBoxText;
  switch(point) {
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
            if(document.getElementById(id_checkBoxFill).checked==true){
              fillChoice=1;
            }
            else{
              fillChoice=0;
            };
            if(document.getElementById(id_checkBoxText).checked==true){
              textChoice=1;
            }
            else{
              textChoice=0;
            };
    eel.updateDefaults(key,property_name,point, color, text, parseFloat(fontScale), parseFloat(thickness), fontColor,fillChoice,textChoice)(function(response) {
        eel.initializeImage(globalResult,
        document.getElementById("epsilon").value,
        document.getElementById("threshold").value,
        document.getElementById("checkBoxSettingsClosed").checked,
        document.getElementById("checkBoxSettingsText").checked,
        document.getElementById("checkBoxSettingsFill").checked,
        document.getElementById("checkBoxSettingsLog").checked,
        )(function(response){ 
        var imgOutput = document.getElementById("outputImage");
        [out,count]=response; 
        imgOutput.src = out;  
        document.getElementById("triangle").innerHTML=count["triangle"];
        document.getElementById("rectangle").innerHTML=count["rectangle"];
        document.getElementById("pentagon").innerHTML=count["pentagon"];
        document.getElementById("hexagon").innerHTML=count["hexagon"];
        document.getElementById("circle").innerHTML=count["circle"];
          })
    });
}

let rangeEpsilon=document.getElementById("epsilonSlider");
let numberEpsilon=document.getElementById("epsilon")
rangeEpsilon.addEventListener("change",(e)=>{
  numberEpsilon.value=e.target.value;
})
numberEpsilon.addEventListener("onkeyup",(e)=>{
  rangeEpsilon.value=e.target.value;
})

let rangeThreshold=document.getElementById("thresholdSlider");
let numberThreshold=document.getElementById("threshold")
rangeThreshold.addEventListener("change",(e)=>{
  numberThreshold.value=e.target.value;
})
numberThreshold.addEventListener("onkeyup",(e)=>{
  rangeThreshold.value=e.target.value;
})