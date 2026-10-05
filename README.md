# AI-Agents

Time to give myself a crash course in building AI agents!

[This Claude training](https://academy.claude.com/courses/building-with-the-claude-api) seems like a good place to start.

I hit a snag where the tutorial was obsolete. I changed to a newer Claude model, but that caused another problem because now "thinking blocks" and not just "text" blocks were in the mix, breaking the sample code. Hilariously and very meta, I let Claude itself fix the Claude tutorial, and it worked! Time to study what it did...

The tutorial describes a hacky message prefill and stop sequence technique, but this is no longer the way to do things for new models. I implemented the structured output method instead. I also filled in a missing function and corrected some names in the "prompt eval" section.

I found the training quite helpful. It was basic but covered a lot of different areas. I could tell it has been rewritten a lot, as it points things were incorrect or missing. Crucially it implied it provided some functions for what would have been code for an agent (though it didn't call it that yet_. but didn't actually provide the code. So as a tutorial to actually run and try out things it was lacking a bit. I think it was once a notebook with complete code, then morphed into its current form. But just a guess.

Only a few parts of the training covered agents, and not in a way as to actually provide an example. So of course I asked Claude Code. I am so amazed at what it can do. Completely in awe. I asked it to add a file showcasing a simple agent. It did so, including finding and activating my python environment, and even named the file in sequential order as '5.py'. I did ask it to do that, nor even say there was a pattern to be found! Nor would I even expect that to be a common filename pattern used by others. It also told me there was a way that uses an api call to handle the main agent loop, and showed me an example of rewriting the example to do just that, and offered to save it and run it for me.
