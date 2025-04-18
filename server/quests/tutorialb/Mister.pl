sub EVENT_SAY {
    if ($text=~/hail/i) { quest::say("Greetings $name! I never bent the truth — just curved it where I needed. You come to [" . quest::saylink("reclaim what cracked") . "]?"); }
    if ($text=~/reclaim what cracked/i) { quest::say("The cane snapped when the shots rang out. A [" . quest::saylink("smiling enforcer") . "] pocketed the handle, said it brought him luck."); }
    if ($text=~/smiling enforcer/i) { quest::say("He struts near the boardwalk, tossing it end over end. His kind always grins before they draw."); }
}

sub EVENT_ITEM {
    quest::say("He said it whispered Doc’s last breath. I just remember the splinters.");
    quest::say("Let him have it back. And may it jab his heel for every lie I told.");
    quest::say("Look for Pastor Crowley in Qeynos. He never forgave Doc’s sins — or his own.");
}
