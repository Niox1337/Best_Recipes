$(document).ready(function(){

    
    // TODO: we currenly dont unempty the first star - kinda minor aeshetic issue but still
    // TODO: we don't want users to be able to rate their own recipes
    
    // we need to access some things from django without directly referencing them in javascript
    // so we get django to put them in a div and pull them with jquery...
    $('#for_jquery').hide()
    
    function handle_delete_profile(delete_account) {
    
        let username  = $("#username").text();
        let handle_delete_profile_url = $("#handle_delete_url").text();
    
        $.ajax({
            type: 'GET',
                    url: handle_delete_profile_url,
                    data: {
                        "username": username,
                        "delete_account": delete_account,
                    },
                    success: function (response) {
                        console.log(response)
                    },
                    error: function (response) {
                        console.log(response);
                    }
                })
    }
       

    $("#yes_button").click(
        function() {
            handle_delete_profile(true);
            window.location.replace($("#logout_url").text());
        }
    )

    $("#no_button").click(
        function() {
            handle_delete_profile(false);
            window.location.replace("/");
        }
    )

    });