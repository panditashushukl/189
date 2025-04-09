const output = document.querySelector('.output-pane')
let history = JSON.parse(localStorage.getItem('history')) || []
const options = document.querySelector('#options');
const equation = document.querySelector('#equation')

equation.addEventListener('input', function () {
  const equationText = equation.getValue('ascii-math').replace(/\^/g, '**');
  try {
    const result = eval(equationText);
    output.innerHTML = `= ${result.toFixed(3) || ''}`;
  } catch (error) {
    output.innerHTML = ' ';
  }
})
function sendData(expression, calculationType){
  const formData = new URLSearchParams();
  formData.append('userInput', expression);
  formData.append('calculationType', calculationType);

  fetch('/BhaskarAcharya', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded', // change content type
    },
    body: formData.toString() // convert the form data to query string format
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

document.addEventListener('DOMContentLoaded', () => {
  settingOptionBackground()
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

  document.querySelector('#clear').addEventListener('click',()=>{
    equation.setValue('')
    output.style.display = 'none'
  })
});


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

function printError(error){
  output.innerHTML = `
    <div id="expression"> ${error} </div>
  `
}

function setHistory(result,expression) {
  history.push({expression : expression, result : result, calculationType : options.value})
  localStorage.setItem("history", JSON.stringify(history))
}

function clearHistory() {
  localStorage.removeItem("history");
  history = []
  document.querySelector('#history-list').innerHTML = ""
}

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

  document.querySelectorAll('.useHistory').forEach(button => {
    button.addEventListener('click', (e) => {
      const index = e.target.getAttribute('data-index'); 
      expression = history[index].expression
      calculationType = history[index].calculationType
      equation.setValue(expression)
      options.value = calculationType
      settingOptionBackground()
      sendData(expression,calculationType)
      toggleSlider('null')
    });
  });

}

options.addEventListener('change',settingOptionBackground)
const optionLinks = document.querySelectorAll('.option-link');
optionLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); 
        options.value = this.getAttribute('data-option');
        settingOptionBackground() 
    });
});
function settingOptionBackground() {
  optionLinks.forEach(member => {
    if (member.getAttribute('data-option') === options.value) {
      member.classList.add('option-link-active');
    } else {
      member.classList.remove('option-link-active');
    }
  });
}

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
const equationID = document.querySelector('#equation');
const dropDownMenu = document.querySelector('.dropdown-menu');

// Check localStorage for saved theme preference
const currentTheme = localStorage.getItem("theme") || 
 (window.matchMedia('(prefers-color-scheme: dark)').matches ? "dark-mode" : "light-mode");
// Apply the saved theme on page load
document.body.classList.add(currentTheme);
leftSpan.classList.add(currentTheme);
rightSpan.classList.add(currentTheme);
equationID.classList.add(currentTheme);
dropDownMenu.classList.add(currentTheme);
// Toggle the theme when the button is clicked
toggleButton.addEventListener("click", function () {
  if (document.body.classList.contains("dark-mode")) {
    document.body.classList.remove("dark-mode");
    leftSpan.classList.remove("dark-mode");
     rightSpan.classList.remove("dark-mode");
     equationID.classList.remove("dark-mode");
     dropDownMenu.classList.remove("dark-mode");
    localStorage.setItem("theme", "light-mode");
  } else {
   document.body.classList.add("dark-mode");
   leftSpan.classList.add("dark-mode");
   rightSpan.classList.add("dark-mode");
   equationID.classList.add("dark-mode");
   dropDownMenu.classList.add("dark-mode");
    localStorage.setItem("theme", "dark-mode");
}
});