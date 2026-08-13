"""Generate the four anxiety-journal interior PDFs (books #2-#5).

Each book uses the shared 108-page template in template.py, with title-specific
prompts, exercises, and framing that keep them from competing on the same
keywords.
"""

from __future__ import annotations

from pathlib import Path

from template import BookConfig, build_book

OUT_DIR = Path(__file__).parent / "out"


BOOK_2 = BookConfig(
    slug="overthinker",
    title="The Overthinker's Journal",
    subtitle="A Teen Guide to Quieting a Racing Mind",
    dedication="For anyone whose brain refuses to close its tabs.",
    tracker_focus="racing-thought episodes",
    section1_intro="Get the loop out of your head and onto the page.",
    prompts=[
        "What thought have you been on a loop with today? Write it out until it runs out.",
        "If your mind is a browser, how many tabs are open right now? Name them.",
        "Which of your worries have you already thought about more than once this week?",
        "What is a decision you've been re-deciding? What would 'good enough' look like?",
        "Write down the worst-case scenario in full. Now write how you'd actually handle it.",
        "What are you overthinking because you care? What are you overthinking out of fear?",
        "Finish this: 'I keep thinking about it because...'",
        "Which of your worries are you actually solving, and which are you just circling?",
        "Write down every 'what if.' Then, next to each, write 'and then what?'",
        "What conversation are you rehearsing in your head? Write the version you'd actually say.",
        "What is one thing you cannot know right now, no matter how long you think about it?",
        "What would it feel like to be done thinking about this for tonight?",
        "Whose voice is loudest in your head when you spiral? Is it yours?",
        "What's the story your brain keeps telling? What's a truer, kinder version?",
        "What is a small action that would move this forward more than more thinking?",
        "Write the message you want to send, but don't send it. What did you learn?",
        "Where do you feel the overthinking in your body? What do you notice?",
        "What is the thing you're afraid to decide? Set a deadline for the decision.",
        "What would you tell a friend who was thinking about this as hard as you are?",
        "What has your overthinking never once solved for you? What has it cost?",
        "What is one worry you can hand off — to tomorrow, to a friend, to no one at all?",
        "Write down three worries. Rate each 1-10 for 'how likely is this, really?'",
        "What would you do next if you trusted yourself to figure it out along the way?",
        "What is a decision past-you made that turned out fine? How did that feel then?",
        "What if the thing you're worried about isn't actually the point?",
        "What is the smallest thing you could do right now to interrupt the loop?",
        "What thought are you ready to be done with, at least for tonight?",
        "Write about a time your overthinking was wrong. What actually happened?",
        "Finish this: 'The version of me that isn't overthinking would...'",
        "What does 'done thinking about it' look like tonight? Write yourself permission.",
    ],
    exercises=[
        ("Close the tabs", "List every open worry in your head like browser tabs. Star the "
         "ones worth keeping open. Close the rest by writing 'not today' next to them."),
        ("The 10-10-10", "Ask: Will this matter in 10 minutes? In 10 months? In 10 years? "
         "Write your honest answer to each. Notice how the size of the worry shifts."),
        ("Worry window", "Give yourself a 15-minute worry window. Set a timer. Write down "
         "everything your brain wants to worry about. When the timer ends, close the book."),
        ("Name the loop", "Write the exact sentence your brain is stuck on. Read it out "
         "loud three times. Ask: is this a fact, a fear, or a story?"),
        ("The next tiny step", "You do not need the whole plan. Write the single smallest "
         "next action. Do that. Come back to this page after."),
        ("Reframe it", "Write the anxious thought at the top. Underneath, write what you "
         "would tell a friend who said this to you. Notice the tone difference."),
        ("Park it for tonight", "Write your worry on a page. Close the book. Tell yourself: "
         "'It will still be here in the morning if I need it.' Try to leave it here."),
        ("What I can control", "Draw a small circle inside a bigger one. Small circle: "
         "what you can actually do. Big circle: what's outside your reach. Keep your "
         "attention in the small circle."),
        ("The 5-minute rule", "Pick the thing you've been avoiding by overthinking it. "
         "Set a timer for 5 minutes and start. Then stop. Write about what came up."),
        ("Body first", "Overthinking is often a signal that your body needs something. "
         "Drink water, eat, move for five minutes, or step outside. Then check in."),
    ],
    affirmations_seed=[
        "I do not have to solve every thought.",
        "Not deciding is also a decision I can rest in.",
        "One clear next step is enough.",
        "My worry is not my future.",
        "I can put this down for tonight.",
        "I trust myself to figure it out as it comes.",
        "Overthinking is not the same as caring.",
        "I am allowed to close the tabs.",
    ],
)


