#!/usr/bin/env node
"use strict";

const readline = require("node:readline");
const process = require("node:process");

class UnifiedCompleter {
  constructor() {
    this.prompts = [];
    this.promptMap = new Map();
    this.resources = [];
  }

  updatePrompts(prompts) {
    this.prompts = prompts;
    this.promptMap = new Map(prompts.map((prompt) => [prompt.name, prompt]));
  }

  updateResources(resources) {
    this.resources = [...resources];
  }

  getCompletions(text, cursor) {
    const textBeforeCursor = text.slice(0, cursor);

    if (textBeforeCursor.includes("@")) {
      const lastAtPos = textBeforeCursor.lastIndexOf("@");
      const prefix = textBeforeCursor.slice(lastAtPos + 1);
      return this.resources
        .filter((resourceId) =>
          resourceId.toLowerCase().startsWith(prefix.toLowerCase()),
        )
        .map((id) => ({
          value: id,
          meta: "Resource",
          insertText: id,
          replaceStart: lastAtPos + 1,
          replaceEnd: cursor,
        }));
    }

    if (textBeforeCursor.startsWith("/")) {
      const body = textBeforeCursor.slice(1);
      const parts = body.trim() ? body.trim().split(/\s+/) : [];
      const endsWithSpace = /\s$/.test(textBeforeCursor);

      if (parts.length <= 1 && !endsWithSpace) {
        const cmdPrefix = parts[0] || "";
        const replaceStart = 1;
        const replaceEnd = cursor;
        return this.prompts
          .filter((prompt) => prompt.name.startsWith(cmdPrefix))
          .map((prompt) => ({
            value: `/${prompt.name}`,
            meta: prompt.description || "",
            insertText: prompt.name,
            replaceStart,
            replaceEnd,
          }));
      }

      if (parts.length === 1 && endsWithSpace) {
        return this.resources.map((id) => ({
          value: id,
          meta: "Resource",
          insertText: id,
          replaceStart: cursor,
          replaceEnd: cursor,
        }));
      }

      if (parts.length >= 2) {
        const docPrefix = parts[parts.length - 1];
        const replaceStart = cursor - docPrefix.length;
        return this.resources
          .filter((id) => id.toLowerCase().startsWith(docPrefix.toLowerCase()))
          .map((id) => ({
            value: id,
            meta: "Resource",
            insertText: id,
            replaceStart,
            replaceEnd: cursor,
          }));
      }
    }

    return [];
  }
}

class InputBuffer {
  constructor() {
    this.text = "";
    this.cursor = 0;
  }

  get isCursorAtEnd() {
    return this.cursor === this.text.length;
  }

  insertText(content) {
    this.text =
      this.text.slice(0, this.cursor) + content + this.text.slice(this.cursor);
    this.cursor += content.length;
  }

  replaceRange(start, end, content) {
    const safeStart = Math.max(0, Math.min(start, this.text.length));
    const safeEnd = Math.max(safeStart, Math.min(end, this.text.length));
    this.text = this.text.slice(0, safeStart) + content + this.text.slice(safeEnd);
    this.cursor = safeStart + content.length;
  }

  deleteLeftChar() {
    if (this.cursor === 0) {
      return;
    }

    this.text = this.text.slice(0, this.cursor - 1) + this.text.slice(this.cursor);
    this.cursor -= 1;
  }

  moveLeft() {
    if (this.cursor > 0) {
      this.cursor -= 1;
    }
  }

  moveRight() {
    if (this.cursor < this.text.length) {
      this.cursor += 1;
    }
  }

  moveHome() {
    this.cursor = 0;
  }

  moveEnd() {
    this.cursor = this.text.length;
  }

  clear() {
    this.text = "";
    this.cursor = 0;
  }
}

class CliApp {
  constructor({ prompts = [], resources = [] } = {}) {
    this.promptLabel = "> ";
    this.buffer = new InputBuffer();
    this.completer = new UnifiedCompleter();
    this.completer.updatePrompts(prompts);
    this.completer.updateResources(resources);

    this.completionItems = [];
    this.selectedCompletionIndex = -1;
    this.previousCompletionLineCount = 0;
  }

  run() {
    if (!process.stdin.isTTY || !process.stdout.isTTY) {
      throw new Error("This CLI requires an interactive TTY terminal.");
    }

    readline.emitKeypressEvents(process.stdin);
    process.stdin.setRawMode(true);

    process.stdin.on("keypress", (str, key) => this.handleKeypress(str, key));
    this.render();
  }

  handleKeypress(str, key) {
    if (key && key.ctrl && key.name === "c") {
      this.exit();
      return;
    }

    if (key && key.name === "return") {
      if (this.hasCompletions()) {
        this.acceptSelectedCompletion();
        this.render();
        return;
      }

      this.submitLine();
      return;
    }

    if (key && key.name === "backspace") {
      this.buffer.deleteLeftChar();
      this.clearCompletions();
      this.render();
      return;
    }

    if (key && key.name === "left") {
      this.buffer.moveLeft();
      this.render();
      return;
    }

    if (key && key.name === "right") {
      this.buffer.moveRight();
      this.render();
      return;
    }

    if (key && key.name === "home") {
      this.buffer.moveHome();
      this.render();
      return;
    }

    if (key && key.name === "end") {
      this.buffer.moveEnd();
      this.render();
      return;
    }

    if (key && key.name === "up") {
      if (this.hasCompletions()) {
        this.moveSelection(-1);
        this.render();
      }
      return;
    }

    if (key && key.name === "down") {
      if (this.hasCompletions()) {
        this.moveSelection(1);
        this.render();
      }
      return;
    }

    if (key && key.name === "tab") {
      if (this.hasCompletions()) {
        this.acceptSelectedCompletion();
        this.render();
        return;
      }

      this.startCompletion();
      this.render();
      return;
    }

    if (str === "/") {
      this.onSlashKey();
      this.render();
      return;
    }

    if (str === "@") {
      this.onAtKey();
      this.render();
      return;
    }

    if (str === " ") {
      this.onSpaceKey();
      this.render();
      return;
    }

    if (str && !key?.ctrl && !key?.meta) {
      this.buffer.insertText(str);
      this.clearCompletions();
      this.render();
    }
  }

