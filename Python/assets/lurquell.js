
lurquell = function () {
    $('#lurquell').text("Gadget loaded. Requesting information from the Urquell server. Please wait...");

    function option_builder(name) {
        return $('<option value="' + name + '">').text(name)
    }

    function start_line() {
        $.getJSON("http://urquell-fn.appspot.com/?__=?", function(json) {
            $('#lurquell').replaceWith(
                $('<div id="urquell">').append(
                    $('<span id="urquell_server"></span>').text("http://urquell-fn.appspot.com/")
                ).append(
                    function(level) {
                        var opts = $('<select id="urquell_select_' + level + '">').append(
                            $('<option value="">').text( level ? "<null>" : "")
                        );
                        for ( var o in json.value.modules )
                            opts = opts.append(option_builder(json.value.modules[o].name))
                        return opts;
                    }(0)
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
