Anthropic apps - Claude Code and computer use

# Anthropic apps

In this module, we'll explore two powerful applications built by Anthropic: Claude Code and Computer Use. These aren't just useful tools on their own - they're perfect examples of AI agents in action. By understanding how they work, you'll get a solid foundation for building your own agents later.

## Our Plan

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542875%2F10_-_001_-_Anthropic_Apps_02.1748542875572.jpg)We'll follow a progression that builds your understanding step by step:

* **Claude Code** - Start with this agentic coding assistant that runs in your terminal
* **Computer Use** - Explore this set of tools that lets Claude interact with desktop applications
* **Agents** - Understand what makes these applications successful as agents

## Claude Code

Claude Code is a terminal-based coding assistant that can help you with various programming tasks. Think of it as having Claude available right in your command line, ready to:

* Edit files and fix bugs
* Answer coding questions
* Help with development workflows

We'll walk through the complete setup process and then use Claude Code on a small sample project so you can see exactly how it operates in practice.

## Computer Use

Computer Use takes Claude's capabilities much further. It's a collection of tools that allow Claude to interact with a full desktop computer environment. This means Claude can:

* Access websites and browse the internet
* Interact with desktop applications
* Perform tasks that require visual interface navigation

This dramatically expands what's possible compared to text-only interactions.

## Why These Matter for Agents

Both Claude Code and Computer Use serve as excellent case studies for understanding agents. They demonstrate key principles that make agents effective:

* Tool integration and usage
* Multi-step task execution
* Environmental interaction
* Autonomous problem-solving

By examining these real-world implementations, you'll gain insights into what makes Claude Code and Computer Use successful, which will inform your own agent development work.

Let's start with the setup process for Claude Code in the next section.

# Claude Code setup

Claude Code is a terminal-based coding assistant that runs directly in your command line. Think of it as having Claude available right in your terminal to help with any coding task you're working on.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542849%2F10_-_002_-_Claude_Code_Setup_00.1748542849392.jpg)## What Claude Code Can Do

Claude Code comes with a comprehensive set of tools to help with your development workflow:

* **File operations** - Search, read, and edit files in your project
* **Terminal access** - Run commands directly from the conversation
* **Web access** - Search documentation, fetch code examples, and more
* **MCP Server support** - Add additional tools by connecting MCP servers

The MCP integration is particularly powerful because it means you can extend Claude Code's capabilities by adding specialized tools for databases, APIs, or any other services you work with.

Claude Code works across MacOS, Windows WSL, and Linux, so you can use it regardless of your development environment.

## Installation

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542850%2F10_-_002_-_Claude_Code_Setup_10.1748542849909.jpg)Getting Claude Code set up takes just three steps:

1. **Install Node.js** from nodejs.org/en/download (check if you already have it by running `npm help` in your terminal)
2. **Install Claude Code** with the command: `npm install -g @anthropic-ai/claude-code`
3. **Start and login** by running `claude` in your terminal

When you run the `claude` command for the first time, it will prompt you to log in to your Anthropic account. The full setup guide is available at docs.anthropic.com if you need more detailed instructions.

Once you're set up, you'll have Claude available directly in your terminal, ready to help with any coding project or task you're working on.

# Claude Code in action

Claude Code isn't just a tool for writing code - it's designed to work alongside you throughout every phase of a software project. Think of it as another engineer on your team who can handle everything from initial setup to deployment and support.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542928%2F10_-_003_-_Claude_Code_in_Action_01.1748542928114.jpg)

## The /init Command

When you start working with Claude Code on a project, the first thing you'll want to do is run the `/init` command. This tells Claude to scan your entire codebase and understand your project's structure, dependencies, coding style, and architecture.

Claude summarizes everything it learns in a special file called `CLAUDE.md`. This file automatically gets included as context in all future conversations, so Claude remembers important details about your project.

You can have multiple CLAUDE.md files for different scopes:

