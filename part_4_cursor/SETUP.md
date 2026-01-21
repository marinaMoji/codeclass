# Setting up the Part 4 Repository on GitHub

## Step 1: Create the GitHub Repository

1. Go to https://github.com/organizations/PotatoSinology/repositories/new
   - Or navigate to the PotatoSinology organization and click "New repository"

2. Repository settings:
   - **Repository name**: `codeclass-part4` (or your preferred name)
   - **Description**: "Part 4 instructions for codeclass course"
   - **Visibility**: ✅ **Private** (important - this keeps it hidden from students)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these locally)

3. Click "Create repository"

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these commands in the `codeclass-part4` directory:

```bash
cd /home/d/Python/codeclass-part4
git remote add origin https://github.com/PotatoSinology/codeclass-part4.git
git push -u origin main
```

**Note**: Replace `codeclass-part4` in the URL with whatever name you chose in Step 1.

## Step 3: Verify

1. Check that the files appear on GitHub
2. Verify the repository is private
3. Test that students cannot access it (by logging out or using an incognito window)

## When Ready to Share with Students

You have several options:

### Option A: Add students as collaborators
1. Go to the repository Settings → Collaborators
2. Add students individually (they'll need GitHub accounts)
3. Grant them "Read" access

### Option B: Add as a submodule to the main repo
Once the repository is ready to be shared, you can add it as a submodule to the main codeclass repository:

```bash
cd /home/d/Python/codeclass
git submodule add https://github.com/PotatoSinology/codeclass-part4.git part_4_instructions
git commit -m "Add Part 4 as submodule"
```

Students would then need to run:
```bash
git submodule update --init --recursive
```

### Option C: Make it public
Simply change the repository visibility from Private to Public in Settings.

