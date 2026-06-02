#!/bin/zsh
# runbook_updater_launcher.sh
# Wrapper so launchd can run the runbook updater with correct shell environment
export PATH="/usr/bin:/bin:/usr/sbin:/sbin"
exec /usr/bin/python3 "/Users/edknowlt/Documents/ICR_Automation/_Runbook/runbook_updater.py"