BOOK_3 = BookConfig(
    slug="before_the_test",
    title="Before the Test",
    subtitle="A Teen's Journal for School & Study Anxiety",
    dedication="For anyone who has ever cried over a study guide.",
    tracker_focus="test and school stress",
    section1_intro="For the hour before, the night before, and every ordinary school day.",
    prompts=[
        "What test or assignment is on your mind right now? Write it out in one sentence.",
        "What are you actually afraid will happen if this doesn't go well?",
        "Whose voice is in your head about grades — a parent, a teacher, yourself? What are they saying?",
        "Write down every step you'd need to feel prepared. Circle the next one.",
        "What is one thing you know really well already? Remind yourself.",
        "What subject makes your chest tight? What is one small thing that helps?",
        "What does 'doing your best' actually mean, in your own words?",
        "What would you tell a classmate who felt the way you feel about this test?",
        "What is the story you tell yourself about being 'smart'? Is it fully true?",
        "Write about a time you were scared you'd fail and didn't. How did you get through it?",
        "What is one thing outside of school that you're good at? How did you get good at it?",
        "What do you need before a test to feel steady? Food? Sleep? Quiet? Music?",
        "What is your morning-of routine on a test day? What would you want it to be?",
        "What are you comparing yourself to? Is that comparison fair to you?",
        "What subject do you actually enjoy? What does your body feel like in that class?",
        "What grade would be 'enough' for you on this? Not perfect — enough.",
        "What is one hard question you don't understand yet? Who could you ask?",
        "What would this test feel like if you weren't afraid of it? Describe it.",
        "What are three things you did this week that were harder than this test?",
        "What does your teacher not know about how much effort this has taken?",
        "What is one small kindness you can do for yourself the night before?",
        "What would 'over-preparing' look like? What would 'good-enough preparing' look like?",
        "What are you afraid people will think of you? What would you think of them?",
        "Write down what your anxiety is predicting will happen. Rate it 1-10 for likely.",
        "What would you do this week if grades didn't exist for a moment?",
        "What is one thing you understand now that you didn't a month ago?",
        "What is a lie your anxiety tells you before a test? Write the truth next to it.",
        "What are you going to do the moment the test is over, no matter how it went?",
        "Finish this: 'Even if this doesn't go well, I still...'",
        "Write yourself a permission slip: 'I am allowed to...' during this test week.",
    ],
    exercises=[
        ("Study block plan", "Break the material into small chunks. Write each chunk on a "
         "line, with the smallest possible task next to it. One chunk = one line."),
        ("The night-before wind-down", "List three things to do the night before that are "
         "NOT studying: shower, snack, playlist, whatever calms you. Commit to them."),
        ("Rehearse the room", "Close your eyes. Picture walking in, sitting down, taking a "
         "breath, and starting. Write what you see. Rehearsing calm counts as studying."),
        ("The 'if I blank' plan", "Write down what you'll do if your mind goes blank mid-test: "
         "breathe, skip and come back, re-read the question, next question. Have a plan."),
        ("Fear vs. fact", "On the left, write what your anxiety predicts. On the right, "
         "write what is actually true about this test. Compare them."),
        ("Effort inventory", "Write down every hour you've already put into this material. "
         "Notice how much you've already done."),
        ("The 5-minute reset", "Halfway through a study session, set a 5-minute timer. Stand "
         "up. Water. Stretch. Look out a window. Then come back."),
        ("Reframe 'I don't get it'", "Change every 'I don't get it' to 'I don't get it YET.' "
         "Write down what specifically you don't get. That's your next study step."),
        ("Ask-for-help list", "Write three questions you could bring to a teacher, tutor, "
         "or classmate. Pick one to actually send this week."),
        ("The after-test kindness", "Plan one small good thing for right after the test — "
         "no matter how it went. Snack, walk, playlist, nap. Commit to it now."),
    ],
    affirmations_seed=[
        "My grade is not my worth.",
        "I have prepared. I can trust that.",
        "One question at a time.",
        "It is okay to not know something yet.",
        "I am allowed to ask for help.",
        "Breathing is a study skill.",
        "Doing my best is not the same as being perfect.",
        "This test does not define me.",
    ],
)


