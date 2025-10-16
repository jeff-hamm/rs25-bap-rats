# Jekyll Setup Guide

## Quick Start (GitHub Pages - Easiest!)

1. **Push this folder to GitHub:**
   ```bash
   cd rsbap
   git init
   git add .
   git commit -m "Initial commit - RAT proposals"
   git branch -M main
   git remote add origin https://github.com/jeff-hamm/rs25-bap-rats.git
   git push -u origin main
   ```

2. **Enable GitHub Pages:**
   - Go to your repo on GitHub: https://github.com/jeff-hamm/rs25-bap-rats
   - Click **Settings** → **Pages**
   - Under "Source", select **main** branch
   - Click **Save**

3. **View your site:**
   - Will be live at: `https://jeff-hamm.github.io/rs25-bap-rats/`
   - Usually takes 1-2 minutes to build

---

## Local Development (Optional)

If you want to preview locally before pushing:

### Install Jekyll (Windows)

```powershell
# Install Ruby (if not already installed)
# Download from: https://rubyinstaller.org/downloads/
# Choose Ruby+Devkit version

# Then install Jekyll
gem install jekyll bundler

# Navigate to rsbap folder
cd rsbap

# Install dependencies
bundle install

# Run local server
bundle exec jekyll serve

# View at: http://localhost:4000
```

---

## File Structure

```
rsbap/
├── _config.yml                          # Jekyll configuration
├── Gemfile                              # Ruby dependencies
├── .gitignore                           # Git ignore rules
├── index.md                             # Homepage
├── README.md                            # Repository info
├── SETUP_GUIDE.md                       # This file
├── Bring_a_Pheromone_RAT_2025.md       # Option 1
├── Pheromone_Decategorization_RAT_Option2.md  # Option 2
└── Armpit_Glory_Hole_RAT_Option3.md    # Option 3
```

---

## Customization

### Change Theme

Edit `_config.yml`:
```yaml
theme: minima  # or jekyll-theme-cayman, jekyll-theme-slate, etc.
```

### Add Images

1. Create an `assets` or `images` folder
2. Add images there
3. Reference in markdown: `![Alt text](images/booth.jpg)`

### Customize Navigation

Create `_data/navigation.yml`:
```yaml
- name: Home
  link: /
- name: Option 1
  link: /Bring_a_Pheromone_RAT_2025.html
```

---

## Troubleshooting

**GitHub Pages not building?**
- Check the Actions tab in your GitHub repo for build errors
- Make sure `_config.yml` has valid YAML syntax

**Links not working?**
- Use `.html` extension in links, not `.md`
- Or use Jekyll's `{% link filename.md %}` syntax

**Styling issues?**
- Try a different theme in `_config.yml`
- Or create custom CSS in `assets/css/style.scss`

---

## Need Help?

- Jekyll Docs: https://jekyllrb.com/docs/
- GitHub Pages: https://docs.github.com/en/pages
- Themes: https://pages.github.com/themes/
