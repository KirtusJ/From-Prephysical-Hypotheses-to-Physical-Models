"""Run disposable Stage 2 fixtures. Uses the Python interface to the Rust Wasmtime engine."""
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

import wasmtime as wasm


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    config = wasm.Config()
    config.consume_fuel = True
    engine = wasm.Engine(config)

    def prepare(source):
        data = bytes(wasm.wat2wasm(source))
        return data, wasm.Module(engine, data)

    def link(module):
        store = wasm.Store(engine)
        store.set_limits(memory_size=65536, memories=1, instances=1)
        store.set_fuel(10000)
        return store, wasm.Linker(engine).instantiate(store, module)

    results = {}
    # A regular subprocess can read files accessible to the invoking Windows user, even
    # with a fresh working directory and a zero-file-permissions declaration.
    with TemporaryDirectory() as root:
        path = Path(root)
        private = path / "sibling.txt"
        private.write_text("only-this-fixture", encoding="utf-8")
        work = path / "guest"
        work.mkdir()
        code = "import sys; from pathlib import Path; print(Path(sys.argv[1]).read_text())"
        ordinary = subprocess.run([sys.executable, "-I", "-c", code, str(private)],
                                  cwd=work, capture_output=True, check=True, timeout=10)
        require(ordinary.stdout.strip() == b"only-this-fixture", "native control")
        results["ordinary_subprocess_read_sibling"] = True

    arithmetic, module = prepare('(module (func (export "run") (param i32 i32) (result i32) local.get 0 local.get 1 i32.mul))')
    store, instance = link(module)
    value = instance.exports(store)["run"](store, 7, 6)
    require(value == 42, "arithmetic control")
    results["arithmetic"] = dict(result=value, wasm_sha256=sha256(arithmetic).hexdigest())

    for name, params in (("path_open", "i32 i32 i32 i32 i32 i64 i64 i32 i32"),
                         ("sock_accept", "i32 i32 i32")):
        _, guest = prepare(f'(module (import "wasi_snapshot_preview1" "{name}" (func (param {params}) (result i32))))')
        try:
            link(guest)
        except wasm.WasmtimeError as e:
            require(name in str(e) and "unknown import" in str(e), "unexpected refusal")
            results[name] = "unavailable at instantiation"
        else:
            raise RuntimeError(name + " unexpectedly linked")

    _, guest = prepare('(module (memory 1 3) (func (export "grow") (result i32) i32.const 1 memory.grow))')
    store, instance = link(guest)
    require(instance.exports(store)["grow"](store) == -1, "guest exceeded one Wasm page")
    results["grow_beyond_one_page"] = "refused"

    _, guest = prepare('(module (func (export "run") (loop br 0)))')
    store, instance = link(guest)
    try:
        instance.exports(store)["run"](store)
    except wasm.Trap as e:
        require(e.trap_code == wasm.TrapCode.OUT_OF_FUEL, "wrong loop failure")
        results["loop"] = "fuel exhausted"
    else:
        raise RuntimeError("loop completed unexpectedly")
    print(json.dumps(dict(wasmtime=version("wasmtime"), results=results), indent=2))


if __name__ == "__main__":
    main()
