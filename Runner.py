import  contextlib
import io, asyncio

def _execute_code(code: str, globals_dict: dict, stdout: io.StringIO, stderr: io.StringIO):
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exec(code, globals_dict)

async def execute(code: str, globals_dict: dict, timeout: float = 10):
    stdout = io.StringIO()
    stderr = io.StringIO()
    loop = asyncio.get_running_loop()
    try:
        await asyncio.wait_for(
            loop.run_in_executor(None, _execute_code, code, globals_dict, stdout, stderr),
            timeout=timeout
        )
        return stdout.getvalue(), stderr.getvalue(), None
    except asyncio.TimeoutError:
        return stdout.getvalue(), stderr.getvalue(), "Execution timed out"
    except Exception as e:
        return stdout.getvalue(), stderr.getvalue(), str(e)