* **Project** - Shared between all engineers working on the project
* **Local** - Your personal notes that aren't checked into git
* **User** - Used across all your projects

When running `/init`, you can add special directions for areas you want Claude to focus on. The generated file will include build commands, coding guidelines, and project-specific patterns that Claude should follow.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542928%2F10_-_003_-_Claude_Code_in_Action_05.1748542928626.jpg)You can also quickly add notes to your CLAUDE.md file using the `#` command. For example, typing `# Always use descriptive variable names` will prompt you to add this guideline to your project, local, or user memory.

## Common Workflows

Claude works best when you approach it as an effort multiplier. The more context and structure you provide, the better results you'll get. Here's the most effective workflow:

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542929%2F10_-_003_-_Claude_Code_in_Action_11.1748542928969.jpg)

### Step 1: Feed Context into Claude

Before asking Claude to build something, identify files in your codebase that are relevant to the feature you want to create. Ask Claude to read and analyze these files first. This gives Claude examples of your coding patterns and existing functionality it can build upon.

### Step 2: Tell Claude to Plan a Solution

Instead of jumping straight to implementation, ask Claude to think through the problem and create a plan. Tell Claude specifically not to write any code yet - just focus on the approach and steps needed.

### Step 3: Ask Claude to Implement the Solution

Once you have a solid plan, ask Claude to implement it. Claude will write code based on the context and planning work you've already done together.

## Test-Driven Development Workflow

For even better results, you can use a test-driven approach:

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542929%2F10_-_003_-_Claude_Code_in_Action_17.1748542929416.jpg)1. **Feed context into Claude** - Same as before, show Claude relevant files

1. **Ask Claude to think of test cases** - Have Claude brainstorm what tests would validate your new feature
2. **Ask Claude to implement those tests** - Select the most relevant tests and have Claude write them
3. **Ask Claude to write code that passes the tests** - Claude will iterate on the implementation until all tests pass

This approach often produces more robust code because Claude has clear success criteria to work toward.

## Practical Example

Here's how these workflows look in practice. Let's say you want to add a document conversion tool to an existing project:

```
// First, ask Claude to read relevant files
> Read the math.py and document.py files

// Then ask for planning (not implementation)
> Plan to implement document_path_to_markdown tool:
1. Create a function that:
   - Takes a file path parameter
   - Validates the file exists  
   - Determines file type from extension
   - Reads binary data from file
   - Leverages existing binary_document_to_markdown function
   - Returns markdown string
2. Add appropriate documentation
3. Register the tool with MCP server
4. Add tests

// Finally, ask for implementation
> Implement the plan
```

Claude will then create the function, update the necessary files, write tests, and even run the test suite to verify everything works correctly.

## Additional Commands

Claude Code includes several helpful commands:

* `/clear` - Clears conversation history and resets context
* `/init` - Scans codebase and creates CLAUDE.md documentation
* `#` - Adds notes to your CLAUDE.md file

Claude can also handle routine development tasks like staging and committing changes to git, running tests, and managing dependencies. Instead of switching between your editor and terminal, you can ask Claude to handle these tasks while you focus on the bigger picture.

The key to success with Claude Code is remembering that it's designed to be a collaborative partner, not just a code generator. The more context and structure you provide, the more effectively Claude can help you build and maintain your projects.

# Enhancements with MCP servers

Claude Code has an MCP client built right into it, which means you can connect MCP servers to dramatically expand what Claude can do. This opens up some really powerful possibilities for customizing your development workflow.

## How MCP Extends Claude

The Model Context Protocol allows Claude Code to connect to external services and tools through MCP servers. Instead of being limited to Claude's built-in capabilities, you can add custom functionality by connecting servers that provide specific tools, resources, or integrations.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542913%2F10_-_004_-_Enhancements_with_MCP_Servers_01.1748542913123.jpg)Each MCP server can expose different types of functionality to Claude through three main components: Tools (for taking actions), Prompts (for templates), and Resources (for accessing data).

## Setting Up an MCP Server

