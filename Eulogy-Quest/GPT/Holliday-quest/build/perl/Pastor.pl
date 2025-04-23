sub EVENT_SAY {
    if ($text=~/hail/i) { quest::say("Greetings $name! Blood dries. But memory stains forever. Are you here to [" . quest::saylink("carry the burden of mercy") . "]?"); }
    if ($text=~/carry the burden of mercy/i) { quest::say("Doc gave me the cloth after his last confession. A [" . quest::saylink("grieving squire") . "] snatched it from the altar, claiming absolution."); }
    if ($text=~/grieving squire/i) { quest::say("He kneels beside the fountain. Whispers names no one remembers. Don’t wake him — he weeps in cycles."); }
}

sub EVENT_ITEM {
    quest::say("It still smells of whiskey and iron. I never found peace in it.");
    quest::say("May it rest with him, not me. I’ve recited its weight too long.");
    quest::say("Seek Sylas Wren in Lavastorm. If anyone kept Doc’s pain hot, it was him.");
}
