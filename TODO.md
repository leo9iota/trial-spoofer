# TODO

## Critical Issues

### Completed
- [x] **Fix missing root_check function**
  - **File:** `src/main.py:24`
  - **Issue:** ImportError - `root_check` doesn't exist in `core.system`
  - **Fix:** Import `check_root` from `core.helpers` instead

- [x] **Fix missing get_identifiers function**
  - **File:** `src/main.py:208` and `src/ui/table.py:3`
  - **Issue:** ImportError - `get_identifiers` doesn't exist in `core.system`
  - **Fix:** Import `get_identifiers` from `core.helpers` in both files

- [x] **Fix incorrect function calls in feature mapping**
  - **File:** `src/main.py:44-46`
  - **Issue:** TypeError - Functions called immediately with `()` instead of stored as references
  - **Fix:** Remove parentheses and use lambda for `spoof_vscode`: `lambda: spoof_vscode(self.home_path)`

### In Progress
- [ ] **Add missing check_system_requirements method**
  - **File:** `src/main.py:94`
  - **Issue:** AttributeError - `'Main' object has no attribute 'check_system_requirements'`
  - **Current Error:** Application crashes after banner display

- [ ] **Add missing feature_steps variable**
  - **File:** `src/main.py:68`
  - **Issue:** NameError - `feature_steps` is not defined when executing features
  - **Impact:** Progress display will fail when running spoofing operations

- [ ] **Add missing draw_main_menu method**
  - **File:** `src/main.py:111`
  - **Issue:** AttributeError - `'Main' object has no attribute 'draw_main_menu'`
  - **Impact:** Main menu won't display after system checks pass

- [ ] **Add missing imports for system functions**
  - **File:** `src/main.py:25`
  - **Issue:** NameError - `change_hostname` and `create_new_user` used but not imported
  - **Impact:** Hostname and User Account spoofing features will fail

---

## System

- [ ] Implement `update_boot_config()` function
- [ ] Implement additional rail guards

## Fix

- [ ] Fix rerender of panel component in progress display