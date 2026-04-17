import pathlib

EDITS_EN = [
    # --- AFFECTION ---
    ('en/needs/affection.html',
     "Receiving love is practised, just as much as giving it — often it is even the harder of the two.</li>",
     "Receiving love is practised, just as much as giving it — often it is even the harder of the two <em>(e.g. letting a compliment land without brushing it off, or letting someone help us without rushing to pay them back)</em>.</li>"),
    ('en/needs/affection.html',
     'even though one sees many people.<a class="ref-anchor"',
     'even though one sees many people <em>(e.g. coming home from a lively evening with the sense of an inner absence, as if no one really saw us)</em>.<a class="ref-anchor"'),
    ('en/needs/affection.html',
     "screens everywhere, attention constantly interrupted.</li>",
     "screens everywhere, attention constantly interrupted <em>(e.g. leaving the phone in another room during a visit)</em>.</li>"),

    # --- UNDERSTANDING (compréhension) ---
    ('en/needs/understanding.html',
     'Putting everything off</strong>, becoming unable to decide.<a class="ref-anchor"',
     'Putting everything off</strong>, becoming unable to decide <em>(e.g. scrolling through online courses for weeks without ever enrolling in one)</em>.<a class="ref-anchor"'),
    ('en/needs/understanding.html',
     'This "just right" zone is narrow and shifts over time.<a class="ref-anchor"',
     'This "just right" zone is narrow and shifts over time <em>(e.g. learning a piece a notch above your current level, rather than the virtuoso piece that makes you quit at the first bar)</em>.<a class="ref-anchor"'),
    ('en/needs/understanding.html',
     "Believing you must wait for motivation to start. Motivation tends to come in action, rarely before.</li>",
     "Believing you must wait for motivation to start <em>(e.g. telling yourself \"I'll get to it once I'm ready\", while five clumsy minutes would be enough to get the wheel turning)</em>. Motivation tends to come in action, rarely before.</li>"),

    # --- CREATION ---
    ('en/needs/creation.html',
     "Creating is worth practising even without recognised talent — the value lies in the act, not in how it will be received.</li>",
     "Creating is worth practising even without recognised talent — the value lies in the act, not in how it will be received <em>(e.g. keeping a notebook no one will see, or improvising on the piano without an audience)</em>.</li>"),
    ('en/needs/creation.html',
     "deep boredom even in a life that is objectively full.</li>",
     "deep boredom even in a life that is objectively full <em>(e.g. a smooth and outwardly successful life, with the vague sense that \"it isn't really me living it\")</em>.</li>"),
    ('en/needs/creation.html',
     "<strong>external metrics</strong> — likes, sales, algorithms.</li>",
     "<strong>external metrics</strong> — likes, sales, algorithms <em>(e.g. only posting a photo if it is likely to \"do well\", until you forget why you took it)</em>.</li>"),

    # --- IDENTITY ---
    ('en/needs/identity.html',
     "especially after a loss or a big achievement.</li>",
     "especially after a loss or a big achievement <em>(e.g. landing the dream job and no longer knowing who you are without that project, or losing a loved one and feeling a part of yourself disappear with them)</em>.</li>"),
    ('en/needs/identity.html',
     '(from family, society). Clarifying values is a well-studied lever.<a class="ref-anchor"',
     '(from family, society) <em>(e.g. asking whether "being successful" still matters once you mute the family voice that keeps repeating it)</em>. Clarifying values is a well-studied lever.<a class="ref-anchor"'),
    ('en/needs/identity.html',
     "Showy purchases as a signal of who we are — we end up defining ourselves by what we own.</li>",
     "Showy purchases as a signal of who we are — we end up defining ourselves by what we own <em>(e.g. piling up visible labels so others can \"guess\" who we are)</em>.</li>"),

    # --- FREEDOM (liberté) ---
    ('en/needs/freedom.html',
     "Inner freedom is built through small decisions repeated over time, not through one great leap.</li>",
     "Inner freedom is built through small decisions repeated over time, not through one great leap <em>(e.g. starting by saying no to a drink you don't want, then to a meeting that doesn't concern you, then to a project you didn't really choose)</em>.</li>"),
    ('en/needs/freedom.html',
     "<strong>deciding on your own</strong>, even for minor choices, without seeking someone else's approval.</li>",
     "<strong>deciding on your own</strong>, even for minor choices, without seeking someone else's approval <em>(e.g. hesitating between two dishes at a restaurant until you have asked everyone at the table)</em>.</li>"),
    ('en/needs/freedom.html',
     "<strong>deciding more and more on your own</strong> — start with small things.</li>",
     "<strong>deciding more and more on your own</strong> — start with small things <em>(e.g. planning your weekend without asking anyone, then your next holiday, then a change of life without waiting for permission)</em>.</li>"),

    # --- LEISURE (loisir) ---
    ('en/needs/leisure.html',
     "<strong>Guilt</strong> the moment you stop — rest itself becomes a performance.</li>",
     "<strong>Guilt</strong> the moment you stop — rest itself becomes a performance <em>(e.g. running through the to-do list in bed on Sunday morning, or \"just checking\" work email on holiday)</em>.</li>"),
    ('en/needs/leisure.html',
     'from work outside hours — beyond simply being physically absent.<a class="ref-anchor"',
     'from work outside hours — beyond simply being physically absent <em>(e.g. not opening your laptop on a day off, even "just five minutes")</em>.<a class="ref-anchor"'),
    ('en/needs/leisure.html',
     "<strong>Over-planned holidays</strong> that leave no real room to unwind.</li>",
     "<strong>Over-planned holidays</strong> that leave no real room to unwind <em>(e.g. ticking off three countries in two weeks with a to-do list of monuments to see)</em>.</li>"),

    # --- PARTICIPATION ---
    ('en/needs/participation.html',
     'Feeling <strong>useless</strong> and on the margin, even when surrounded by others.<a class="ref-anchor"',
     'Feeling <strong>useless</strong> and on the margin, even when surrounded by others <em>(e.g. at work or in the family, feeling that everything would keep running just the same without us)</em>.<a class="ref-anchor"'),
    ('en/needs/participation.html',
     "Choose a commitment that matches your <strong>core values</strong>, not just any engagement.</li>",
     "Choose a commitment that matches your <strong>core values</strong>, not just any engagement <em>(e.g. giving time to a cause that genuinely moves you, rather than to whichever one is in the news that week)</em>.</li>"),
    ('en/needs/participation.html',
     "<strong>Passive online belonging</strong>: consuming without ever giving anything back.</li>",
     "<strong>Passive online belonging</strong>: consuming without ever giving anything back <em>(e.g. being a member of dozens of online groups without ever having posted a single message)</em>.</li>"),

    # --- PROTECTION ---
    ('en/needs/protection.html',
     "<strong>Feeling on alert all the time</strong>, even when the situation is objectively safe.</li>",
     "<strong>Feeling on alert all the time</strong>, even when the situation is objectively safe <em>(e.g. flinching at the smallest noise at home, staying \"on watch\" even on a Sunday with nothing planned)</em>.</li>"),
    ('en/needs/protection.html',
     "<strong>regular routines</strong> (hours, places, small rituals) that create an inner sense of safety.</li>",
     "<strong>regular routines</strong> (hours, places, small rituals) that create an inner sense of safety <em>(e.g. the same wake-up, the same breakfast, the same morning commute)</em>.</li>"),
    ('en/needs/protection.html',
     "<strong>asking, receiving, leaning</strong> on others when needed — that is a sign of maturity, not weakness.</li>",
     "<strong>asking, receiving, leaning</strong> on others when needed — that is a sign of maturity, not weakness <em>(e.g. letting a friend help carry a box at moving day, or admitting you need professional support without treating it as a defeat)</em>.</li>"),

    # --- SUBSISTENCE ---
    ('en/needs/subsistence.html',
     "<strong>Lasting fatigue</strong> that rest does not erase.</li>",
     "<strong>Lasting fatigue</strong> that rest does not erase <em>(e.g. sleeping twelve hours on a Saturday and waking up just as drained)</em>.</li>"),
    ('en/needs/subsistence.html',
     "Constantly tracking one's own data (steps, sleep, heart rate) like a dashboard. The body becomes an object to optimise, and life retreats.</li>",
     "Constantly tracking one's own data (steps, sleep, heart rate) like a dashboard <em>(e.g. checking step or sleep stats ten times a day, until measurement replaces the felt sense)</em>. The body becomes an object to optimise, and life retreats.</li>"),
]

miss, ok = 0, 0
for path, old, new in EDITS_EN:
    p = pathlib.Path(path)
    text = p.read_text(encoding='utf-8')
    if old not in text:
        print(f'MISS: {path} :: {old[:70]}')
        miss += 1
        continue
    p.write_text(text.replace(old, new, 1), encoding='utf-8')
    ok += 1
    print(f'OK:   {path} :: {old[:70]}')

print(f'\n{ok} applied, {miss} missed')
