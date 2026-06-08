from src.tool_execution import _strip_stderr_dup_from_output, _subprocess_tool_result


def test_subprocess_tool_result_keeps_stdout_and_stderr_separate():
    out = _subprocess_tool_result("hello", "OpenAI Codex v0.137.0\n--------", 0)
    assert out["stdout"] == "hello"
    assert "Codex" in out["stderr"]
    assert out["output"] == "hello"
    assert "STDERR:" not in out["output"]


def test_strip_stderr_dup_removes_trailing_stderr_block_in_stream():
    stream = (
        "! OpenAI Codex v0.137.0\n"
        "! --------\n"
        "! workdir: C:\\project\n"
        "Analysis complete.\n"
    )
    combined = (
        "Analysis complete.\n"
        "STDERR: OpenAI Codex v0.137.0\n"
        "--------\n"
        "workdir: C:\\project"
    )
    cleaned = _strip_stderr_dup_from_output(combined, stream)
    assert cleaned == "Analysis complete."
    assert "STDERR:" not in cleaned
    assert "Codex" not in cleaned
