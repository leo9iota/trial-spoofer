# TODO

## Critical Issues (Application Won't Run)

### Completed
- [x] Fix missing root_check function - Import check_root from core.helpers instead of root_check from core.system
- [x] Fix missing get_identifiers function - Import get_identifiers from core.helpers and fix ui/table.py import

### In Progress
- [ ] Fix incorrect function calls in feature mapping - Lines 43-45 in main.py call functions instead of storing function references (change_hostname(), spoof_vscode(), create_new_user())
- [ ] Add missing feature_steps variable - Line 67 references feature_steps.get() but feature_steps is not defined
- [ ] Add missing check_system_requirements method - Line 93 calls self.check_system_requirements() but this method doesn't exist in Main class
- [ ] Add missing draw_main_menu method - Line 111 calls self.draw_main_menu() but this method doesn't exist in Main class
- [ ] Fix spoof_vscode function signature issue - spoof_vscode expects a home parameter but is called without arguments
- [ ] Add missing imports for system functions - change_hostname and create_new_user are used but not imported from core.system

---
## System

- [ ] Implement `update_boot_config()` function
- [ ] Implement additional rail guards

---
## Fix

- [ ] Fix rerender of panel component in progress display