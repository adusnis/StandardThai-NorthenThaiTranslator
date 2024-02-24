const myTextArea = document.getElementById('inputtextbox');
  myTextArea.focus();
  myTextArea.setSelectionRange(myTextArea.value.length, myTextArea.value.length);
const form = document.getElementById("autoSubmit");
const inputtextbox = document.getElementById("inputtextbox");
let inputtext = inputtextbox.value;
const outputtextbox = document.getElementById("outputtextbox");
let outputtext = outputtextbox.value;
var lang1 = document.getElementById("lang1");
var lang2 = document.getElementById("lang2");
var direction = document.getElementById("direction-input")
var n
if (lang1.innerHTML == "ไทยกลาง"){
  n = 0;
}
else if(lang1.innerHTML == "ไทยถิ่นเหนือ"){
  n = 1;
}
direction.value = n;

var searchList;
function toggleSearchList() {
  if (n % 2 === 0) {
    searchList = thTranList;
  } else if (n % 2 === 1) {
    searchList = wordList;
  }
}
toggleSearchList();

function switchLang() {
    n++;
    if (n % 2 == 0) {
      lang1.innerHTML = "ไทยกลาง";
      lang2.innerHTML = "ไทยถิ่นเหนือ";
    } else if (n % 2 == 1){
      lang1.innerHTML = "ไทยถิ่นเหนือ";
      lang2.innerHTML = "ไทยกลาง";
    }
    toggleSearchList();
    let temp = inputtextbox.value
    inputtextbox.innerHTML = outputtextbox.value
    outputtextbox.innerHTML = temp
    direction.value = n;
    inputtext = inputtextbox.value;
    if (inputtext){
      form.action=("/"+n+"/"+inputtext)
    }
    else{ 
      form.action=("/"+n)
    }
    form.submit()
  }

  function selectInput(event){
    const selectedWord = event.target.innerHTML;
    inputtextbox.value = selectedWord;
    inputtext = inputtextbox.value;
    if (inputtext){
      form.action=("/"+n+"/"+inputtext)
    }
    else{
      form.action=("/"+n)
    }
    form.submit()
  }
  function display(result){
    const limitedResult = result.slice(0, 3);
    const content = limitedResult.map((list)=>{
      return "<div class='result' onclick='selectInput(event)'>" + list + "</div>"
    });

    resultBox.innerHTML = "<div>" + content.join("") + "</div>";
  }
  const resultBox = document.querySelector(".result-box")
  inputtextbox.onkeyup = function(){
    let result = [];
    let input = inputtextbox.value;
    if(input.length){
      result = searchList.filter((word) => {
        return word.toLowerCase().startsWith(input.toLowerCase());
      });
      console.log(result)
    }
    display(result)
  }


  function autoSubmit() {
  let timer;
  inputtextbox.addEventListener("input", function () {
    inputtext = inputtextbox.value;
    if (inputtext){
      form.action=("/"+n+"/"+inputtext)
    }
    else{ 
      form.action=("/"+n)
    }
    clearTimeout(timer);
      timer = setTimeout(function() {
        form.submit();
        const spinner = document.getElementsByClassName(
          "arrow"
        )[0];
        spinner.classList.add("spin");
      }, 2000);
  });
}

autoSubmit();
const addOrRedos = document.getElementsByClassName("addOrRedo");
for (let i = 0; i < addOrRedos.length; i++) {
  addOrRedos[i].value = 0;
}

function submitRate(event, word) {
  event.preventDefault();
  const star = event.target.closest(".star");
  const rateForm = event.target.closest(".rate-form");
  const directionRate = event.target.closest(".rate-form").querySelector(".direction-rate");
  directionRate.value = n;
  const uri = "/rated";
  const addOrRedo = event.target.closest(".rate-form").querySelector(".addOrRedo");
  addOrRedo.value = parseInt(addOrRedo.value) + 1;
  fetch(uri, {
    method: 'POST',
    body: new FormData(rateForm)
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    // Handle the response here
  })
  .catch(error => {
    console.error('Error:', error);
    // Handle errors here
  });
  star.classList.toggle("rated");
  
  form.reset();
  const outputTextbox = document.getElementById("outputtextbox")
  outputTextbox.innerHTML = word
}

function togglePopup(){;
  document.getElementById("popup-1").classList.toggle("active");
  
}
document.getElementById('addWord-form').addEventListener('submit', function(event) {
  event.preventDefault();

  var thwordInput = document.getElementsByName('thword')[0];
  var nwordInput = document.getElementsByName('nword')[0];
  var definitionInput = document.getElementsByName('definition')[0];
  
  if (thwordInput.value.trim() === '' || definitionInput.value.trim() === '' || nwordInput.value.trim() === '') {
    // Display an alert
    alert('โปรดกรอกข้อมูลให้ครบ');
  } else {
    // Proceed with form submission
    const addWordForm = document.getElementById("addWord-form");
    const uri = "/added";
    fetch(uri, {
      method: 'POST',
      body: new FormData(addWordForm)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Handle the response here
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle errors here
    });
    addWordForm.reset();
    document.getElementById("popup-1").classList.toggle("active");
  }
});
form.addEventListener("submit", function (e) {
  e.preventDefault();

  const spinner = document.getElementsByClassName(
    "arrow"
  )[0];

  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/submit");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
if (xhr.readyState == XMLHttpRequest.DONE) {
  spinner.classList.remove("spin");
}
};
const formData = new FormData(form);
xhr.send(formData);
});

var inputTextbox = document.getElementById("inputtextbox");
var outputTextbox = document.getElementById("outputtextbox");
inputTextbox.addEventListener('input', () => {
  inputTextbox.style.height = 'auto';
  outputTextbox.style.height = 'auto';
  outputTextbox.style.height = inputTextbox.scrollHeight + 10 + 'px';
  inputTextbox.style.height = inputTextbox.scrollHeight + 10 + 'px';
});
outputTextbox.style.height = inputTextbox.scrollHeight + 10 + 'px';
inputTextbox.style.height = inputTextbox.scrollHeight + 10 + 'px';

function copyText() {
  const outputTextbox = document.getElementById("outputtextbox");
  outputTextbox.select(); // Select the text
  navigator.clipboard.writeText(outputTextbox.value); // Copy the selected text to the clipboard
}

function shareText() {
  const shareText = "https://kammuang.onrender.com/" + n + '/' +inputtext
  
  if (navigator.share) {
    navigator.share({
      title: "Shared Text",
      text: shareText
    })
      .then(() => console.log("Text shared successfully"))
      .catch((error) => console.log("Error sharing text:", error));
  } else {
    console.log("Web Share API not supported");
    // Fallback for browsers that do not support Web Share API
    // You can implement your custom sharing logic here
  }
}