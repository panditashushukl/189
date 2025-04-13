//This Page Contains Data about slider function changing background on sidebar option and Scroll the page 50 px below screen and toggleing Background
document.addEventListener('DOMContentLoaded', () => {
  // Button to change the Theme
  const toggleButton = document.getElementById("toggleTheme");
  toggleButton.addEventListener('click', toggleTheme)
})
//Function to toggleTheme
const toggleTheme = () => {
  const imglst = ['steps','graph','Ido']
  const images = document.querySelectorAll('.toggle-img');
  const rootStyles = getComputedStyle(document.documentElement);
  const colorScheme = rootStyles.getPropertyValue('color-scheme').trim();
  if (colorScheme === 'dark') {
      document.documentElement.style.colorScheme = 'light';
      document.documentElement.removeAttribute('data-theme', 'dark');
      images.forEach((img, index) => {
        img.src = `../static/images/${imglst[index]}light.png`
      });
  
  } else {
      document.documentElement.style.colorScheme = 'dark';
      document.documentElement.setAttribute('data-theme', 'dark');
      images.forEach((img, index) => {
        img.src = `../static/images/${imglst[index]}dark.png`
      });
  }
}

//Event Listener to toggle the slider
document.querySelectorAll('.right-slider .link').forEach(el => {
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

//Slider of the Explaination Page
let currentSlide = 0; 
const totalSlides = document.querySelectorAll('.slide').length;
const slidesWrapper = document.querySelector('.slides-wrapper');

function goToNextSlide() {
  currentSlide = (currentSlide + 1) % totalSlides;
  slidesWrapper.style.transform = `translateX(-${currentSlide * 100}%)`; 
}

setInterval(goToNextSlide, 8000);