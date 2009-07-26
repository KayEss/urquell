

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
        Builds the select box for a single level.
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
    this.execute = function() {
        var element = $('#urquell_path');
        var path = escape(element[0].value);
        for ( element = element.prev(); element[0].tagName.toLowerCase() == "select"; element = element.prev() )
            if (element[0].value)
                path = escape(element[0].value) + ( !path.length ? "" : "/" + path );
        if ( this.in_wave ) {
            // TODO Send this to the robot for evaluation
            alert("http://urquell-fn.appspot.com/" + path);
        } else
            alert("In a wave this would send the following to the robot for evaluation\nhttp://urquell-fn.appspot.com/" + path);
    }
    /*
        Called to reset the gadget for the beginning of a line
    */
    this.start_line = function () {
        execute_command("http://urquell-fn.appspot.com/", function(json) {
            replace_content('urquell_builder').append(
                $('<span id="urquell_server"></span>').text("http://urquell-fn.appspot.com/")
            ).append(
                level_builder(json, 0)
            ).append(
                $('<input type="text" id="urquell_path">')
            ).append(
                $('<input type="submit" value="Execute" onclick="lurquell.execute()">')
            )
        });
    }
    return this;
}

$('#urquell_builder').text("Gadget loaded. Requesting information from the Urquell server. Please wait...");

lurquell.start_line();
