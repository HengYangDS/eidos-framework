import asyncio
import traceback
from typing import Any
from ..intelligence.driver import CognitiveDriver, OpenAIDriver
from ..system.logging import get_logger
from .telemetry import trace_span

logger = get_logger(__name__)

class Sidecar:
    """
    The Healer Daemon (Eidos Nous).
    Monitors the system and uses AI to fix issues.
    """
    def __init__(self, driver: CognitiveDriver | None = None):
        self.driver = driver or OpenAIDriver()
        
    @trace_span("sidecar.heal")
    async def heal(self, error: Exception, context: Any) -> str:
        """
        Attempts to heal a runtime error.
        """
        logger.error("Intercepted error", error=str(error))
        
        # Capture full traceback
        tb_str = "".join(traceback.format_exception(type(error), error, error.__traceback__))
        
        logger.info("Analyzing error", driver=type(self.driver).__name__)
        
        diagnosis = await self.driver.diagnose_error(tb_str, context)
        logger.info("Diagnosis received", diagnosis=diagnosis)
        
        # Realization: Persist the patch
        self._persist_patch(diagnosis)
        
        return diagnosis

    def _persist_patch(self, content: str):
        from pathlib import Path
        import time
        
        patch_dir = Path("patches")
        try:
            patch_dir.mkdir(exist_ok=True)
            filename = f"patch_{int(time.time())}.py"
            (patch_dir / filename).write_text(f"# Auto-generated Patch by Eidos Sidecar\n\n{content}", encoding="utf-8")
            logger.info("Patch saved", path=str(patch_dir / filename))
        except Exception as e:
            logger.error("Failed to save patch", error=str(e))

    async def run_daemon(self):
        logger.info("Daemon started. Watching for signals...")
        
        # Structured Concurrency (Python 3.11+)
        # Using TaskGroup to manage the lifecycle of background tasks
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(self._monitor_loop())
        except Exception as e:
            logger.exception("Daemon crashed", error=str(e))

    async def _monitor_loop(self):
        """
        Simulated event loop for monitoring system health.
        """
        while True:
            # In a real system, this would check a queue or shared memory
            await asyncio.sleep(1)
