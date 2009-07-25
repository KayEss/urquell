
lurquell = function () {
    $('#lurquell').text("Gadget loaded. Requesting information from the Urquell server. Please wait...");

    function start_line() {
        $.getJSON("http://urquell-fn.appspot.com/?__=?", function(json) {
            $('#lurquell').replaceWith(
                $('<div id="urquell">').append(
                    $('<span id="urquell_server"></span>').text("http://urquell-fn.appspot.com/")
                ).append(
                    $("<select>").append(
                        $('<option value="">').text("")
                    ).append(
                        $('<option value="null">').text("<null>")
                    )
                ).append(
                    $('<input type="text" name="path">')
                ).append(
                    $('<input type="submit" value="Execute">')
                )
            );
        })
    }

    start_line();
}

lurquell();
