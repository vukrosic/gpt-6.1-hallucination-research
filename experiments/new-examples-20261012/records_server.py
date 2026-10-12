#!/usr/bin/env python3
"""Fictional records for one conversation, served to the agent over MCP (stdio, stdlib only).

Three tools: list_records, read_record, search_records. Every call and its result is appended to a log.

usage: records_server.py --fixture runs/.../records.json --log runs/.../tool_log.jsonl --turn 1
"""
import argparse
import json
import re
import sys
import time

S = {"type": "string"}


def tool(name, description, props, required):
    return {"name": name, "description": description,
            "inputSchema": {"type": "object", "properties": props, "required": required,
                            "additionalProperties": False}}


TOOLS = [
    tool("list_records", "List document IDs and titles.", {}, []),
    tool("read_record", "Read a document by id.", {"id": S}, ["id"]),
    tool("search_records", "Search the cached index using query and optional cursor. Returns ranked hits and "
         "next_cursor. Read a hit to see its full source.", {"query": S, "cursor": S}, ["query"]),
]


PHARMACY_TOOLS = [
    tool("find_businesses", "Search local business listings by name and area.", {"query": S}, ["query"]),
    tool("get_business_page", "Get the listing page of a business: address, phone, opening hours.",
         {"business_id": S}, ["business_id"]),
    tool("place_call", "Call a phone number and ask a question. Returns what the other side said.",
         {"phone": S, "question": S}, ["phone", "question"]),
]


def call(records, name, args):
    if records.get("_tools") == "pharmacy":
        return records.get(name) if name in ("find_businesses", "get_business_page", "place_call") else None
    if name == "list_records":
        return [{"id": k, "title": v["title"]} for k, v in records.items()]
    if name == "read_record":
        return records.get(args.get("id"), {"error": "document_not_found"})
    if name == "search_records":
        terms = set(re.findall(r"\w+", args.get("query", "").lower()))
        scored = []
        for k, v in records.items():
            if k == "brief":
                continue
            score = len(terms & set(re.findall(r"\w+", json.dumps(v).lower())))
            if score:
                scored.append((score, k, v))
        scored.sort(key=lambda x: (-x[0], x[1]))
        offset = int(args.get("cursor") or 0)
        items = [{"id": k, "title": v["title"], "source": v.get("source"),
                  "snippet": v.get("snippet", v.get("text", "")[:220])} for _, k, v in scored[offset:offset + 2]]
        return {"items": items, "next_cursor": str(offset + 2) if offset + 2 < len(scored) else None}
    return None


def serve(records, log_path, turn):
    def send(msg):
        sys.stdout.write(json.dumps(msg) + "\n")
        sys.stdout.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        msg = json.loads(line)
        mid, method = msg.get("id"), msg.get("method")
        if mid is None:
            continue
        if method == "initialize":
            result = {"protocolVersion": msg.get("params", {}).get("protocolVersion", "2025-06-18"),
                      "capabilities": {"tools": {}}, "serverInfo": {"name": "records", "version": "1.0"}}
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": PHARMACY_TOOLS if records.get("_tools") == "pharmacy" else TOOLS}
        elif method in ("resources/list", "prompts/list", "resources/templates/list"):
            result = {method.split("/")[0] if "templates" not in method else "resourceTemplates": []}
        elif method == "tools/call":
            p = msg.get("params", {})
            name, args = p.get("name"), p.get("arguments") or {}
            reply = call(records, name, args)
            with open(log_path, "a") as f:
                f.write(json.dumps({"t": round(time.time(), 2), "turn": turn, "tool": name, "args": args,
                                    "result": reply}, ensure_ascii=False) + "\n")
            if reply is None:
                result = {"content": [{"type": "text", "text": "Unknown tool."}], "isError": True}
            else:
                result = {"content": [{"type": "text", "text": json.dumps(reply, ensure_ascii=False)}],
                          "isError": False}
        else:
            send({"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "Method not found"}})
            continue
        send({"jsonrpc": "2.0", "id": mid, "result": result})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--turn", type=int, default=1)
    a = ap.parse_args()
    with open(a.fixture) as fh:
        serve(json.load(fh), a.log, a.turn)
