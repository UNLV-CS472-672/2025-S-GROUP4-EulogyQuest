sub EVENT_SAY {
    if ($text=~/hail/i) { quest::say("Did the wind tell you I was here? Or did you [" . quest::saylink("feel the weight of the wager") . "]?"); }
    if ($text=~/feel the weight of the wager/i) { quest::say("The past don’t rest. It shuffles and draws. Four souls carry my echoes — [" . quest::saylink("Ada") . "], [" . quest::saylink("Dunne") . "], [" . quest::saylink("Crowley") . "], and [" . quest::saylink("Wren") . "]."); }
    if ($text=~/Ada/i) { quest::say("She still holds the chip I never folded. It should’ve stayed buried."); quest::say("Start with Ada Larkin in South Karana. She still guards the bet I never claimed."); }
}

sub EVENT_ITEM {
    quest::say("The hands were always stacked, but you played ‘em fair. You brought back the parts I lost — not to the law, but to me.");
}
