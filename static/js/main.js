$(document).ready(function(){

    //add click handlers to buttons

    function send_button_state(hex_state) {
        $.ajax({
            url: "webpower/set/" + hex_state,
            success: function() {
                console.log("sent: " + hex_state)
            },
        });
    }

    $(".outlet-button").on( "click", function() {
                $( this ).button('toggle');
                var state = get_button_state();
                send_button_state(state);
                console.log("sending outlet state: " + state);
});

    function get_button_state() {
        btn_state = ""
        $(".outlet-button").each(function (index) {
            is_active = $(this).hasClass("active");
            if (is_active===true){
                btn_state = "1" + btn_state;
            }
            else if (is_active===false){
                btn_state = "0" + btn_state;
            }
        });
        btn_state = parseInt(btn_state,2);
        btn_state = btn_state.toString(16);
        return(btn_state)
    }
    function set_button_state(hex_state) {
        $.ajax({
            url: "webpower/set/" + hex_state,
            success: function() {
                console.log("sent: " + hex_state)
            },
        });
    }
    function handleOutletState(data) {
       var outlets_states = data;
       var outlets = [];
       console.log("inside post processing");
       for (i = 0; i < outlets_states.length; i++) { 
            console.log("inside loop");
            outlet_i = i+1;
            outlets[i] = $("#outlet" + outlet_i);

            //Set state to reflect current state
            if (outlets_states[i] === true){
                console.log("think its true");
                console.log(outlets[i]);
                outlets[i].addClass("active").attr("aria-pressed", "true")
            }
            else if (outlets_states[i] === false){
                console.log("think its false");
                console.log(outlets[i]);
                outlets[i].removeClass("active").attr("aria-pressed", "false")
            }

        }
    return(outlets);
    }

    getValues();
    function getValues(){
         $.ajax({
            url: 'webpower/',
            type: 'get',
            dataType: 'json',
            cache: false,
            success: handleOutletState,
            async:true,
            });
    };
})



