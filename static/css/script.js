let selectedInputField = null;

function updateFields() {
    const radioOptions = document.getElementsByName('calculationType');
    let selectedOption = null;
    radioOptions.forEach(option => {
        if (option.checked) {
            selectedOption = option.value;
            var labelElement = document.querySelector("label[for='" + option.id + "']");
            document.getElementById("selectedOption").innerHTML = "Selected Option: " + labelElement.innerHTML;
        }
    });

    // Store the selected option in localStorage
    localStorage.setItem('selectedOption', selectedOption);

    const inputFieldsContainer = document.getElementById('inputFieldsContainer');
    inputFieldsContainer.innerHTML = ''; // Clear previous input fields
    const placeholderMap = {
        "quadratic": "Equation of form ax^2+bx+c=0",
        "simple": "Expression of form a+b-c*d/e%f^g^(1/2)h^3√i",
        "functions": "Expression of function with arguments ,i.e., function(argument)",
        "linear1": "Equation of form ax+b=0",
        "linear2": "Equation of form ax+by+c=0",
        "linear3": "Equation of form ax+by+cz+d=0",
        // options and placeholders 
    };

    if (selectedOption === "quadratic" || selectedOption === "simple" || selectedOption === "functions") {
        createInputField('userInput', 'Enter Expression : ', placeholderMap[selectedOption]);
    } else if (selectedOption === "linear1" || selectedOption === "linear2" || selectedOption === "linear3" || selectedOption === "linear4") {
        const numVariables = parseInt(selectedOption.charAt(selectedOption.length - 1));
        for (let i = 1; i <= numVariables; i++) {
            createInputField(`userInput${i}`, `Enter Equation ${i} : `, placeholderMap[selectedOption]);
        }
    } else {
        // Handle the case when none of the specific options is selected
        createInputField('userInput', 'Enter Default Input : ', '');
        
    }
}

function createInputField(inputName, labelText, placeholder) {
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.placeholder = placeholder;
    inputField.classList.add('input-container');
    inputField.name = inputName; // Set the name for the input field
    const label = document.createElement('label');
    label.textContent = labelText;
    label.for = inputName; // Set the 'for' attribute for the label
    inputFieldsContainer.appendChild(label);
    inputFieldsContainer.appendChild(inputField);
    const lineBreak = document.createElement('br');
    inputFieldsContainer.appendChild(lineBreak);
    inputField.onfocus = function () {
        selectedInputField = inputField;
    };
    
}

function deleteCharacter() {
    if (selectedInputField) {
        const cursorPosition = selectedInputField.selectionStart;
        if (cursorPosition > 0) {
            const text = selectedInputField.value;
            const newText = text.substring(0, cursorPosition - 1) + text.substring(cursorPosition);
            selectedInputField.value = newText;
            selectedInputField.selectionStart = selectedInputField.selectionEnd = cursorPosition - 1;
            selectedInputField.focus();
        }
    }
}

function clearInput() {
    if (selectedInputField) {
        selectedInputField.value = '';
    }
    selectedInputField.focus();
}


function addCharacter(character) {
    if (selectedInputField) {
        const cursorPosition = selectedInputField.selectionStart;
        const text = selectedInputField.value;
        const newText = text.substring(0, cursorPosition) + character + text.substring(cursorPosition);

        selectedInputField.value = newText;
        selectedInputField.selectionStart = selectedInputField.selectionEnd = cursorPosition + character.length;
        selectedInputField.focus();
    }
}


document.addEventListener('DOMContentLoaded', function () {
    // Call the loadSelectedOption function when the DOM is fully loaded
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        loadSelectedOption();
        // Update input fields based on the selected option
        updateFields();
    } else {
        document.addEventListener('DOMContentLoaded', function () {
            loadSelectedOption();
            // Update input fields based on the selected option
            updateFields();
        });
    }
});


function loadSelectedOption() {
    const selectedOption = localStorage.getItem('selectedOption');
    const radioOptions = document.querySelectorAll('[name="calculationType"]');

    if (selectedOption) {
        radioOptions.forEach(option => {
            if (option.value === selectedOption) {
                option.checked = true;
            }
        });
    } else {
        // If no option is stored, set a default option here
        // For example, you can set the first option as the default:
        radioOptions[0].checked = true;
    }
}


function submitForm() {
    const inputFields = document.querySelectorAll('.user-input-container');
    const inputData = {};

    inputFields.forEach(inputField => {
        inputData[inputField.name] = inputField.value;
    });

    // Now, you can pass the data (inputData) to your Flask module or perform further actions with it.
    console.log('Input Data:', inputData);
}
function sendDataToServer() {
    const inputFields = document.querySelectorAll('.user-input-container');
    const inputData = {};

    inputFields.forEach(inputField => {
        inputData[inputField.name] = inputField.value;
    });

    // Send the data to your Flask module using an AJAX request
    fetch('/calculate', {
        method: 'POST',
        body: JSON.stringify(inputData),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the Flask module if needed
        // For example, you can update the result on the page.
        const resultElement = document.getElementById('result');
        resultElement.innerHTML = `<h2>${data.result}</h2>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
const buttonTable = document.getElementById('buttonTable');
const toggleButton = document.getElementById('toggleButton');

// Check if there's a saved state in localStorage
const storedState = localStorage.getItem('buttonTableState');
if (storedState === 'visible') {
    buttonTable.style.display = 'table';
} else {
    buttonTable.style.display = 'none';
}

toggleButton.addEventListener('click', function () {
    if (buttonTable.style.display === 'none') {
        buttonTable.style.display = 'table';
        // Save the state to localStorage
        localStorage.setItem('buttonTableState', 'visible');
    } else {
        buttonTable.style.display = 'none';
        // Save the state to localStorage
        localStorage.setItem('buttonTableState', 'hidden');
    }
});
  function toggleInfo() {
    var infoItem = document.getElementById('infoItem');
    infoItem.classList.toggle('active');
  }

  document.addEventListener('click', function (event) {
    var infoButton = document.getElementById('infobutton');
    var infoItem = document.getElementById('infoItem');

    if (event.target !== infoButton && event.target !== infoItem) {
      infoItem.classList.remove('active');
    }
  });
  function toggleSlider(direction) {
    const leftSlider = document.getElementById('leftSlider');
    const rightSlider = document.getElementById('rightSlider');

    if (direction === 'left') {
      leftSlider.style.width = leftSlider.style.width === '100%' ? '0' : '100%';
      rightSlider.style.width = '0';
    } else if (direction === 'right') {
      rightSlider.style.width = rightSlider.style.width === '250px' ? '0' : '250px';
      leftSlider.style.width = '0';
    }
  }
  function openOptionsModal() {
const optionsModal = document.getElementById('optionsModal');
optionsModal.style.display = 'block';
}

  function closeOptionsModal() {
    const optionsModal = document.getElementById('optionsModal');
    optionsModal.style.display = 'none';
  }

  // Close the modal if the user clicks outside of it
  window.onclick = function (event) {
    const optionsModal = document.getElementById('optionsModal');
    if (event.target === optionsModal) {
      optionsModal.style.display = 'none';
    }
  };


document.getElementById("stepsButton").addEventListener("click", function() {
    toggleContent('stepsContent');
});

function toggleContent(contentId) {
    var content = document.getElementById(contentId);
    if (content.style.display === "none") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
}
  // Call the loadSelectedOption function when the page loads
window.addEventListener('load', loadSelectedOption);
