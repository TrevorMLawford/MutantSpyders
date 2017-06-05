# MutantSpyders
Python port of Mutant Xpiders - also runs on Raspberry Pi (easily inside RetroPie)

A simple arcade-style game ("Mutant Spyders") written in Python/Pygame which morphed into a project to implement realistic AI.
The conditions are that the AI can only see what's strictly on-screen, and movement & fire are goverened by the same rules as would apply to a real player. In other words the AI has no 'special' abilities!

As you can see on the title screen there are many variables to adjust - and it can become insane (where the AI has NO chance). I'll post some more examples later.

The display shows some deliberate visual artifacts illustrating how the AI 'thinks', according to 9 vertical screen divisions. Danger areas are shown in Red (the brighter the more dangerous), the Green lines show where potential targets are (longer line = more targets) and the Yellow line shows the next intended target location for the ship to move (whilst avoiding the Reds).

This isn't any kind of Neural Network self-learning thing. It's 'just' programming - trying to play by the rules and to look as if it *could* be a human.

It also runs nicely on a Raspberry Pi 3 (and in a Picade, which I thoroughy recommend)
