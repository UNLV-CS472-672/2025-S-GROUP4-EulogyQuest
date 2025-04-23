# in perl syntax, @ preceeds arrays
# and             $ preceeds scalar variables (strings, numbers..

sub main {
    # @_ is array of passed arguments to the method (main in this case)
    # for this program, this is the json file and the NPCs quest file
    my ($json_file, $quest_file) = @_;

    # supplying the entire file path, later we might have to supply the region directory too
    my $gen_quest_file_path = "../server/quests/tutorialb/";
    my $full_quest_file_path = $gen_quest_file_path . $quest_file;

    my $gen_json_file_path = "./quest_json/";
    my $full_json_file_path = $gen_json_file_path . $json_file;

    # bit confusing, read_json is returning the json info as a reference to a hash
    # we then use $json_data->{element} to access elements
    # perl will treat a lot of empty scenarios as false
    my $json_data = read_json($full_json_file_path); 

    # terminate program with the error unless there is an event element in the json
    die "Error: 'event' field is empty in $json_file\n" unless $json_data->{event};
    
    # expand generate_code method to include more event support
    my $perl_code = generate_code($json_data);

    write_to_file($full_quest_file_path, $perl_code);

    print "$quest_file has been changed.\n";
}

sub read_json {
    # Casts the array of passed arguments (@_) into file
    # in this case the passed arg is a json file
    my ($json_file) = @_;

    # $file_stream is really a file handle in perl, but it is very similar to a file stream
    # '<' is for read only mode,
    open my $file_stream, '<', $json_file or die "Error opening '$json_file': $!";

    # Called "slurp" mode in perl, will read entire file into one string
    local $/;

    # since we enabled slurp mode, $json_text is now the enire json file in one string
    my $json_text = <$file_stream>;
    
    # done reading the file
    close $file_stream;

    # kind of like a local "import JSON", but it isn't loaded at compile time
    # so JSON is local to this scope.
    require JSON;

    # Uses the decode_json method on the string, which returns a hash 
    # that is almost identical to the original json, but perl accessable
    return JSON::decode_json($json_text);
}

# I added in this 'middle man' method so that support for different events and more can be added later. 
sub generate_code {
    my ($json_data) = @_;
    my $event_name = $json_data->{event}->{name};

    # EVENT_SAY event
    if ($event_name eq "EVENT_SAY") { 
        return generate_event_say_code($json_data);
        # Other events can go here later
    } else {
        die "Error: Unsupported event type '$event_name'.\n";
    }
}

sub generate_event_say_code{
	my ($data) = @_;
	my $texts = $data->{event}->{texts} // die "Error: Missing 'texts' key in 'event'";
	
	# There can be many triggers in an event, so we store them in an array
	die "Error: 'texts' must be an array" unless ref($texts) eq 'ARRAY';
	
	# perl method declaration
	my $perl_code = "sub EVENT_SAY {\n";
	
	# for each element in the array
	foreach my $entry (@$texts) {
	# the elements must contain triggers
	# only tested the hail trigger, more support needed
        my $trigger = $entry->{trigger} // die "Error: Missing 'trigger' key in texts";
        $perl_code .= " if (\$text=~/$trigger/i) {\n";
	
	# trigger a say
        if ($entry->{say}) {
            my $say = $entry->{say};
            $perl_code .= "     quest::say(\"$say\");\n";
        }
	
	# trigger a popup
        if ($entry->{popup}) {
            my $popup_name = $entry->{popup}->{name} // "DEFAULT";
            my $popup_body = $entry->{popup}->{body} // "";
            $perl_code .= "     quest::popup(\"$popup_name\", \"$popup_body\");\n";
        }
	
	# close the bracket for each element in array of texts
        $perl_code .= " }\n";
    }
	
    #close the bracket for the method EVENT_SAY	
    $perl_code .= "}\n";

    return $perl_code;
}

sub write_to_file{
    	my ($quest_file, $perl_code) = @_;

		# open file stream in write only mode or else throw an error
    		open my $file_stream, ">", $quest_file or die "Error opening '$quest_file': $!";
	
		# print the perl code into the file stream
    		print $file_stream $perl_code;
	
		# close file stream
    		close $file_stream;
}


eval{
	require JSON; 	# import JSON
	JSON->import(); # check if JSON was imported. Exits eval on failure
	1; 		# Set eval to true if we made it here
} or die "Error: The JSON perl module is not installed. Install it using 'sudo apt-get install libjson-perl'\n";

# if there aren't 2 command line arguments, exit with usage message
die "Usage: perl editNPC.pl <input File>.json <NPC File>.pl\n" unless @ARGV == 2;

# call to main passing command line arguments
main(@ARGV);
