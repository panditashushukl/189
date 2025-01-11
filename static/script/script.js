const equation = document.getElementById('equation');
const mathField = document.querySelector('math-field');

mathField.addEventListener('input', function () {
  const latexContent = mathField.shadowRoot.querySelector('.ML__latex');
  const newLine = mathField.shadowRoot.querySelector('.ML__container');
  if (latexContent ) {
    let newSpan = latexContent.querySelector('.dynamic-result') || newLine.querySelector('.dynamic-result');
    if (!newSpan) {
      newSpan = document.createElement('span');
      newSpan.classList.add('dynamic-result');
      if (window.innerWidth < 600) {
        newLine.appendChild(newSpan);
      }
      else{
        latexContent.appendChild(newSpan);
      }
      
    }
    if (window.innerWidth >= 600) {
      newSpan.style.marginLeft = '5px';
    }
    if (window.innerWidth<600){
      newSpan.style.alignItems = 'center';
      newSpan.style.height = '40px';
    }
    newSpan.style.background = 'linear-gradient(45deg, red, blue, green)';
    newSpan.style.webkitBackgroundClip = 'text'; // Ensure gradient applies to text
    newSpan.style.color = 'transparent'; // Make text color transparent so background shows through
    const equationText = mathField.getValue('ascii-math').replace(/\^/g, '**');
    try {
      const result = eval(equationText);
      newSpan.textContent = '=' + result.toFixed(1) || ' ';
    } catch (error) {
      newSpan.textContent = ' ';
    }
  }
});

document.querySelector('math-field').
  addEventListener('focus', () => { 
    mathVirtualKeyboard.layouts = ["numeric", "symbols","alphabetic"];
    mathVirtualKeyboard.visible = true;
  });

$(document).ready(function() {
  $('.output-pane').hide();
  $('#submit').click(function() {
    const expression = equation.getValue('ascii-math'); // Use .value to get the raw expression from input field
    const latexExpression = equation.getValue(); // Assuming this is the LaTeX expression (formatted)

    const calculationType = $('#options').val();
    
    if (!expression) {
      alert('Please enter an expression.');
      return;
    }

    $.ajax({
      url: '/BhaskarAcharya',
      type: 'POST',
      data: {
        userInput: expression,
        calculationType: calculationType
      },
      success: function(response) {
        $('#result').html('<b>Evaluated Result:</b><br><br>' + response.result.replace(/\n/g, '<br>'));
        $('#stepsContent').html('<b>Step-by-step Solution:</b><br><br>' + response.steps.replace(/\n/g, '<br>'));
        $('#graphContent').html('<b>Graph:</b><br><br><img src="data:image/png;base64,' + response.graph + '" alt="Graph" style="width: 100%; max-width: 600px;">');
        
        $('.output-pane').show();
        // Save LaTeX expression, result, and calculationType to history
        var history = JSON.parse(localStorage.getItem('history')) || [];
        history.push({
          latexExpression: latexExpression, // LaTeX expression
          result: response.result, // Store the result
          calculationType: calculationType // Store the calculation type
        });
        localStorage.setItem('history', JSON.stringify(history));
      },
      error: function(xhr, status, error) {
        alert('An error occurred. Please try again.');
      }
    });
  });

  // Handle history button click to load history
  $('#historyBtn').click(function() {
    const history = JSON.parse(localStorage.getItem('history')) || [];
    const historyList = $('#history-list');

    historyList.empty(); // Clear previous history

    if (history.length > 0) {
      history.forEach((entry, index) => {
        const historyItem = $('<div class="history-item"></div>');
        historyItem.html(`
          <p><strong>Equation: </strong><math-field  class="latex" readonly>${entry.latexExpression}</math-field></p>
          <p><strong>Result: </strong>${entry.result}</p>
          <p><strong>Operation: </strong>${entry.calculationType}</p>
          <button class="append-history" data-latex-expression="${entry.latexExpression}" data-calculation-type="${entry.calculationType}">Use this calculation</button>
          <hr />
        `);

        historyList.append(historyItem);
      });

      // Bind click event to use history item
      $('.append-history').click(function() {
        const latexExpression = $(this).data('latex-expression');
        const calculationType = $(this).data('calculation-type');
        $('#equation').val(latexExpression);  
        $('#options').val(calculationType); 
      });
    } else {
      historyList.html('<p>No history found.</p>');
    }
  });

  // Handle clear history button click
  $('#clearHistoryBtn').click(function() {
    localStorage.removeItem('history');
    $('#history-list').html('<p>History has been cleared.</p>');
  });
});
$(document).on('click', '.append-history', function() {
  toggleSlider('null');  // This will call the function with 'null' argument
});
const optionLinks = document.querySelectorAll('.option-link');
  optionLinks.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();  // Prevent the default behavior of the anchor tag
      const selectedOption = event.target.getAttribute('data-option');  // Get the value of data-option
      const selectElement = document.getElementById('options');  // Get the select element
      selectElement.value = selectedOption;  // Update the selected option in the dropdown
    });
});

function toggleSlider(direction) {
  const leftSlider = document.getElementById('leftSlider');
  const rightSlider = document.getElementById('rightSlider');
  
  if (direction === 'left') {
    leftSlider.style.width = leftSlider.style.width === '100%' ? '0' : '100%';
    rightSlider.style.width = '0';
  } else if (direction === 'right') {
    rightSlider.style.width = rightSlider.style.width === '50%' ? '0' : '50%';
    leftSlider.style.width = '0';
  }
  else{
    rightSlider.style.width = '0';
    leftSlider.style.width = '0';
  }
}