BOOK_4 = BookConfig(
    slug="say_it_anyway",
    title="Say It Anyway",
    subtitle="A Teen Journal for Social Anxiety & Shyness",
    dedication="For everyone who has ever rehearsed a hello.",
    tracker_focus="social situations",
    section1_intro="Small pages for the moments before you speak.",
    prompts=[
        "What social situation is on your mind right now? Describe it in detail.",
        "What are you afraid people will think of you? What's the story you tell yourself?",
        "Write out a conversation you're rehearsing. What are you afraid they'll say?",
        "What did you almost say today but didn't? What would have happened if you had?",
        "Who feels easy to be around? What is it about them that makes it easy?",
        "What is a compliment you've never known how to accept? Try accepting it here.",
        "Describe your ideal version of a party or gathering. Who's there? What do you do?",
        "What is one small social risk you could take this week? What's the smallest version of it?",
        "Write about a time you felt awkward and everyone survived. What actually happened?",
        "What do you wish people knew about you that they usually don't?",
        "What does small talk feel like in your body? What do you wish you could say instead?",
        "Who would you like to know better? What is one question you could ask them?",
        "What is a friendship you'd like to build or repair? What's the first small move?",
        "What do you assume other people are thinking about you? Are you sure?",
        "Write about someone who made you feel seen. What did they do, exactly?",
        "What is a group you feel out of place in? Is that group actually the wrong fit?",
        "What is one thing you like about how you show up around other people?",
        "What would you say if you weren't worried about how it sounded?",
        "What is a memory of you being funny, warm, or interesting that you tend to dismiss?",
        "Who would be lucky to have you as a friend? What would you bring to that friendship?",
        "What are you tired of pretending to feel around other people?",
        "What is the most exhausting kind of social situation for you? Why?",
        "What is a text you've been meaning to send? Draft it here. Then decide.",
        "Write about a time you set a boundary. How did it feel? What happened?",
        "What would you do at lunch this week if you weren't worried about looking alone?",
        "Who are you around when you feel most like yourself? What are you doing?",
        "What is one hard thing you want to say to someone? Practice it here.",
        "What does 'good enough' look like for a conversation? Not perfect. Just good enough.",
        "Finish this: 'The version of me who isn't anxious around people would...'",
        "Write yourself permission to leave early, be quiet, or say no this week.",
    ],
    exercises=[
        ("The 3-second opener", "Write down three low-pressure openers you could actually "
         "use this week: 'Hey.' 'How's your week going?' 'What did you think of...?' Pick one."),
        ("Rehearse the exit", "Write your polite exit line. 'I've got to head out — good "
         "seeing you.' Practice having it ready so leaving feels like a plan, not a panic."),
        ("Reframe the mind-read", "Write down what you assume someone is thinking about you. "
         "Then write three other explanations for what they might actually be thinking."),
        ("The tiny risk", "Pick one social risk this week that's a 2/10, not a 9/10. Wave. "
         "Compliment. Ask a small question. Write which one and when."),
        ("Post-mortem, kindly", "After a hard social moment, write what happened. Then write "
         "what you'd tell a friend who described this exact same moment to you."),
        ("The 'me too' list", "Write down every awkward thing you're sure only you feel. "
         "Realize most people feel these. Circle the ones a friend has also mentioned."),
        ("Ask a question", "The easiest thing to say in a hard conversation is a real "
         "question. Write three questions you could ask someone this week."),
        ("Boundary draft", "Draft a boundary you want to set. Short, kind, clear. 'I can't "
         "tonight.' 'I need to head home.' 'Please don't joke about that.' Practice it."),
        ("The exit plan", "Before a social event, write down: when you'll leave, how you'll "
         "get home, and what you'll do to recover after. Plans make it possible to go."),
        ("Small brag", "Write down one thing you did socially this week that took courage — "
         "however small. Waving. Sending the text. Sitting with someone. That counts."),
    ],
    affirmations_seed=[
        "I am not everyone's cup of tea, and that is okay.",
        "Being quiet is not the same as being wrong.",
        "One warm sentence is enough.",
        "I can leave when I need to.",
        "I do not have to earn my place at the table.",
        "People are thinking about themselves, not me.",
        "It is okay to take a while to open up.",
        "I am allowed to like who I like and skip who I don't.",
    ],
)