Adding an MCP server to Claude Code is straightforward. You use the command line to register your server:

```
claude mcp add [server-name] [command-to-start-server]
```

For example, if you have a document processing server that starts with `uv run main.py`, you'd run:

```
claude mcp add documents uv run main.py
```

Once registered, Claude Code will automatically connect to your server when it starts up.

## Example: Document Processing

A practical example is creating a tool that lets Claude read PDF and Word documents. By building an MCP server with a "document_path_to_markdown" tool, you can ask Claude to convert document contents to markdown format.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542914%2F10_-_004_-_Enhancements_with_MCP_Servers_02.1748542913748.jpg)When you ask Claude to "Convert the tests/fixtures/mcp_docs.docx file to markdown", it will automatically use your custom tool to read the document and return the converted content.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542914%2F10_-_004_-_Enhancements_with_MCP_Servers_13.1748542914556.jpg)## Popular MCP Integrations

The MCP ecosystem includes servers for many common development tools and services:

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542915%2F10_-_004_-_Enhancements_with_MCP_Servers_16.1748542915462.jpg)* **sentry-mcp** - Automatically discover and fix bugs logged in Sentry

* **playwright-mcp** - Gives Claude browser automation capabilities for testing and troubleshooting
* **figma-context-mcp** - Exposes Figma designs to Claude
* **mcp-atlassian** - Allows Claude to access Confluence and Jira
* **firecrawl-mcp-server** - Adds web scraping capabilities to Claude
* **slack-mcp** - Allows Claude to post messages or reply to specific threads

## Building Your Development Workflow

The real power comes from combining multiple MCP servers that match your specific development process. You might set up:

* A Sentry server to fetch production error details
* A Jira server to read ticket requirements
* A Slack server to notify your team when work is complete
* Custom servers for your internal tools and APIs

This creates a development environment where Claude can seamlessly work with all the tools and services you already use, making it a much more powerful coding assistant tailored to your specific workflow.

# Parallelizing Claude Code

Running multiple instances of Claude Code in parallel is one of the biggest productivity gains you can achieve. Since Claude is lightweight, you can easily spin up several copies, assign each a different task, and have them work simultaneously. This effectively gives you a team of virtual software engineers working on your project.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542981%2F10_-_005_-_Parallelizing_Claude_Code_00.1748542980996.jpg)## The Core Challenge

The main problem with parallel instances is file conflicts. When two Claude instances try to modify the same file simultaneously, they can write conflicting or invalid code since they're unaware of each other's changes.

The solution is simple: give each instance its own separate workspace. Each Claude instance works with its own copy of your project, makes changes in isolation, and then merges those changes back into your main project.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542981%2F10_-_005_-_Parallelizing_Claude_Code_02.1748542981591.jpg)## Git Worktrees

Git worktrees are the perfect tool for this workflow. If your project uses Git (which it should), you can use worktrees immediately. They're like an extension of Git's branching system that creates complete copies of your project in separate directories.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542982%2F10_-_005_-_Parallelizing_Claude_Code_03.1748542982035.jpg)Each worktree corresponds to a separate branch. You can have:

* Feature A branch in one folder
* Feature B branch in another folder
* Each containing a complete copy of your codebase
* Separate Claude Code instances running in each

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542983%2F10_-_005_-_Parallelizing_Claude_Code_04.1748542982398.jpg)When each Claude instance finishes its work, you commit the changes and merge them back into your main branch, just like any normal Git workflow.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542983%2F10_-_005_-_Parallelizing_Claude_Code_05.1748542983427.jpg)## Automating Worktree Creation

Rather than manually creating worktrees, you can have Claude handle the entire process. Here's a prompt that creates a worktree and sets up the workspace:

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542984%2F10_-_005_-_Parallelizing_Claude_Code_06.1748542984326.jpg)This prompt tells Claude to:

