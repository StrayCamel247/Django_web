jQuery(function ($) {
    "use strict";
    // Get the form.
    var form = $('#ajax-form');

    // Get the button.
    var sendbutton = $('#sendbutton');

    // Get the messages div.
    var formMessages = $('#form-messages');

    // Set up an event listener for the contact form.
    $(form).submit(function (e) {
        // Stop the browser from submitting the form.
        e.preventDefault();
        
        // Disable the button
        sendbutton.prop('disabled', true);

        // Serialize the form data.
        var formData = $(form).serialize();

        // Submit the form using AJAX.
        $.ajax({
            type: 'POST',
            url: $(form).attr('action'),
            data: formData
        }).done(function (response) {
            
            // Make sure that the formMessages div has the 'ajax-success' class.
            $(formMessages).removeClass('ajax-error');
            $(formMessages).addClass('ajax-success');

            // Set the message text.
            $(formMessages).text(response);

            // Clear the form.
            $('#sendername').val('');
            $('#senderemail').val('');
            $('#senderphone').val('');
            $('#sendermessage').val('');
            
            // Display the button
            sendbutton.prop('disabled', false);
            
        }).fail(function (data) {
            
            // Make sure that the formMessages div has the 'ajax-error' class.
            $(formMessages).removeClass('ajax-success');
            $(formMessages).addClass('ajax-error');

            // Set the message text.
            if (data.responseText !== '') {
                // Display the message
                $(formMessages).text(data.responseText);
                // Display the button
                sendbutton.prop('disabled', false);
            } else {
                // Display the error message
                $(formMessages).text('Oops! An error occured and your message could not be sent.');
                // Display the button
                sendbutton.prop('disabled', false);
            }
        });
    });
});