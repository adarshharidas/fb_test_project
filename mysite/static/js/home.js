$(document).ready(function() {
	// body...
	
	$("#update_page_form").submit(function(e) {
        e.preventDefault();
    }).validate({
        rules: {
            about: {
                required: true,
                minlength: 5
            },
            phone: {
                required: true,
                minlength: 5
            },
            emails: {
                required: true,
                minlength: 5,
            },
            // street: {
            //     required: true,
            //     minlength: 3
            // },
            // city: {
            //     required: true,
            //     minlength: 2
            // },
            // country: {
            //     required: true,
            //     minlength: 2
            // },
            // zip: {
            //     required: true,
            //     minlength: 4
            // }
        },
        submitHandler: function(form) { 
            $.ajax({
                url: '/update-page', 
                type: 'POST',
                data: $('#update_page_form').serialize(),
                success: function(data){
                	console.log(data, "::::::::::::::::::::::::::::::")
                	// swal("Success", 'Updated', 'success');
                    window.location = '/?st='+data['success']+'&em='+data['eum']
                }
            });
            return false;  //This doesn't prevent the form from submitting.
        }
    });
     $("#update").on('click', function() {
        $("#update_page_form").submit();
    });

});