1. Check if a worktree already exists
2. Create a new Git worktree in the `.trees` folder
3. Symlink the `.venv` folder (since virtual environments aren't tracked by Git)
4. Launch a new VSCode instance in that directory

## Custom Slash Commands

Typing long prompts repeatedly gets tedious. Claude Code supports custom commands that automate this process.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542985%2F10_-_005_-_Parallelizing_Claude_Code_09.1748542984846.jpg)To create custom commands:

* Add a `.md` file to `.claude/commands`
* Put your prompt inside the file
* Use `$ARGUMENTS` as a placeholder for dynamic values
* Run with `/project:filename argument`

For example, `/project:create_worktree feature_b` would create a worktree named "feature_b".

## Parallel Development Workflow

Here's how a typical parallel development session works:

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542985%2F10_-_005_-_Parallelizing_Claude_Code_15.1748542985281.jpg)1. Create multiple worktrees for different features

1. Launch Claude Code in each workspace
2. Assign different tasks to each instance
3. Let them work in parallel
4. Commit changes when each task completes
5. Merge all branches back to main

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542985%2F10_-_005_-_Parallelizing_Claude_Code_16.1748542985628.jpg)## Automated Merging

You can also automate the merge process with another custom command. Create a merge prompt that:

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542986%2F10_-_005_-_Parallelizing_Claude_Code_17.1748542986000.jpg)1. Changes into the worktree directory

1. Examines the latest commit
2. Changes back to the root directory
3. Merges the worktree branch
4. Handles any merge conflicts automatically
5. Resolves conflicts based on understanding of the changes

Claude can even handle merge conflicts intelligently, understanding the context of changes from different branches and resolving them appropriately.

## Scaling Your Development

This approach scales to as many parallel instances as you can effectively manage. You're limited only by:

* Your machine's resources
* Your ability to coordinate multiple tasks
* The complexity of potential merge conflicts

The productivity gains are substantial - instead of working on features sequentially, you can develop multiple features simultaneously, dramatically reducing development time for complex projects.

# Automated debugging

Claude Code extends far beyond writing code in your editor. It can monitor your deployed applications, detect production errors, and even automatically fix them. This creates a powerful workflow where Claude acts as your automated debugging assistant, catching issues that only appear in production environments.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542967%2F10_-_006_-_Automated_Debugging_00.1748542967081.jpg)## The Production Problem

Here's a common scenario: your application works perfectly in development, but breaks in production. You might have a chatbot that responds correctly to simple questions locally, but fails to generate artifacts like spreadsheets when deployed to AWS Amplify. The request appears to succeed, but the results are empty or incomplete.

Traditionally, you'd need to dig through CloudWatch logs, hunt for error messages, and manually debug the differences between your local and production environments. This process is time-consuming and requires you to context-switch from development work to operations troubleshooting.

## Automated Error Detection and Fixing

Instead of manual debugging, you can set up Claude to handle this entire workflow automatically. Here's how the system works:

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748542967%2F10_-_006_-_Automated_Debugging_14.1748542967617.jpg)The automated workflow follows these steps:

1. A GitHub Action runs daily (typically early morning)
2. Claude queries CloudWatch for errors from the last 24 hours
3. It filters and deduplicates errors to fit within context limits
4. Claude analyzes each error and attempts to fix it
5. Fixed code gets committed and a pull request is automatically opened

## Setting Up the Workflow

The GitHub Action needs several components to work effectively:

* Repository checkout and dependency installation
* Claude Code setup and configuration
* AWS CLI installation for CloudWatch access
* Error filtering logic to manage context window limits
* Automated commit and pull request creation

When Claude finds errors in your logs, it doesn't just identify them—it understands the context. For example, if you have an invalid model identifier that only affects production (like `us.anthropic.claude-3-5-sonnet-20241021-v2:0` instead of the correct `us.anthropic.claude-3-5-sonnet-20240624-v1:0`), Claude can recognize this pattern and apply the appropriate fix.

## Real-World Results

When the automated system runs successfully, you'll see pull requests that include:

