// Select the contact form
const contactForm = document.getElementById('contactForm');

// Add event listener for form submission
contactForm.addEventListener('submit', function (event) {
    event.preventDefault();

    // Get form values
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    // Basic validation
    if (name && email && message) {
        alert('Thank you for your message!');
        // Clear form
        contactForm.reset();
    } else {
        alert('Please fill out all fields.');
    }
});

// Function to open the modal
function showNewEntryForm() {
    document.getElementById('modal').classList.add('show');
  }
  
  // Function to close the modal
  function closeNewEntryForm() {
    document.getElementById('modal').classList.remove('show');
  }
  