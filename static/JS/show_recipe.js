$(document).ready(function(){

    
    // TODO: we currenly dont unempty the first star - kinda minor aeshetic issue but still
    // TODO: we don't want users to be able to rate their own recipes
    
    // we need to access some things from django without directly referencing them in javascript
    // so we get django to put them in a div and pull them with jquery...
    $('#for_jquery').hide()
    
    function initalize_favourite_button() {
    
        let username  = $("#username").text();
        let recipe_name_slug = $("#recipe_name_slug").text();
        let get_favourited_status_url = $("#get_favourited_status").text();
    
        console.log("CALLED");
    
        $.ajax({
            type: 'GET',
                    url: get_favourited_status_url,
                    data: {
                        "recipe": recipe_name_slug,
                        "user": username,
                    },
                    success: function (response) {
                        favourited = response["favourited"]
                        if (favourited == true) {
                            console.log("setting unfav")
                            $("#favourite_button_container").children("button").text("Unfavourite");
                        }
                        else {
                            console.log("setting fav")
                            $("#favourite_button_container").children("button").text("Favourite");
                        }
                    },
                    error: function (response) {
                        console.log(response);
                    }
                })
    }
    
    function set_favourited_status(favourited) {
    
        let username  = $("#username").text();
        let recipe_name_slug = $("#recipe_name_slug").text();
        let set_favourited_status_url = $("#set_favourited_status").text();
    
        $.ajax({
            type: 'GET',
                    url: set_favourited_status_url,
                    data: {
                        "recipe": recipe_name_slug,
                        "user": username,
                        "favourited": favourited,
                    },
                    success: function (response) {
                        console.log(response)
                    },
                    error: function (response) {
                        console.log(response);
                    }
                })
    }
    
    function toggle_favourite_button() {
        let favourited = $("#favourite_button_container").children("button").text();
        if (favourited == "Favourite") {
            set_favourited_status(true);
            $("#favourite_button_container").children("button").text("Unfavourite");
        }
        else {
            set_favourited_status(false);
            $("#favourite_button_container").children("button").text("Favourite");
        }
    }
    
    $("#favourite_button_container").children("button").click(
        function() { toggle_favourite_button(); }
    )
    
    initalize_favourite_button();
    
    function update_recipe_rating_div(rating_data) {
        let rating_text = "Rating: " + rating_data["rating"] + " (" + rating_data["no_of_ratings"] + " ratings so far)";
        $("#rating_text").text(rating_text)
      }
    
    function get_recipe_rating_data() {
    
        let recipe_name_slug = $("#recipe_name_slug").text();
        let get_rating_data_url = $("#get_recipe_rating").text();
    
        $.ajax({
            type: 'GET',
                    url: get_rating_data_url,
                    data: {
                        "recipe": recipe_name_slug,
                    },
                    success: function (response) {
                        let rating = response["rating"];
                        let no_of_ratings = response["no_of_ratings"];
                        console.log("Got rating " + rating + " and no of ratings " + no_of_ratings);
                        update_recipe_rating_div(response);
                    },
                    error: function (response) {
                        console.log(response);
                    }
                })
      }
    
      get_recipe_rating_data()
    
      function star_click(star_div_id) {
    
        let username  = $("#username").text();
        let recipe_name_slug = $("#recipe_name_slug").text();
        let give_rating_url = $("#give_rating").text();
    
        console.log("hi");
        console.log(username)
    
        let star_number = star_div_id.charAt(star_div_id.length - 1);
    
        $.ajax({
                    type: 'GET',
                    url: give_rating_url,
                    data: {
                        "rating": star_number,
                        "user": username,
                        "recipe": recipe_name_slug,
                    },
                    success: function (response) {
                        console.log("it worked!!");
                        get_recipe_rating_data()
                    },
                    error: function (response) {
                        console.log(response)
                    }
                })
        
        
    
      }
    
      function user_current_rating() {
        console.log("LOADING!");
    
        let username  = $("#username").text();
        let recipe_name_slug = $("#recipe_name_slug").text();
        let get_rating_url = $("#get_rating").text();
    
        $.ajax({
                    type: 'GET',
                    url: get_rating_url,
                    data: {
                        "user": username,
                        "recipe": recipe_name_slug,
                    },
                    success: function (response) {
                        let rating = parseInt(response["rating"])
                        console.log("got rating of " + rating);
                        if (rating > 0) {
                            star_hover("star_" + rating);
                        }
                    },
                    error: function (response) {
                        console.log(response)
                    }
                })
    
      }
      
      user_current_rating();
    
      function empty_star(star_div_id) {
        let empty_star_path = $("#empty_star_path").text();
        $("#" + star_div_id).children("img").attr("src", empty_star_path);
      }
    
      function fill_star(star_div_id) {
        let full_star_path = $("#full_star_path").text();
        $("#" + star_div_id).children("img").attr("src", full_star_path);
      }
    
      function star_hover(star_div_id) {
        console.log(star_div_id)
        let star_num = parseInt(star_div_id.charAt(star_div_id.length - 1))
    
        for (let i = 1; i < 6; i++) {
            if (i < star_num + 1) {
                fill_star("star_" + i);
                last_star_filled = i;
            }
            else {
                empty_star("star_" + i);
            }
        }
    
      }
    
      $('.star').click(
        function() {
            star_click(this.id);
        }
      )
    
      $('.star').hover(
        function() {
            star_hover(this.id);
        }
      )
    
    });