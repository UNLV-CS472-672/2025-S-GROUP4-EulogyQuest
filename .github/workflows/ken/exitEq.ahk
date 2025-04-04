#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
; SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SendMode, Event

;// ai-gen start (ChatGPT-4o, 0)

; Bring EverQuest to the foreground
WinActivate, EverQuest
WinWaitActive, EverQuest
Sleep, 500

; Send /exit to trigger logout
Send, /exit
Send, {Enter}

;// ai-gen end
