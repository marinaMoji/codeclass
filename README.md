# codeclass
Course materials for one-day coding class for MP

## Installation Instructions

To use these Jupyter notebooks on Ubuntu, you'll need to install Python and JupyterLab. Follow these steps:

### Step 1: Check Python Installation

Python 3 is usually pre-installed on Ubuntu. Check if you have it:

```bash
python3 --version
```

If Python 3 is not installed, install it:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 2: Install JupyterLab and Required Packages

Open a terminal and run:

```bash
pip3 install jupyterlab ipykernel
```

If you get a permission error, you may need to use `--user`:

```bash
pip3 install --user jupyterlab ipykernel
```

### Step 3: Launch JupyterLab

1. Navigate to this project directory in your terminal:
   ```bash
   cd /path/to/codeclass
   ```
   (Replace `/path/to/codeclass` with the actual path to this folder)

2. Start JupyterLab:
   ```bash
   jupyter lab
   ```
   
   If the `jupyter` command is not found, try:
   ```bash
   python3 -m jupyter lab
   ```

3. Your web browser should automatically open to JupyterLab. If it doesn't, look for a URL in the terminal output (usually `http://localhost:8888`)

### Step 4: Open the Notebooks

In JupyterLab:
- Navigate to the `part_1_notebooks/` folder
- Click on any `.ipynb` file to open it
- Start with `00_Python_Intro.ipynb` and work through them in order

### Troubleshooting

- **"pip3 not found"**: Install pip3 with `sudo apt install python3-pip`
- **"jupyter: command not found"**: If you used `--user` flag, you may need to add `~/.local/bin` to your PATH. Alternatively, run `python3 -m jupyter lab` instead of `jupyter lab`
- **Notebooks won't run**: Make sure you've installed `ipykernel` (it's included in the installation command above)
- **Permission errors**: Use the `--user` flag when installing with pip3, or use `sudo` (not recommended)

### Additional Notes

- The notebooks use data from the `data/` directory. Make sure you don't delete or move this folder.
- All notebooks are designed to work with Python 3.8 or newer.
- If you encounter encoding errors with Japanese text, make sure your terminal/system supports UTF-8 encoding.

## Course Schedule

This is a 10-hour schedule designed for a one-day intensive course (9:00-19:00). Time estimates are approximate and can be adjusted based on student pace.

| Time | Activity | Duration |
|------|----------|----------|
| 09:00-09:30 | Part 1: Intro + Numbers (quick) | 30 min |
| 09:30-11:30 | Part 1: Strings, Lists, Dicts, Functions | 120 min |
| 11:30-11:45 | Break | 15 min |
| 11:45-12:00 | Part 1: Files (quick), Regex basics | 15 min |
| 12:00-13:00 | Part 2: Pandas Intro, Loading, Exploring (quick), Filtering | 60 min |
| 13:00-14:00 | Lunch | 60 min |
| 14:00-15:00 | Part 2: Merging (thorough) | 60 min |
| 15:00-15:30 | Part 2: Statistics | 30 min |
| 15:30-15:45 | Break | 15 min |
| 15:45-17:30 | Part 3: XML parsing (Parts 5-7, skip 8-9) | 105 min |
| 17:30-18:30 | Part 4: Choose one project (4A or 4B) | 60 min |
| 18:30-19:00 | Wrap-up, Q&A, review | 30 min |

**Total: 10 hours** (9:00-19:00)

**Key Time-Savers:**
- Skip Part 1 Numbers notebook - do a 5-minute demo
- Skip Part 1 Regex - mention it, don't go deep
- Move quickly through Part 2 Exploring - show the basics
- Skip Part 3 Parts 1-4 - do a quick demo, then jump to parsing
- Skip Part 3 Part 8 (scaling up) - mention it, don't implement
- Choose one Part 4 project - don't try both
