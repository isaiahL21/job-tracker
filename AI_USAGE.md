# AI Usage Documentation

## Tools Used
- Claude (Anthropic) — primary tool for generating Flask routes, HTML templates, CSS, and debugging

## Key Prompts Used
1. "Help me build a Flask route to display all companies from MySQL"
2. "Debug job match feature - it only shows matched skills and no missing skills"
3. "Give some example theme ideas for CSS stylesheet"
4. "Debug my dashboard route — only one stat card is showing"

## What Worked Well
- Claude generated complete, working Flask routes quickly
- Very helpful for debugging errors and explaining what went wrong
- Generated clean HTML templates with consistent styling
- Helped design the dark command-center UI theme

## What I Modified
- Changed variable names to match my exact database schema
- Adjusted CSS colors and spacing to fit my preferences
- Fixed SQL queries to match my actual table and column names
- Added input validation and error handling

## Lessons Learned
- AI-generated code needs to be tested — small errors are common
- It helps to give AI very specific context about your project
- AI is great for boilerplate and structure, but customization is still needed
- Asking for explanations alongside code helps you actually learn the material