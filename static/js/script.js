// Smooth Scroll for Navigation
document.querySelectorAll('.smooth-scroll').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Function to toggle high contrast mode
function toggleContrast() {
    document.body.classList.toggle('high-contrast');
}

// Function to increase font size
function increaseFont() {
    let currentSize = parseFloat(window.getComputedStyle(document.body).fontSize);
    document.body.style.fontSize = (currentSize * 1.1) + 'px';
}

// Function to decrease font size
function decreaseFont() {
    let currentSize = parseFloat(window.getComputedStyle(document.body).fontSize);
    document.body.style.fontSize = (currentSize * 0.9) + 'px';
}

// Function to summarize text
function summarizeText() {
    const inputText = document.getElementById('inputText').value;
    const summaryLength = document.getElementById('summaryLength').value;
    const summaryOutput = document.getElementById('summaryOutput');

    let summary = "This is a placeholder summary.";
    if (summaryLength === 'short') {
        summary = inputText.substring(0, 100) + "...";
    } else if (summaryLength === 'medium') {
        summary = inputText.substring(0, 300) + "...";
    } else if (summaryLength === 'detailed') {
        summary = inputText;
    }

    summaryOutput.textContent = summary;
}

// Select all list items in the "How It Works" section
const howItWorksItems = document.querySelectorAll('#how-it-works li');

// Function to add fade-in effect when in viewport
function animateOnScroll() {
    howItWorksItems.forEach((item, index) => {
        const rect = item.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
            // Add fade-in class with delay for staggered effect
            setTimeout(() => {
                item.classList.add('fade-in');
            }, index * 150); // 150ms delay for staggered animation
        }
    });

    // Animate sections when they come into view (added 'visible' class as per CSS)
    document.querySelectorAll('.fade-in-section').forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
            section.classList.add('visible');
        }
    });

    // Animate team members when they come into view (added 'visible' class as per CSS)
    document.querySelectorAll('.team-member').forEach(member => {
        const rect = member.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
            member.classList.add('visible');
        }
    });
}

// Event listener for scroll
window.addEventListener('scroll', animateOnScroll);

// Initialize scrolling text effect (assuming you're adding a 'scrolling' class to span elements)
document.querySelectorAll('.scrolling-text span').forEach(text => {
    text.classList.add('scrolling');
});

// Function for logo animation (glowing effect for logos as per CSS)
document.querySelectorAll('.logo-grid img').forEach(logo => {
    logo.classList.add('glowing');
});



// Function for Text-to-Speech
function textToSpeech(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(utterance);
    } else {
        alert('Text-to-speech is not supported in your browser.');
    }
}

// Function for Speech-to-Text
function speechToText() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.start();

        recognition.onresult = (event) => {
            const spokenText = event.results[0][0].transcript;
            document.getElementById('inputText').value = spokenText;
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error detected: ' + event.error);
            alert('Error during speech recognition: ' + event.error);
        };

    } else {
        alert('Speech-to-text is not supported in your browser.');
    }
}

// Example usage
// Attach event listeners to buttons for text-to-speech and speech-to-text
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.cta-btn').addEventListener('click', () => {
        const text = document.getElementById('summaryOutput').innerText;
        textToSpeech(text);
    });

    // Optional button to trigger speech-to-text if you create one:
    // document.getElementById('startRecordingButton').addEventListener('click', speechToText);
});
