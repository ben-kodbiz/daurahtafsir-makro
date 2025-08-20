# Makefile for Channel Processing Tools

# Variables
TOOLS_DIR := /data/work/dev/daurahtafsir-makro/tools
PYTHON := python3
SHELL_SCRIPT := process_channel.sh
UTILS_SCRIPT := utils.sh
TEST_SCRIPT := test_tools.py

# Default target
.PHONY: help
help:
	@echo "📺 Channel Processing Tools - Makefile"
	@echo "========================================"
	@echo "Available targets:"
	@echo "  help          - Show this help message"
	@echo "  test          - Run tool tests"
	@echo "  utils         - Run interactive utilities"
	@echo "  demo          - Show quick start examples"
	@echo "  clean         - Clean temporary files"
	@echo ""
	@echo "To process a new channel, use the shell script directly:"
	@echo "  ./$(SHELL_SCRIPT) <CHANNEL_URL> --name <NAME> --description <DESC>"

# Run tests
.PHONY: test
test:
	@echo "🧪 Running tool tests..."
	@cd $(TOOLS_DIR) && $(PYTHON) $(TEST_SCRIPT)

# Run utilities
.PHONY: utils
utils:
	@echo "🔧 Running interactive utilities..."
	@cd $(TOOLS_DIR) && ./$(UTILS_SCRIPT)

# Show quick start guide
.PHONY: demo
demo:
	@echo "🎬 Quick Start Examples:"
	@echo "======================"
	@echo ""
	@echo "# Process a new YouTube channel:"
	@echo "./process_channel.sh https://www.youtube.com/@channel \\"
	@echo "    --name \"Module Name\" \\"
	@echo "    --description \"Module description\" \\"
	@echo "    --output ../module_directory"
	@echo ""
	@echo "# See all options:"
	@echo "./process_channel.sh --help"

# Clean temporary files
.PHONY: clean
clean:
	@echo "🧹 Cleaning temporary files..."
	@cd $(TOOLS_DIR) && rm -f *.pyc __pycache__/*.pyc
	@echo "✅ Cleaned temporary files"

# Install dependencies
.PHONY: install-deps
install-deps:
	@echo "📦 Installing dependencies..."
	pip install yt-dlp
	@echo "✅ Dependencies installed"

# Show tool help
.PHONY: help-tool
help-tool:
	@echo "📺 Channel Processor Help:"
	@echo "=========================="
	@cd $(TOOLS_DIR) && ./$(SHELL_SCRIPT) --help