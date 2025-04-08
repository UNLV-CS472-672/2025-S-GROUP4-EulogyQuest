#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
; SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SendMode, Event

;// ai-gen start (ChatGPT-4o, 1)

; === Make absolutely sure each keypress happens on the EverQuest-focuesd window
; === Windows loves stealing focus away.
FocusAndEnter() {
    WinActivate, EverQuest
    WinWaitActive, EverQuest
    Send, {Enter}
}
FocusAndTab() {
    WinActivate, EverQuest
    WinWaitActive, EverQuest
    Send, {Tab}
}


; ==== Everquest (eqemu) login automation for the Eulogy project ====
; == Part of my CI/CD pipeline work ==
; == Verifies whether the client can log in
; == after any changes are made to the repo

; === Config ===
;logPath := A_ScriptDir "\ahk-log.txt"
logPath := A_Desktop "\ahk-log.txt"
FileDelete, %logPath%
FileAppend, [%A_Now%] login.ahk started.`n`, %logPath%
FileAppend, Script directory: %A_ScriptDir%`n`, %logPath%
SetWorkingDir, C:\Eulogy-quest-client-local; Ensures a consistent starting directory.
password := "buzz9099e"
eqgameShortcut := "Eulogy-local.lnk"

; Launch game client with patchme
FileAppend, [%A_Now%] Launching EQ via shortcut: %eqgameShortcut%`n`, %logPath%
Run, %A_Desktop%\%eqgameShortcut%
FileAppend, [%A_Now%] eqgame shortcut launch executed.`n`, %logPath%

WinWaitActive, EverQuest

Sleep, 3000      ; Wait for EULA screen
FocusAndTab()    ; Tab away from "Decline" onto "Accept"

Sleep, 1000
FocusAndEnter()  ; Accept EULA

Sleep, 1000      ; wait for SOE splash screen
FocusAndEnter()  ; Dismiss SOE splash screen

Sleep, 1000      ; wait for login intro
FocusAndEnter()  ; Proceed past EQ intro screen

Sleep, 1000      ; wait for actual login screen
WinActivate, EverQuest
WinWaitActive, EverQuest
Send, %password%
Sleep, 500
FocusAndEnter()  ; Submit login password

Sleep, 1000
FocusAndEnter()  ; Select server

Sleep, 20000     ; Long wait just in case loading takes a long time
FocusAndEnter()  ; Log in with a character

;// ai-gen end