* Clear error descriptions in plain language
* Root cause analysis
* Specific fixes implemented
* Updated code with proper model identifiers or configuration

The pull request becomes a reviewable artifact where you can see exactly what Claude found and how it fixed the issue. This gives you confidence in the changes while maintaining code review practices.

## Customizing Your Debugging Workflow

This automated debugging approach is highly flexible. You can adapt it to your specific needs by:

* Adjusting the error detection frequency
* Customizing which types of errors to prioritize
* Adding specific debugging instructions for your application
* Integrating with different logging systems beyond CloudWatch
* Setting up notifications for critical issues

The key is that Claude Code can understand your application's context, analyze production errors intelligently, and propose fixes that account for environment-specific differences. This transforms debugging from a reactive, manual process into a proactive, automated system that keeps your applications running smoothly.

# Computer use

Computer Use is a powerful feature that lets Claude interact directly with desktop environments, essentially giving the AI the ability to control a computer like a human would. This capability opens up entirely new possibilities for automation, testing, and workflow assistance.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543021%2F10_-_007_-_Computer_Use_00.1748543021569.jpg)## What Computer Use Can Do

Instead of just generating code or providing advice, Claude can actually navigate websites, click buttons, fill out forms, and interact with applications in real-time. This makes it incredibly useful for tasks like:

* Automated QA testing of web applications
* Data entry and form filling
* Website navigation and information gathering
* UI testing and validation
* Repetitive desktop tasks

## Real-World Example: Automated QA Testing

Here's a practical example that shows the power of Computer Use. Imagine you've built a React component with an autocomplete feature - users can type `@` to mention files or resources. At first glance, everything seems to work fine, but there might be edge cases you haven't discovered yet.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543022%2F10_-_007_-_Computer_Use_05.1748543022086.jpg)Rather than manually testing every possible interaction, you can delegate this work to Claude. You simply provide instructions like:

```
Your goal is to conduct QA testing on a React component hosted at https://test-mentioner.vercel.app/

Testing process:
1. Open a new browser tab
2. Navigate to https://test-mentioner.vercel.app/
3. Execute the test cases below one by one
4. After completing all tests, write a concise report

Test cases:
1. Typing 'Did you read @' should display autocomplete options
2. Typing 'Did you read @' then pressing enter should add '@document.pdf'
3. After adding '@document.pdf', pressing backspace should show autocomplete options directly below the text, not elsewhere on the page
```

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543022%2F10_-_007_-_Computer_Use_16.1748543022490.jpg)## How It Works in Practice

Computer Use runs in a controlled environment - typically a Docker container with a browser that's completely isolated from your main system. You interact with Claude through a chat interface, giving it instructions about what to do, and then watch as it navigates and interacts with the application.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543023%2F10_-_007_-_Computer_Use_17.1748543022870.jpg)Claude follows your instructions step by step, taking screenshots, clicking elements, typing text, and observing the results. In the QA testing example, Claude would:

1. Navigate to the specified URL
2. Type the test input and observe autocomplete behavior
3. Test the enter key functionality
4. Check the backspace behavior for proper positioning
5. Generate a detailed report of what passed and what failed

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543023%2F10_-_007_-_Computer_Use_18.1748543023770.jpg)## The Results

After running through all the test cases, Claude provides a comprehensive report. In our example, it might find that the first two tests pass (autocomplete appears correctly, enter key works), but the third test fails because the autocomplete dropdown appears in the wrong location when backspace is pressed.

This kind of automated testing can save developers significant time, especially for repetitive QA tasks or when you need to test multiple scenarios quickly. Instead of manually clicking through every possible interaction, you can describe what you want tested and let Claude handle the execution.

## Security and Isolation

Computer Use operates in a sandboxed environment for safety. The browser and desktop environment run inside Docker containers, completely isolated from your main system. This means Claude can interact with web applications and test interfaces without any risk to your personal files or system security.

