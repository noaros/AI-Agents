# AI-Agents

Time to give myself a crash course in building AI agents!

[This Claude training](https://academy.claude.com/courses/building-with-the-claude-api) seems like a good place to start.

I hit a snag where the tutorial was obsolete. I changed to a newer Claude model, but that caused another problem because now "thinking blocks" and not just "text" blocks were in the mix, breaking the sample code. Hilariously and very meta, I let Claude itself fix the Claude tutorial, and it worked! Time to study what it did...

The tutorial describes a hacky message prefill and stop sequence technique, but this is no longer the way to do things for new models. I implemented the structured output method instead. I also filled in a missing function and corrected some names in the "prompt eval" section.
