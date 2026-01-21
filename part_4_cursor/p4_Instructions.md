# Part 4: Cyborg woman coding

This session has three parts.  

In the first part, Daniel will challenge you to a battle of wills.

In the next two parts, you will use **Cursor** as a learning partner: not just to write code, but to _explain unfamiliar codebases, help you plan changes, and reason about feasibility_.

You are not expected to already know how everything works.  

You _are_ expected to:

- ask clear questions,
- proceed in small steps,
- test often.

---

## Before Everything: Set Up Cursor (Very Important)

<span style="color: grey">(10-15 min - essential setup)</span>

### Goal

Configure Cursor so it knows:

- you are new to coding,
- you want **explicit explanations**, not shorthand,
- you want to learn _why_ things work, not just _what to type_.

### Step 1 — Open Cursor

Open Cursor and open **any folder** (it can be empty for now).

### Step 2 — Set the system instruction prompt

Find Cursor’s **instruction / system prompt** (sometimes called “Rules” or “Custom Instructions”).

Paste **this exactly**, or adapt it slightly in your own words:

> I am new to coding and I am learning by modifying existing projects.  
> When I ask questions, I want **explicit, step-by-step explanations**, even for basic things.  
> Please:
> 
> - explain unfamiliar concepts before using them
> - describe the purpose of files and directories
> - explain why a change is needed, not just how
> - propose small, testable steps
> - warn me if something might break  
>     Assume I want to understand and learn, not just copy code.

Save this.

### Step 3 — Habit to adopt

Whenever you feel lost, explicitly say things like:

- “Explain this as if I’ve never seen a project like this before.”
- “What is the _mental model_ here?”
- “What would be the smallest safe change to try first?”

---

# Part 4A — Keyboard Layout Remix (Macron vowels on AZERTY)

<span style="color: grey">(60-90 min - choose one project)</span> <span style="color: red">Choose either 4A or 4B, don't try both</span>

## Objective

You will:

- fork an existing keyboard-layout project,    
- adapt it so you can type **macron vowels for Japanese** (ā ī ū ē ō),
- label the language/variant as **`mp`**,
- test it on a virtual machine (VM).

---

## A0 — Prepare Your Environment

### Goal

You must be able to:

- clone repositories,
- build/run them,
- test inside a VM.

### Check

You are ready when:

- you can open a terminal in the VM,
- `git --version` works,
- you can clone a repo from GitHub.

---

## A1 — Fork the Keyboard Project

### Step 1 — Try to fork

Attempt to fork:

`https://github.com/PotatoSinology/dvorak-dpm`

If GitHub shows **404 / not found**, tell Daniel.

If the repo exists:

- fork it to your own GitHub account,
- clone it locally,
- open it in Cursor.

---

## A2 — Ask Cursor to Explain the Project

### Goal

Understand _what this project does_ before touching anything.

### In Cursor, ask:

> Explain what this project does, which operating system it targets, and how keyboard layouts are defined here.  
> Which files should I read first, and why?

Read the answer carefully.  
Open the files Cursor mentions.

### Write a short note (in a file called `NOTES.md`)

Answer, in your own words:

- What kind of keyboard system is this?
- Where are the key mappings defined?
- How does the project distinguish between languages or variants?

You don’t need perfect accuracy — this is about orientation.

---

## A3 — Ask Cursor About Your Goal

### Goal

Translate “what I want” into “what needs to change”.

Ask Cursor:

> I want to support typing macron vowels for Japanese (ā ī ū ē ō) on an AZERTY keyboard, and label this layout as language code `mp`.  
> Based on this repository, what parts would likely need to change?

Cursor should:

- point to specific files,
- mention configuration vs logic,
- explain risks.

Add notes to `NOTES.md`.

---

## A4 — Devise a Plan (Before Coding)

### Goal

Decide _how_ you want typing to work.

Write answers to these questions:

- How will I trigger macrons? (AltGr? dead key? sequence?)
- What exact keys produce ā ī ū ē ō?
- Do I want minimal changes or a richer system?

Then ask Cursor:

