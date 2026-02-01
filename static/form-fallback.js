// Alternative: Form submission method (bypasses CORS)
function submitToGoogleForms(formData, callback) {
    // Create hidden form
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = 'https://script.google.com/macros/s/AKfycbwB77DBzA1M_FmV5nV9Yz3TtUJgVWnylnQ78jhqcTPQgD1c19hcY0O7-9XuA0iLun3JIA/exec';
    form.target = 'hidden_iframe';
    form.style.display = 'none';
    
    // Add form data as hidden inputs
    Object.keys(formData).forEach(key => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = formData[key];
        form.appendChild(input);
    });
    
    // Create hidden iframe for response
    const iframe = document.createElement('iframe');
    iframe.name = 'hidden_iframe';
    iframe.style.display = 'none';
    
    // Handle response
    iframe.onload = function() {
        callback(true);
        document.body.removeChild(form);
        document.body.removeChild(iframe);
    };
    
    // Submit form
    document.body.appendChild(iframe);
    document.body.appendChild(form);
    form.submit();
}

// Usage example:
// submitToGoogleForms({
//     formType: 'contact',
//     name: 'John Doe',
//     email: 'john@example.com',
//     message: 'Hello'
// }, function(success) {
//     if (success) {
//         alert('Form submitted successfully!');
//     }
// });