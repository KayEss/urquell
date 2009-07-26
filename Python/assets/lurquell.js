
$('#lurquell').text("Gadget loaded. Requesting information from the Urquell server. Please wait...");

lurquell = new function () {
    /*
        Builds the select box for a single level. This only works for modules.
    */
    function level_builder(json, level) {
        function option_builder(name) {
            return $('<option value="' + name + '">').text(name)
        }
        var opts = $('<select id="urquell_select_' + level + '">').append(
            $('<option value="">').text( level ? "<null>" : "")
        );
        for ( var o in json.value.modules )
            opts = opts.append(option_builder(json.value.modules[o].name))
        return opts;
    }
    /*
        Called to reset the gadget for the beginning of a line
    */
    this.start_line = function () {
        $.getJSON("http://urquell-fn.appspot.com/?__=?", function(json) {
            $('#lurquell').replaceWith(
                $('<div id="urquell">').append(
                    $('<span id="urquell_server"></span>').text("http://urquell-fn.appspot.com/")
                ).append(
                    level_builder(json, 0)
                ).append(
                    $('<input type="text" name="path">')
                ).append(
                    $('<input type="submit" value="Execute">')
                )
            );
        })
    }
    return this;
}

lurquell.start_line();
