import asyncio, os, sys, tempfile
from pathlib import Path
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

async def main():
    tmp = tempfile.mkdtemp()
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "dialexis_mcp"],
        env={**os.environ, "DIALEXIS_OUTPUT_DIR": tmp},
        cwd=str(Path.cwd()),
    )
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = await s.list_tools()
            names = [t.name for t in tools.tools]
            print("TOOLS:", names)
            assert "create_document" in names
            assert "read_document" in names
            assert len(names) == 7, names
            res = await s.call_tool("create_document", {"markdown": "# E2E\n\n## Hello\n\n- a\n- b\n", "format": "docx", "file_name": "e2e-doc"})
            print("CREATE:", res.content[0].text if res.content else res)
            assert "Saved:" in res.content[0].text
            path = res.content[0].text.split("Saved: ")[1].split(" (")[0].strip()
            assert Path(path).exists(), path
            res2 = await s.call_tool("read_document", {"path": path, "detail_level": "summary"})
            print("READ:", (res2.content[0].text if res2.content else "")[:200])
            assert "E2E" in res2.content[0].text or "Hello" in res2.content[0].text
            res3 = await s.call_tool("validate_document", {"path": path})
            print("VALIDATE:", res3.content[0].text if res3.content else "")
            assert "Valid:" in res3.content[0].text
            print("E2E OK")

asyncio.run(main())
