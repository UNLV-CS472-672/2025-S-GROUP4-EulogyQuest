sub EVENT_SAY {
 if ($text=~/hail/i) {
     quest::say("Beep Boop!");
     quest::popup("Test", "Welcome to the test window! Enjoy your stay.");
 }
}
