.PHONY: smoke seal test
smoke:
	PYTHONPATH=src python3 -m crimson_os.cli smoke
seal:
	PYTHONPATH=src python3 -m crimson_os.cli seal
test:
	PYTHONPATH=src python3 -m crimson_os.cli seal
	PYTHONPATH=src python3 -m crimson_os.cli smoke
	PYTHONPATH=src python3 -m crimson_os.cli drop /tmp/crimson_bus.md HOLD
	PYTHONPATH=src python3 -m crimson_os.cli drop /tmp/crimson_bus.md DEAD --iota-off
