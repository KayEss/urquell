
try {
    lurquell = function() {
        $('#lurquell').find('div').text("Gadget loaded. Requesting information from the Urquell server. Please wait... (you'll be waiting a long however as nothing is really happening)");
    };
    lurquell();
} catch ( e ) {
    alert(e.description);
}
