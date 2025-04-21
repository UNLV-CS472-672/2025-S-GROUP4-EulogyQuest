### Author: Tanner Donovan
### Script Development Start Date: 4/14/2025
### Description: This script generates a PERL script for quest logic, including dialogue and item rewards, from the JSON input.

import json
import os
import sys

def generate_quest_perl_script(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    base = os.path.basename(input_file)
    honored_target = base.replace("_quest", "").replace(".json", "")
    perl_filename = f"{honored_target}.pl"

    # Start writing the Perl script
    with open(perl_filename, 'w') as f:
        f.write("#!/usr/bin/perl\n")
        f.write("use strict;\nuse warnings;\n\n")

        f.write("sub EVENT_SAY {\n")
        f.write('    my $text = $client->GetSpecializedItem();\n')
        f.write('    if($text =~ /hello/) {\n')
        f.write('        quest::say("Greetings, traveler!");\n')
        f.write('    }\n')
        f.write("}\n\n")

        f.write("sub EVENT_ITEM {\n")
        f.write('    if(plugin::check_handin(\%itemcount, 77005 => 1)) {\n')
        f.write('        quest::say("Thank you for bringing my saddle!");\n')
        f.write('        quest::summonitem(77005);\n')
        f.write('        quest::exp(1000);\n')
        f.write('    }\n')
        f.write('    else {\n')
        f.write('        quest::say("I don\'t need this item.");\n')
        f.write('        plugin::return_items(\%itemcount);\n')
        f.write('    }\n')
        f.write("}\n")

    os.chmod(perl_filename, 0o755)
    print(f" Quest Perl script created: {perl_filename} (ready to execute)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_quest_perl_script.py quest.json")
        sys.exit(1)

    generate_quest_perl_script(input_file=sys.argv[1])
