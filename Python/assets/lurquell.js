
try {
    lurquell = function() {
        $('#lurquell').find('div').text("Gadget loaded. Requesting information from the Urquell server. Please wait... (you'll be waiting a long however as nothing is really happening)");

        function start_line() {
            $.getJSON("http://urquell-fn.appspot.com/?__=?", function(json) {
                    $('#lurquell').find('div').text("Got something, not sure what though");
                })
        }

        start_line();
    };
    lurquell();
} catch ( e ) {
    alert(e);
}
