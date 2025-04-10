const output = document.querySelector('.output-pane')
let history = JSON.parse(localStorage.getItem('history')) || []
const options = document.querySelector('#options');
const equation = document.querySelector('#equation')

//This Event Listenenr is for printing dynamic Results
equation.addEventListener('input', function () {
  const equationText = equation.getValue('ascii-math').replace(/\^/g, '**');
  try {
    const result = eval(equationText);
    output.innerHTML = `= ${result.toFixed(3) || ''}`;
  } catch (error) {
    output.innerHTML = ' ';
  }
})

//Send Data To Server
function sendData(expression, calculationType){
  const formData = new URLSearchParams();
  formData.append('userInput', expression);
  formData.append('calculationType', calculationType);

  fetch('/BhaskarAcharya', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded', 
    },
    body: formData.toString()
  })
  .then(response => response.json())
  .then(data => {
    printData(data,expression)
    setHistory(data.result,expression)
    output.style.display = 'block'
  })
  .catch(error => {
    printError(error)
  });  
  
}
//Event Listener on Document Load
document.addEventListener('DOMContentLoaded', () => {
  addingClassToOptions()
  //Event Listener to Submit the Data
  document.querySelector('#submit').addEventListener('click',()=>{
    if (equation.getValue('ascii-math') === ''){
      output.innerHTML = `
        <div id="expression">
          <b style="color:red">Please Input an Expression</b>
        </div>
      `
      return
    }
    document.querySelector('.output-pane').innerHTML = '<div class="loading-screen"><div class="loading-spinner"></div></div>';
    sendData(equation.getValue('ascii-math'),options.value)
  })

  //Event Listener to clear the data
  document.querySelector('#clear').addEventListener('click',()=>{
    equation.setValue('')
    output.style.display = 'none'
  })
});

//Function that Prints data in Output Pane
function printData(data,expression){
  output.innerHTML = `
    <div id="expression">
      <b>Input Expression:</b><br><br>
      ${expression} 
    </div>
    <div id="result">
      <b>Evaluated Result:</b><br><br>
      ${data.result.replace(/\n/g, '<br>')} 
    </div>
    <div id="stepsContent">
      <b>Step-by-step Solution:</b><br><br> 
      <pre>${data.steps}</pre>
    </div>
    <div id="graphContent">
      <b>Graph:</b><br><br>
      <img src=data:image/png;base64,${data.graph}  alt="Graph" style="width: 100%; max-width: 600px;"> 
    </div>
  `
}

//If Error Occurred this function prints error
function printError(error){
  output.innerHTML = `
    <div id="expression"> ${error} </div>
  `
}

//This function is used to set history in the array and also sets in local storage
function setHistory(result,expression) {
  history.push({expression : expression, result : result, calculationType : options.value})
  localStorage.setItem("history", JSON.stringify(history))
}

//This function clears the History from the local storage
function clearHistory() {
  localStorage.removeItem("history");
  history = []
  document.querySelector('#history-list').innerHTML = ""
}

//This function is used to display History in slider span
function displayHistory(){
  history.map(({expression,result},index)=>{
    const historyItem =`
        <div id="expression">
          <b>Expression : </b>
          ${expression} <br><br>
          <b>Result:</b>
          <pre> ${result} </pre>
          <button class="useHistory" data-index="${index}"> Use this Calculation </button>
        </div>
    `
    document.querySelector('#history-list').innerHTML += historyItem
  })

  //Event Listener to use the data of history
  document.querySelectorAll('.useHistory').forEach(button => {
    button.addEventListener('click', (e) => {
      const index = e.target.getAttribute('data-index'); 
      expression = history[index].expression
      calculationType = history[index].calculationType
      equation.setValue(expression)
      options.value = calculationType
      addingClassToOptions()
      sendData(expression,calculationType)
      toggleSlider('null')
    });
  });
}


//Event Listener to set option Background on Click Event
const optionLinks = document.querySelectorAll('.option-link');
optionLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); 
        options.value = this.getAttribute('data-option');
        addingClassToOptions() 
    });
});

//Event listener to set option background when option changes
options.addEventListener('change',addingClassToOptions)
function addingClassToOptions() {
  optionLinks.forEach(member => {
    if (member.getAttribute('data-option') === options.value) {
      member.classList.add('option-link-active');
    } else {
      member.classList.remove('option-link-active');
    }
  });
}

//Event Listener to toggle the slider
document.querySelectorAll('.right-slider .option-link').forEach(el => {
  el.addEventListener('click', (event) => {
    toggleSlider(event.target, 'none');
  });
});

//This Function is used to toggle the slider
function toggleSlider(direction) {
  const leftSlider = document.getElementById('leftSlider');
  const rightSlider = document.getElementById('rightSlider');
  
  if (direction === 'left') {
    leftSlider.style.width = leftSlider.style.width === '100%' ? '0' : '100%';
    rightSlider.style.width = '0';
  } else if (direction === 'right') {
    rightSlider.style.width = rightSlider.style.width === '100%' ? '0' : '100%';
    leftSlider.style.width = '0';
  }
  else{
    rightSlider.style.width = '0';
    leftSlider.style.width = '0';
  }
}

//This sets footer anchor click to scroll top 50px below insted of top 0
document.querySelectorAll('.footer-button a').forEach(link => {
  link.addEventListener('click', function (e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);
      
      if (targetElement) {
          window.scrollTo({
              top: targetElement.offsetTop - 50, 
              behavior: 'smooth'
          });
      }
  });
});

// Get the button element
const toggleButton = document.getElementById("toggleTheme");
const leftSpan = document.querySelector('.left-span');
const rightSpan = document.querySelector('.right-span');
const dropDownMenu = document.querySelector('.dropdown-menu');

// Check localStorage for saved theme preference
const currentTheme = localStorage.getItem("theme") || 
 (window.matchMedia('(prefers-color-scheme: dark)').matches ? "dark-mode" : "light-mode");
// Apply the saved theme on page load
document.body.classList.add(currentTheme);
leftSpan.classList.add(currentTheme);
equation.classList.add(currentTheme);
dropDownMenu.classList.add(currentTheme);
// Toggle the theme when the button is clicked
toggleButton.addEventListener("click", function () {
  if (document.body.classList.contains("dark-mode")) {
    document.body.classList.remove("dark-mode");
    leftSpan.classList.remove("dark-mode");
     equation.classList.remove("dark-mode");
     dropDownMenu.classList.remove("dark-mode");
    localStorage.setItem("theme", "light-mode");
  } else {
   document.body.classList.add("dark-mode");
   leftSpan.classList.add("dark-mode");
   equation.classList.add("dark-mode");
   dropDownMenu.classList.add("dark-mode");
    localStorage.setItem("theme", "dark-mode");
}
});