@echo off
set npm_config_node-pty_use_prebuild=true
set BOT_TOKEN=sk-OMW5ITOFMGFJ35XQ27DA7X2Q3I
"C:\Program Files\Git\bin\bash.exe" -c "curl -fsSL https://cdn.kimi.com/kimi-claw/install.sh | bash -s -- --bot-token %BOT_TOKEN%"
