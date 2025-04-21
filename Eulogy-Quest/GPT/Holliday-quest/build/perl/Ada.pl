sub EVENT_SAY {
    if ($text=~/hail/i) { quest::say("Greetings $name! The bet was placed before you were born, stranger. You here to [" . quest::saylink("settle old scores") . "]?"); }
    if ($text=~/settle old scores/i) { quest::say("Doc tossed his chip to me the night before the shooting. Said he didn’t plan to use it. A [" . quest::saylink("weeping outlaw") . "] stole it from my hand before dawn."); }
    if ($text=~/weeping outlaw/i) { quest::say("He camps near the jagged stones by the southern trail — sobbing into a flask. He won’t fight. But he won’t give it up easy either."); }
}

sub EVENT_ITEM {
    quest::say("Still warm with memory… and regret.");
    quest::say("I held it long enough. Let it jingle in his pocket again.");
    quest::say("You’ll find Dunne behind the Freeport saloon. He still limps from the deal he broke.");
}