  onSlashKey() {
    if (this.buffer.isCursorAtEnd && this.buffer.text.length === 0) {
      this.buffer.insertText("/");
      this.startCompletion();
    } else {
      this.buffer.insertText("/");
      this.clearCompletions();
    }
  }

  onAtKey() {
    this.buffer.insertText("@");
    if (this.buffer.isCursorAtEnd) {
      this.startCompletion();
      return;
    }

    this.clearCompletions();
  }

  onSpaceKey() {
    const textBeforeInsert = this.buffer.text;
    this.buffer.insertText(" ");

    if (textBeforeInsert.startsWith("/")) {
      const parts = textBeforeInsert.slice(1).trim().split(/\s+/).filter(Boolean);

      if (parts.length === 1) {
        this.startCompletion();
        return;
      }

      if (parts.length === 2) {
        const arg = parts[1].toLowerCase();
        if (
          arg.includes("doc") ||
          arg.includes("file") ||
          arg.includes("id")
        ) {
          this.startCompletion();
          return;
        }
      }
    }

    this.clearCompletions();
  }

  startCompletion() {
    const completions = this.completer.getCompletions(
      this.buffer.text,
      this.buffer.cursor,
    );

    if (completions.length === 0) {
      this.clearCompletions();
      return;
    }

    this.completionItems = completions;
    this.selectedCompletionIndex = 0;
  }

  hasCompletions() {
    return this.completionItems.length > 0;
  }

  moveSelection(step) {
    if (!this.hasCompletions()) {
      return;
    }

    const total = this.completionItems.length;
    this.selectedCompletionIndex =
      (this.selectedCompletionIndex + step + total) % total;
  }

  acceptSelectedCompletion() {
    if (!this.hasCompletions()) {
      return;
    }

    const item = this.completionItems[this.selectedCompletionIndex];
    this.buffer.replaceRange(item.replaceStart, item.replaceEnd, item.insertText);
    this.clearCompletions();
  }

  getCompletionLines() {
    if (!this.hasCompletions()) {
      return [];
    }

    const visibleCount = 8;
    const total = this.completionItems.length;
    let start = 0;
    if (this.selectedCompletionIndex >= visibleCount) {
      start = this.selectedCompletionIndex - visibleCount + 1;
    }
    const end = Math.min(start + visibleCount, total);

    const lines = ["Suggestions (use Up/Down + Enter):"];
    for (let i = start; i < end; i += 1) {
      const item = this.completionItems[i];
      const marker = i === this.selectedCompletionIndex ? ">" : " ";
      const meta = item.meta ? `  (${item.meta})` : "";
      lines.push(`${marker} ${item.value}${meta}`);
    }

    return lines;
  }

  clearCompletions() {
    this.completionItems = [];
    this.selectedCompletionIndex = -1;
  }

  submitLine() {
    const value = this.buffer.text.trim();
    this.clearCompletions();

    process.stdout.write("\n");
    if (value.length > 0) {
      if (value === "/quit") {
        this.exit();
        return;
      }
      process.stdout.write(`Echo: ${value}\n`);
    }

    this.buffer.clear();
    this.render();
  }

  render() {
    readline.cursorTo(process.stdout, 0);
    readline.clearLine(process.stdout, 0);

    const completionLines = this.getCompletionLines();

    for (let i = 0; i < this.previousCompletionLineCount; i += 1) {
      process.stdout.write("\n");
      readline.clearLine(process.stdout, 0);
    }
    if (this.previousCompletionLineCount > 0) {
      readline.moveCursor(process.stdout, 0, -this.previousCompletionLineCount);
    }

    process.stdout.write(`${this.promptLabel}${this.buffer.text}`);

    for (const line of completionLines) {
      process.stdout.write(`\n${line}`);
    }

    this.previousCompletionLineCount = completionLines.length;
    if (this.previousCompletionLineCount > 0) {
      readline.moveCursor(process.stdout, 0, -this.previousCompletionLineCount);
    }

    readline.cursorTo(process.stdout, this.promptLabel.length + this.buffer.cursor);
  }

  exit() {
    process.stdin.setRawMode(false);
    process.stdin.removeAllListeners("keypress");
    process.stdout.write("\n");
    process.exit(0);
  }
}

if (require.main === module) {
  const cli = new CliApp({
    prompts: [
      { name: "help", description: "Show usage help" },
      { name: "quit", description: "Quit this CLI" },
      { name: "summarize", description: "Summarize a document" },
      { name: "rewrite", description: "Rewrite a document" },
    ],
    resources: [
      "deposition.md",
      "report.pdf",
      "financials.docx",
      "outlook.pdf",
      "plan.md",
      "spec.txt",
    ],
  });
  cli.run();
}

module.exports = {
  CliApp,
  UnifiedCompleter,
};