This isolation is crucial because it allows you to give Claude broad permissions to interact with applications while maintaining complete control over what it can and cannot access.

# How Computer use works

Computer use in Claude works exactly like regular tool use - it's just a special implementation of the same underlying tool system. Understanding this connection makes computer use much easier to grasp and implement.

## Tool Use Refresher

Before diving into computer use, let's quickly review how regular tool use works with Claude:

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543025%2F10_-_008_-_How_Computer_Use_Works_01.1748543025424.jpg)1. You send Claude a user message along with a tool schema

1. Claude decides it needs to use a tool to answer the question
2. Claude responds with a tool use request containing the tool name and input parameters
3. Your server runs the actual function and returns the result
4. You send the result back to Claude in a tool result message

For example, if someone asks "What's the weather in San Francisco?", you'd provide a `get_weather` tool schema. Claude would call that tool with the location parameter, your code would fetch the weather data, and you'd return "Sunny" back to Claude.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543026%2F10_-_008_-_How_Computer_Use_Works_07.1748543026297.jpg)## Computer Use: Same Flow, Different Tool

Computer use follows this exact same pattern. The key insight is that computer use is implemented as a tool - just a very special one that can interact with a desktop environment.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543026%2F10_-_008_-_How_Computer_Use_Works_08.1748543026655.jpg)Here's what happens:

* You include a tool schema that provides computer interaction capabilities
* Claude decides to use the computer tool
* Instead of running a simple function, you execute the requested action in a computing environment
* You send the result (like a screenshot) back to Claude

## The Computer Tool Schema

The computer use tool schema starts simple but gets automatically expanded into something much more comprehensive:

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543027%2F10_-_008_-_How_Computer_Use_Works_09.1748543027109.jpg)You send a basic schema like:

```
{
  "type": "computer_20250124",
  "name": "computer",
  "display_width_px": 1024,
  "display_height_px": 768,
  "display_number": 1
}
```

Behind the scenes, this gets expanded into a detailed schema that tells Claude it can perform actions like:

* `key` - Press keyboard keys
* `mouse_move` - Move the cursor
* `left_click` - Click at specific coordinates
* `screenshot` - Take a screenshot
* `scroll` - Scroll the screen

## The Computing Environment

To make computer use work, you need an actual computing environment that can execute these actions programmatically. The most common approach is using a Docker container with a desktop environment like Firefox.

When Claude requests an action like "click at coordinates (500, 300)", your system:

1. Receives the tool use request
2. Executes the mouse click in the Docker container
3. Takes a screenshot of the result
4. Sends the screenshot back to Claude

The Docker container doesn't have to be complex - it just needs to support programmatic keyboard and mouse interactions.

## Getting Started

You don't need to build the computing environment from scratch. Anthropic provides a reference implementation that handles all the technical details.

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543027%2F10_-_008_-_How_Computer_Use_Works_17.1748543027671.jpg)Setting it up is straightforward:

1. Install Docker (you might already have it)
2. Run the provided Docker command with your API key
3. Access the web interface to chat with Claude

The setup command looks like this:

```
export ANTHROPIC_API_KEY="your_api_key"
docker run \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -v $HOME/.anthropic:/home/computeruse/.anthropic \
  -p 5900:5900 \
  -p 8501:8501 \
  -p 6080:6080 \
  -p 8080:8080 \
  -it ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest
```

![](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2Fa46l9irobhg0f5webscixp0bs%2Fpublic%2F1748543028%2F10_-_008_-_How_Computer_Use_Works_19.1748543027991.jpg)Once running, you'll have access to a chat interface where you can test Claude's computer use capabilities directly. The full setup guide is available at github.com/anthropics/anthropic-quickstarts.

## Key Takeaway

Computer use isn't magic - it's just the regular tool use system applied to desktop automation. Claude doesn't directly control computers; instead, it makes tool requests that your code fulfills by executing actions in a controlled environment. This makes computer use both powerful and safe, since you maintain full control over what actions actually get executed.
