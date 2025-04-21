$(document).ready(function() {

        // // Send the AJAX request
        // $.ajax({
        //     type: 'POST',
        //     url: '/login',
        //     data: formData,
        //     success: function(response) {
        //         // Handle success (e.g., redirect to dashboard)
        //         window.location.href = '/dashboard';
        //     },
        //     error: function(xhr, status, error) {
        //         // Handle error (e.g., show error message)
        //         alert('Login failed: ' + xhr.responseText);
        //     }
        // });

        $(document).on('submit', '#login-form', function(event) {
            event.preventDefault();
    
            var formData = $(this).serialize();
    
            if (formData) {
                console.log("Inicio Sesión!");
                console.log(formData);
            }
        });
    
        $(document).on('submit', '#register-form', function(event) {
            event.preventDefault();
    
            var formData = $(this).serialize();
    
            if (formData) {
                console.log("Registro!");
                console.log(formData);
            }
        });
});


function login() {
    console.log("login");
}