const equation = document.getElementById('equation');
const mathField = document.querySelector('math-field');

mathField.addEventListener('input', function () {
  const latexContent = document.querySelector('#dynamic-results');
  if (latexContent ) {
    let newSpan = latexContent.querySelector('.dynamic-result') ;
    if (!newSpan) {
      newSpan = document.createElement('span');
      newSpan.classList.add('dynamic-result');
      latexContent.appendChild(newSpan);
      
    }
    newSpan.style.background = 'linear-gradient(45deg, red, blue, green)';
    newSpan.style.webkitBackgroundClip = 'text'; // Ensure gradient applies to text
    newSpan.style.color = 'transparent'; // Make text color transparent so background shows through
    const equationText = mathField.getValue('ascii-math').replace(/\^/g, '**');
    try {
      const result = eval(equationText);
      newSpan.textContent = '=' + result.toFixed(1) || '';
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

    // Clear button click listener
    $('#clear').click(function() {
      mathField.setValue(''); // Clear the MathField content
      $('#dynamic-results').html(''); // Clear the result
      $('.output-pane').hide(); // Hide the output pane
    });
  $('#submit').click(function() {
    const expression = equation.getValue('ascii-math'); // Use .value to get the raw expression from input field
    const latexExpression = equation.getValue(); // Assuming this is the LaTeX expression (formatted)

    const calculationType = $('#options').val();
    
    if (!expression) {
      alert('Please enter an expression.');
      return;
    }
    
    $('.output-pane').html('<div class="loading-screen"><div class="loading-spinner"></div></div>'); 

    $('.output-pane').show();
    $.ajax({
      url: '/BhaskarAcharya',
      type: 'POST',
      data: {
        userInput: expression,
        calculationType: calculationType
      },
      success: function(response) {
        $('.output-pane .loading-screen').remove();
        $('.output-pane').html(`
          <div id="result"></div>
          <div id="stepsContent"></div>
          <div id="graphContent"></div>`); 
        $('#result').html('<b>Evaluated Result:</b><br><br>' + response.result.replace(/\n/g, '<br>'));
        $('#stepsContent').html('<b>Step-by-step Solution:</b><br><br>' + response.steps.replace(/\n/g, '<br>'));
        $('#graphContent').html('<b>Graph:</b><br><br><img src="data:image/png;base64,' + response.graph + '" alt="Graph" style="width: 100%; max-width: 600px;">');
        
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
    rightSlider.style.width = rightSlider.style.width === '100%' ? '0' : '100%';
    leftSlider.style.width = '0';
  }
  else{
    rightSlider.style.width = '0';
    leftSlider.style.width = '0';
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const dropdown = document.getElementById('options');
  const optionLinks = document.querySelectorAll('.option-link');

  // Function to remove persistent focus from all elements
  function removeAllFocus() {
      optionLinks.forEach(link => {
          link.classList.remove('persistent-focus');
      });
  }

  // Function to focus the corresponding link based on selected value
  function focusOptionLink(selectedValue) {
      removeAllFocus(); // Remove focus from all links before focusing the selected one

      // Find the link matching the selected option and add focus
      optionLinks.forEach(link => {
          if (link.getAttribute('data-option') === selectedValue) {
              link.classList.add('persistent-focus');
              link.focus(); // Focus the link visually
          }
      });
  }

  // Listen for changes on the dropdown menu
  dropdown.addEventListener('change', function () {
      const selectedValue = dropdown.value;
      focusOptionLink(selectedValue);
  });

  // Optional: Allow clicking on the links to keep their focus
  optionLinks.forEach(link => {
      link.addEventListener('click', function () {
          removeAllFocus(); // Remove focus from other links
          link.classList.add('persistent-focus'); // Focus the clicked link
      });
  });

  // On page load, apply the focus to the currently selected dropdown option
  focusOptionLink(dropdown.value);
});
document.querySelectorAll('.footer-button a').forEach(link => {
  link.addEventListener('click', function (e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);
      
      if (targetElement) {
          window.scrollTo({
              top: targetElement.offsetTop - 50,  // Scroll 50px above the target
              behavior: 'smooth' // Smooth scroll effect
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