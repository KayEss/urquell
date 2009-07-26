

lurquell = new function () {
    /*
        Detects whether or not we're in a wave
    */
    in_wave = function() {
        try {
            return wave && wave.isInWaveContainer();
        } catch (e) {
            return false;
        }
    }();
    /*
        Builds the select box for a single level. This only works for modules as functions must be handled differently.
    */
    function level_builder(json, level) {
        function option_builder(name, is_function) {
            return $('<option value="' + name + '" class="' + (is_function ? 'function' : 'module') + '">').text(name)
        }
        var opts = $('<select id="urquell_select_' + level + '">').append(
            $('<option value="">').text( level ? "<null>" : "")
        );
        for (var o in json.value.modules)
            opts = opts.append(option_builder(json.value.modules[o].name, false))
        return opts;
    }
    /*
        Takes a div ID and returns the newly empty div
    */
    function replace_content(id) {
        var inner_div = $('<div id="' + id + '">');
        $('#' + id).replaceWith(inner_div);
        return inner_div;
    }
    /*
        Shows a command and its current status in the status bar
    */
    function status_text(command, status) {
        var content = replace_content('urquell_status');
        if ( !this.in_wave )
            content = content.append(
                $('<b>').text("Not in wave -- ")
            )
        return content.append(
            $('<span>').text(command)
        ).append(
            $('<span>').text(' -- ')
        ).append(
            $('<b>').text(status)
        );
    }
    /*
        Execute the provided Urquell command. The command executes asynchronously.
    */
    function execute_command(command, lambda) {
        status_text(command, "starting");
        $.getJSON(command+'?__=?', function(json) {
            status_text(command, "complete");
            return lambda(json);
        });
    }
    /*
        Called to reset the gadget for the beginning of a line
    */
    this.start_line = function () {
        execute_command("http://urquell-fn.appspot.com/", function(json) {
            $('#urquell_builder').replaceWith(
                $('<div id="urquell_builder">').append(
                    $('<span id="urquell_server"></span>').text("http://urquell-fn.appspot.com/")
                ).append(
                    level_builder(json, 0)
                ).append(
                    $('<input type="text" name="path">')
                ).append(
                    $('<input type="submit" value="Execute">')
                )
            );
        });
    }
    return this;
}

$('#urquell_builder').text("Gadget loaded. Requesting information from the Urquell server. Please wait...");

lurquell.start_line();