> Given this plan, propose the smallest possible implementation steps, in a safe order, with testing after each step.

You should get a **chunked plan**.

---

## A5 — Implement in Small Steps

### Rule

**One idea → one small change → test → commit**

Suggested steps:

1. Add the new variant / language label (`mp`) without changing key behavior.
2. Implement **one vowel only** (e.g. ō).
3. Test it in the VM.
4. Implement the remaining vowels.
5. Add documentation explaining how to type them.

### After each step

- Test in the VM.
- Write a commit message describing _what changed_ and _why_.

---

## A6 — Final Test

### You are done when:

- you can type: `Tōkyō`, `Ōsaka`, `jū`, etc.,
- it still works after rebooting the VM,
- you can explain where the mapping lives in the repo.

---

# Part 4B — Character Composer (Radically → marinaMoji)

<span style="color: grey">(60-90 min - choose one project)</span> <span style="color: red">Choose either 4A or 4B, don't try both</span>

## Objective

You will:

- evaluate an existing character-composition tool,    
- fork it into the marinaMoji organization,
- add it as a submodule,
- create a separate experimentation fork,
- explore whether it could be adapted for your project (possibly in C).

---

## B0 — Evaluate the Existing Tool

### Step 1 — Visit the app

Go to:

`https://radically.bryankok.com/`

Use it for a few minutes.

### Step 2 — Answer these questions (write them down)

- What does this tool do well?
- What feels close to what you want?
- What is missing or wrong for your needs?

There is no “correct” answer.

---

## B1 — Inspect the GitHub Repository

### Step 1 — Visit the repo

Go to the GitHub repository linked from the site.

### Step 2 — Check:

- Programming language(s)
- Project structure
- License(s)

Ask Cursor:

> Explain the structure of this repository and what each major directory does.

---

## B2 — Fork to marinaMoji

### Step

Fork the repository into the **marinaMoji GitHub organization**.

Name it something that clearly signals it mirrors upstream (e.g. `radically-upstream`).

---

## B3 — Add as a Submodule

Inside the **main marinaMoji repository**:

`git submodule add https://github.com/marinaMoji/radically-upstream.git vendor/radically git submodule update --init --recursive git commit -m "Add Radically as submodule"`

### Check

You are done when:

- a fresh clone + submodule init works,
- nothing breaks.

---

## B4 — Create an Experimentation Fork

### Goal

Separate “upstream mirror” from “we experiment freely”.

Steps:

1. Fork `radically-upstream` → `character_composer`
2. Clone `character_composer`
3. Add upstream remote:

`git remote add upstream https://github.com/Radically/radically.git git fetch --all`

---

## B5 — Build and Run Baseline

Before changing anything:

- follow the README,
- build and run the project,
- confirm it works _as is_.

If it doesn’t work:

- ask Cursor to help debug,
- **do not modify functionality yet**.

---

## B6 — Ask Cursor About Adaptation

Now the thinking part.

Ask Cursor:

> Explain the architecture of this project:  
> – where data comes from  
> – how character decomposition/search works  
> – what is UI vs core logic

Then ask:

> If we wanted to reuse the core logic of this project in a different system, possibly implemented in C, which parts could realistically be adapted or rewritten?  
> Propose an incremental plan with testing at each step.

---

## B7 — Write a Chunked Adaptation Plan

Your plan should include:

- What to extract or re-implement first
- What can be ignored initially
- What kind of tests you would use
- What “success” looks like at each stage

You are **not** expected to implement everything — just to reason clearly and cautiously.

---

## End-of-Session Deliverables

By the end, you should have:

- a working keyboard layout variant (`mp`) with macron vowels,
- Radically added as a submodule in marinaMoji,
- a separate `character_composer` fork ready for experiments,
- a written plan describing how (and whether) adaptation makes sense.

If at any point you feel stuck:  
**Pause, ask Cursor to explain, and write down what you learned.**  
That _is_ the exercise.

Now you can code faster and better than almost anyone on earth could 5 years ago. You still have things to learn, which you will – faster than I will anticipate. However, you can now begin developing *with me* as an equal partner.

You're the best Marina.