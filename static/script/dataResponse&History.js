//This Page Contains data related to request, response, history
const output = document.querySelector('.output-pane')
let history = JSON.parse(localStorage.getItem('history')) || []
const options = document.querySelector('#options');
const equation = document.querySelector('#equation')

//This Event Listenenr is for printing dynamic Results
equation.addEventListener('input', function () {
  if(options.value ==='simple'){
    const equationText = equation.getValue('ascii-math').replace(/\^/g, '**');
    try {
      const result = eval(equationText);
      equation.setAttribute('data-result', `= ${result.toFixed(3)}`);
    } catch (error) {
      equation.setAttribute('data-result', '');
    }
  }
})

//Send Data To Server
function sendData(expression, calculationType) {
  const data = {
    userInput: expression,
    calculationType: calculationType
  };

  fetch('/BhaskarAcharya', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)  // Send JSON directly
  })
  .then(response => response.json())
  .then(data => {    
    printData(data, expression);
    setHistory(data.result, expression);
    equation.setAttribute('data-result', '');
    if (equation.hasAttribute('error-display')) {
      equation.removeAttribute('error-display');
    }
    output.style.display = 'block';
    if (data.plot_info && data.plot_array) {
      plotQuadratic(data.plot_info, data.plot_array,expression);
    }
  })
  .catch(error => {
    printError(error);
  });
}


function dynamicError(str) {
  equation.setAttribute('error-display', str)
  setTimeout(() => {
    equation.removeAttribute('error-display')
  }, 9000)
}

//Function to Submit the Data
function submitData () {
  const equationValue = equation.getValue('ascii-math')
  if (equationValue === ''){
    dynamicError('*Please enter a Expression')
    return
  }
  const commaCount = (equationValue.match(/,/g) || []).length;
  const equalCount = (equationValue.match(/=/g) || []).length;
  if (options.value === 'linear1') {
    if (equalCount!==1) {
      dynamicError('*Please provide expressions in form ax+b=0')
      return
    }
  }
  else if (options.value === 'linear2') {
    if (commaCount!==1) {
      dynamicError('*Please provide comma between expressions.')
      return
    } else if (equalCount!==2) {
      dynamicError('*Please provide expressions in form ax+by+c=0')
      return
    }
    
  }
  else if (options.value === 'linear3') {
    if (commaCount!==2) {
      dynamicError('*Please provide comma between expressions.')
      return
    } else if (equalCount!==3) {
      dynamicError('*Please provide expressions in form ax+by+cz+d=0')
      return
    }
  }
  output.innerHTML = '<div class="loading-screen"><div class="loading-spinner"></div></div>';
  sendData(equation.getValue('ascii-math'),options.value)
}

//Event Listener on Document Load
document.addEventListener('DOMContentLoaded', () => {
  addingClassToOptions()

  //Event Listener to Submit the Data
  document.querySelector('#submit').addEventListener('click',submitData)
  equation.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
      event.preventDefault();
      submitData()
    }
  })

  //Event Listener to clear the data
  document.querySelector('#clear').addEventListener('click',()=>{
    equation.setValue('')
    equation.setAttribute('data-result', '');
    output.style.display = 'none'
  })
});

//Function that Prints data in Output Pane
function printData(data,expression){
  output.innerHTML = `
    <div class="box-styling" id="expression">
      <b>Input Expression:</b><br><br>
      ${expression} 
    </div>
    <div class="box-styling" id="result">
      <b>Evaluated Result:</b><br><br>
      ${data.result.replace(/\n/g, '<br>')} 
    </div>
    <div class="box-styling" id="stepsContent">
      <b>Step-by-step Solution:</b><br><br> 
      ${data.steps.replace(/\n/g, '<br>')} 
    </div>
  `
  if (data.graph){
    output.innerHTML += `
    <div class="box-styling" id="graphContent">
      <img src=data:image/png;base64,${data.graph}  alt="Graph" style="width: 100%; max-width: 600px;"> 
    </div>
    `
  }
}

//If Error Occurred this function prints error
function printError(error){
  output.innerHTML = `
    <div class="box-styling"> ${error} </div>
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
        <div class="box-styling">
          <b>Expression : </b>
          ${expression} <br><br>
          <b>Result:</b>
          <pre> ${result} </pre>
          <button class="useHistory button-style" data-index="${index}"> Use this Calculation </button>
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
const optionLinks = document.querySelectorAll('.link');
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
      member.classList.add('link-active');
    } else {
      member.classList.remove('link-active');
    }
  });
}
