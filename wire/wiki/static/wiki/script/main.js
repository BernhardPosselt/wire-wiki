var wiki = wiki || {};

$(document).ready(function(){
    // get javascript settings which need to be passed from the server
    // for instance urls, users etc
    var settingsUrl = $('html').data('settingsurl');
    $.getJSON(settingsUrl, function(settings){
        // settings are in the settings object
        
    });

    $(".show_diff").click(function(){
        $(".diff").slideToggle();
    })

    $("form.edit textarea").markItUp(mySettings);

});
