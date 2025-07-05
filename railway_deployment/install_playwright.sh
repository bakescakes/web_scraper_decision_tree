#!/bin/bash
# Playwright browser installation for Railway deployment

echo "🚀 Installing Playwright browsers for production..."

# Install Playwright browsers with dependencies
playwright install chromium
playwright install-deps chromium

echo "✅ Playwright browser installation complete"