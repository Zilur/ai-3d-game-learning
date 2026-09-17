extends "res://tests/practical_labs.gd"
## Exercise real controls and their runtime evidence. This does not measure learning.

func run() -> void:
	print("Discovery suite: ", Engine.get_version_info().get("string"))
	var lab = await open_scene("res://labs/event_lab.tscn")
	check(not lab.mechanism_visible and not lab.mechanism_view.visible, "mechanism starts folded")
	check(not lab.controls["guard"].visible, "fault control starts folded")
	check(lab.counter_view.visible and lab.count == 0 and not lab.taken, "neutral baseline with ordinary counter")
	check(lab.history.is_empty() and not "taken=" in lab.status.text, "opening does not disclose state explanation")

	lab.controls["visual"].button_pressed = true
	check(not lab.token.visible and lab.count == 0 and not lab.taken, "hiding appearance alone does not collect")
	check(lab.history.is_empty(), "view controls do not inject requests")
	lab.controls["wrong"].pressed.emit()
	check(lab.count == 0 and not lab.taken, "wrong actor rejected even with invisible item")
	check(lab.history.size() == 1 and not lab.history[0]["accepted"], "rejected request is actually recorded")
	check(lab.history[0]["before_count"] == 0 and lab.history[0]["after_count"] == 0, "rejection records unchanged state")

	lab.controls["counter"].button_pressed = false
	lab.controls["feedback"].button_pressed = false
	lab.controls["collect"].pressed.emit()
	check(lab.count == 1 and lab.taken, "request still changes state while displays are hidden")
	check(not lab.counter_view.visible and not lab.feedback.visible, "real counter and feedback are hidden separately")
	var accepted: Dictionary = lab.history[1]
	check(accepted["accepted"] and accepted["before_count"] == 0 and accepted["after_count"] == 1, "trace records actual count transition")
	check(not accepted["before_taken"] and accepted["after_taken"], "trace records actual taken transition")
	lab.controls["counter"].button_pressed = true
	check(lab.counter_view.visible and lab.counter_view.text == "计数 1", "revealing counter displays authoritative current value")
	lab.controls["mechanism"].button_pressed = true
	check(lab.mechanism_view.visible and lab.controls["guard"].visible, "evidence and deliberate fault become accessible")
	check("count 0→1" in lab.mechanism_view.text and "装饰球" in lab.mechanism_view.text, "same runtime trace is rendered")
	var trace_before: Array = lab.history.duplicate(true)
	lab.controls["mechanism"].button_pressed = false
	check(lab.history == trace_before and lab.count == 1, "reading or folding evidence cannot mutate the experiment")
	lab.controls["visual"].button_pressed = false
	check(not lab.token.visible, "revealing appearance does not resurrect a collected item")

	lab.controls["restart"].pressed.emit()
	check(lab.count == 0 and not lab.taken and lab.history.is_empty(), "round restart clears state and evidence")
	check(not lab.feedback_enabled and not lab.mechanism_visible, "round restart keeps deliberate view settings")
	lab.controls["double"].pressed.emit()
	check(lab.history.size() == 2 and lab.history[0]["accepted"] and not lab.history[1]["accepted"], "two requests have ordered distinct outcomes")
	check(lab.history[1]["before_count"] == 1 and lab.history[1]["after_count"] == 1, "duplicate rejection does not manufacture a transition")
	lab.controls["mechanism"].button_pressed = true
	lab.controls["guard"].button_pressed = false
	lab.controls["collect"].pressed.emit()
	check(lab.count == 2 and not lab.history[-1]["guard"], "explicit fault really permits another reward and records its setting")
	lab.controls["wrong"].pressed.emit()
	check(lab.count == 2 and not lab.history[-1]["accepted"], "fault does not silently disable actor filtering")
	lab.controls["restart"].pressed.emit()
	check(not lab.guard_enabled and not lab.feedback_enabled and lab.mechanism_visible, "restart preserves fault and views as labelled")
	lab.controls["reset"].pressed.emit()
	await steps(6)
	lab = current_scene
	check(lab.guard_enabled and lab.feedback_enabled and lab.counter_visible and not lab.visual_hidden, "full reset restores all experiment settings")
	check(not lab.mechanism_visible and lab.history.is_empty() and lab.request_number == 0, "full reset folds explanations and clears history")
	check(lab.token.visible and lab.count == 0 and not lab.taken, "full reset restores original world")
	for i in range(30):
		lab.controls["collect"].pressed.emit()
	check(lab.history.size() == lab.HISTORY_LIMIT and lab.request_number == 30, "history is bounded without resetting sequence")
	check(lab.history[0]["number"] == 19 and lab.history[-1]["number"] == 30 and lab.count == 1, "bounded history preserves correct recent records and gameplay")

	if is_instance_valid(current_scene):
		current_scene.queue_free()
		current_scene = null
	await process_frame
	if failures.is_empty():
		print("DISCOVERY LAB PASS: %d assertions; engine behavior only" % checks)
		quit(0)
	else:
		print("DISCOVERY LAB FAIL: %d / %d" % [failures.size(), checks])
		quit(1)
