document.addEventListener('DOMContentLoaded', function() {
    var messages = JSON.parse(document.getElementById('toastify-messages-data').textContent);
    
    messages.forEach(function(message) {
      var backgroundColor = message.tags.includes('success') ? 'green' : 'red';
      
      Toastify({
        text: message.text,
        duration: 5000,
        close: true,
        gravity: "bottom",
        position: "right",
        backgroundColor: backgroundColor,
      }).showToast();
    });
  });
  