BOOK_5 = BookConfig(
    slug="three_am_thoughts",
    title="3 A.M. Thoughts",
    subtitle="A Teen Journal for Nighttime Worry & Sleep",
    dedication="For every worry that only shows up in the dark.",
    tracker_focus="sleep and nighttime worry",
    section1_intro="For the hours you are supposed to be sleeping.",
    prompts=[
        "What thought is keeping you up tonight? Write it out until it thins.",
        "What did today ask of you? Write it down, so you can put it here instead of in bed.",
        "What are you carrying into tonight that isn't yours to carry?",
        "What time did the worry start? What were you doing? What were you not doing?",
        "Write a list of everything on your mind. All of it. Then close the book.",
        "What does your body need right now that it isn't getting? Water, food, warmth, quiet?",
        "What are you telling yourself about not being able to sleep? Is that true?",
        "What is one thing you could do tomorrow instead of solving it tonight?",
        "What is your bed like right now — safe, tense, comforting? Describe it.",
        "What did today go right, even a little? Name three things.",
        "What conversation from today is looping? Write the ending you wish it had.",
        "What are you afraid of forgetting? Write it here so your brain can let it go.",
        "What are you grateful for tonight? Something small counts.",
        "What has your worry never actually solved at 3 a.m.? What has it cost you?",
        "What did you do today that was hard? Take a second to notice that.",
        "What is the story your brain is telling in the dark? Would you believe it in daylight?",
        "What would you tell yourself in six hours if you saw yourself wide awake now?",
        "What does 'a good enough night of sleep' look like tonight? Not perfect.",
        "What is one comfort you can bring into bed with you? Sound, scent, warmth, memory?",
        "What tomorrow-you problem is worrying you? Write a note to tomorrow-you about it.",
        "What are you missing tonight? Home, a person, a version of yourself?",
        "What is one thing you can let go of, just until morning?",
        "What is the sound of your room right now? What if you named it out loud?",
        "What is the loudest worry? Give it a name. Set it aside for the night.",
        "What is the last kind thing anyone said to you? Say it back to yourself.",
        "What did today teach you? Even one small thing.",
        "What are you refusing to feel that might be part of why you can't sleep?",
        "What is your morning going to need from you? Write it out, so you can rest.",
        "What is a memory of feeling safe? Bring yourself back to it now, slowly.",
        "Finish this: 'It is okay if tonight is not perfect. I can...'",
    ],
    exercises=[
        ("Worry parking", "Write every worry in your head on a page. Close the book. Tell "
         "yourself: 'It will still be here in the morning if I need it.' Then close your eyes."),
        ("The wind-down hour", "Design your last hour before bed. No screens? Warm shower? "
         "Herbal tea? Book? Write the plan here, then try it for a week."),
        ("4-7-8 breathing", "Breathe in for 4 counts. Hold for 7. Breathe out for 8. Repeat "
         "four cycles. This slows your nervous system on purpose."),
        ("Progressive muscle release", "Starting at your feet: squeeze the muscles for 5 "
         "seconds, then release. Move up your body — legs, belly, hands, jaw. Notice the drop."),
        ("Mental unpacking", "Say out loud (or write): 'Tomorrow I will handle X. Tomorrow "
         "I will handle Y.' Give your brain permission to hand things off to future-you."),
        ("The reset if you can't sleep", "If you're wide awake after 20 minutes, get up. "
         "Go to another room. Do something low-stakes. Come back when your body is heavier."),
        ("Safe-place visualization", "Bring a real or imagined safe place to mind. Water, "
         "trees, your childhood bedroom, whatever. Describe every sense: what you see, hear, smell."),
        ("The gratitude three", "Before your head hits the pillow, name three good things "
         "from today. Small counts. Toast that wasn't burnt counts."),
        ("Body scan for sleep", "Starting at the top of your head, notice each part of your "
         "body and let it soften. Forehead. Jaw. Shoulders. Chest. Belly. All the way down."),
        ("Note to tomorrow-you", "Write one sentence tomorrow-you needs to read first thing. "
         "Something honest and kind. Leave it on the nightstand."),
    ],
    affirmations_seed=[
        "I do not have to solve this tonight.",
        "Rest counts, even when I'm not asleep.",
        "The morning will meet me. I do not have to meet it early.",
        "It is okay to be awake right now.",
        "My body is doing its best.",
        "This thought can wait for daylight.",
        "I am safe in this bed.",
        "Tomorrow-me can handle tomorrow.",
    ],
)


ALL_BOOKS = [BOOK_2, BOOK_3, BOOK_4, BOOK_5]


def main() -> None:
    for cfg in ALL_BOOKS:
        path = build_book(cfg, OUT_DIR)
        print(f"  wrote {path.name}")


if __name__ == "__main__":
    main()
