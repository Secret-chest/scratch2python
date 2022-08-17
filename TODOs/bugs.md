## ✅ Finished

- [x] `block.script` is not filled correctly
- [x] Keypress event block is marked as not ran too early
- [x] Keypress event block should be marked as not ran only when the last block in the script is done
- [x] Use `block.top` to detect the event which needs to be marked
- [x] Wait blocks below key events don't work
- [x] Key repeat doesn't apply
- [x] Keys which have ASCII codes don't work

## ❎ In progress

- [ ] Reject key events for a block already running
- [ ] Revisit keypress checks
- [ ] Empty key events set (all keys!)
- [ ] Cannot use multiple event handlers for one key
- [ ] Sprite fencing is wrong