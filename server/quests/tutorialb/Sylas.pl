sub EVENT_SAY {
    if ($text=~/hail/i) { quest::say("Greetings $name! Heat tempers steel. And men. What you holding — truth or myth? Ready to [" . quest::saylink("pull the tooth") . "]?"); }
    if ($text=~/pull the tooth/i) { quest::say("Doc left his forceps here after cauterizing a wound. A [" . quest::saylink("burned rogue") . "] claimed it was blessed and fled into the fire."); }
    if ($text=~/burned rogue/i) { quest::say("She dances near the brimstone spires, wrapped in ash and ash alone. Trick is, she never stops moving."); }
}

sub EVENT_ITEM {
    quest::say("Still gleam through the soot. Still bite when clenched.");
    quest::say("He carved more than teeth with these. Give ‘em back to the only hand steady enough to wield ‘em.");
    quest::say("Return to Holliday’s ghost in North Ro. You’ve done the rounds. The deck is full.");
}
