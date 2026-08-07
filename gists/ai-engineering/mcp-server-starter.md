# MCP Server Starter — Build a Production-Ready Model Context Protocol Server in TypeScript

A complete, typed, testable MCP server you can copy into a new repository and
ship. Covers tools, resources, input validation, error handling, transport
choice (stdio vs HTTP), and the security boundaries that matter once an AI agent
is the one calling your code.

## Why this matters

The Model Context Protocol is how an AI client — Claude Code, Claude Desktop,
an IDE extension, your own agent — discovers and calls capabilities you own.
Without it, every integration is a bespoke prompt-and-parse hack. With it, you
publish a server once and every MCP-aware client can use it.

Most MCP examples stop at a `add(a, b)` toy that returns a string. That leaves
out everything that breaks in production:

- **Unvalidated input.** The model chooses the arguments. It will send a string
  where you expected a number, and an absolute path where you expected a
  relative one.
- **Errors that kill the process.** A thrown exception in a stdio server takes
  the whole connection down instead of returning a recoverable error the model
  can read and retry.
- **Logging to stdout.** On stdio transport, stdout *is* the protocol channel. A
  stray `console.log` corrupts the JSON-RPC stream and the client silently
  disconnects.
- **No boundary.** A file tool without a root check is arbitrary file read for
  anyone who can talk to the model.

This starter handles all four.

## Complete example

### Project layout

```text
mcp-weather-server/
├── src/
│   ├── index.ts          # entry point + transport wiring
│   ├── server.ts         # server definition, tools, resources
│   └── weather.ts        # domain logic, no MCP awareness
├── package.json
└── tsconfig.json
```

Keeping `weather.ts` free of MCP types is the single most useful structural
decision here: the domain logic stays unit-testable without spinning up a
protocol server, and swapping transports never touches it.

### `package.json`

```json
{
  "name": "mcp-weather-server",
  "version": "1.0.0",
  "type": "module",
  "bin": { "mcp-weather-server": "./dist/index.js" },
  "files": ["dist"],
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "inspect": "npx @modelcontextprotocol/inspector node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "typescript": "^5.6.0"
  }
}
```

`"type": "module"` is required — the SDK ships ESM. The `bin` entry is what lets
users run your server with `npx` instead of cloning it.

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src/**/*"]
}
```

`"module": "Node16"` matters: it makes TypeScript enforce the `.js` extensions
in relative imports that ESM requires at runtime.

### `src/weather.ts` — domain logic

```ts
/** Plain domain layer. No MCP imports, so it stays trivially unit-testable. */

export interface Forecast {
  location: string;
  temperatureC: number;
  condition: string;
  updatedAt: string;
}

export class UpstreamError extends Error {
  constructor(
    message: string,
    readonly status?: number,
  ) {
    super(message);
    this.name = "UpstreamError";
  }
}

export async function fetchForecast(
  location: string,
  signal?: AbortSignal,
): Promise<Forecast> {
  const url = new URL("https://api.example.com/v1/forecast");
  url.searchParams.set("q", location);

  const response = await fetch(url, {
    signal,
    headers: { authorization: `Bearer ${requireEnv("WEATHER_API_KEY")}` },
  });

  if (!response.ok) {
    throw new UpstreamError(
      `Forecast lookup failed for "${location}"`,
      response.status,
    );
  }

  const data = (await response.json()) as {
    temp_c: number;
    condition: string;
  };

  return {
    location,
    temperatureC: data.temp_c,
    condition: data.condition,
    updatedAt: new Date().toISOString(),
  };
}

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    // Fail at startup, not on the first tool call — a server that boots
    // successfully and then fails every request is much harder to debug.
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}
```

### `src/server.ts` — the MCP surface

```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { fetchForecast, UpstreamError } from "./weather.js";

export function createServer(): McpServer {
  const server = new McpServer({
    name: "weather",
    version: "1.0.0",
  });

  server.registerTool(
    "get_forecast",
    {
      title: "Get weather forecast",
      // The description is the model's only guide to when this tool applies.
      // Say when to call it, not just what it does.
      description:
        "Get the current weather forecast for a city. Call this when the " +
        "user asks about current or upcoming weather conditions for a " +
        "named location. Returns temperature in Celsius and a condition " +
        "summary. Does not provide historical weather.",
      inputSchema: {
        location: z
          .string()
          .min(1)
          .max(120)
          .describe("City name, optionally with region: 'Ahmedabad, IN'"),
        units: z
          .enum(["celsius", "fahrenheit"])
          .default("celsius")
          .describe("Temperature unit for the response"),
      },
    },
    async ({ location, units }) => {
      try {
        const forecast = await fetchForecast(location);
        const temp =
          units === "fahrenheit"
            ? forecast.temperatureC * 1.8 + 32
            : forecast.temperatureC;

        return {
          // Structured content is machine-readable; the text block is what
          // the model reads. Returning both serves clients of either kind.
          structuredContent: { ...forecast, temperature: temp, units },
          content: [
            {
              type: "text",
              text: `${forecast.location}: ${temp.toFixed(1)}° ${
                units === "celsius" ? "C" : "F"
              }, ${forecast.condition} (as of ${forecast.updatedAt})`,
            },
          ],
        };
      } catch (error) {
        // Return an error result rather than throwing. A thrown error is a
        // protocol-level failure the model cannot see or recover from; an
        // isError result is text it can read and act on.
        return {
          isError: true,
          content: [{ type: "text", text: describeError(error) }],
        };
      }
    },
  );

  server.registerResource(
    "supported-regions",
    "weather://regions",
    {
      title: "Supported regions",
      description: "The list of regions this server can return forecasts for.",
      mimeType: "application/json",
    },
    async (uri) => ({
      contents: [
        {
          uri: uri.href,
          mimeType: "application/json",
          text: JSON.stringify(["IN", "US", "GB", "AU"], null, 2),
        },
      ],
    }),
  );

  return server;
}

function describeError(error: unknown): string {
  if (error instanceof UpstreamError) {
    return error.status === 404
      ? "No forecast found for that location. Check the spelling, or try a larger nearby city."
      : `The weather service is unavailable (status ${error.status ?? "unknown"}). Retrying in a moment may succeed.`;
  }
  // Never leak a raw stack trace into model context: it is noise at best and
  // an information disclosure at worst.
  return "The forecast lookup failed for an unexpected reason.";
}
```

### `src/index.ts` — transport wiring

```ts
#!/usr/bin/env node
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createServer } from "./server.js";

async function main() {
  const server = createServer();
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // stdout is the JSON-RPC channel. All human-readable output goes to stderr.
  console.error("weather MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal:", error);
  process.exit(1);
});
```

## Explanation

**Registration shape.** `registerTool(name, config, handler)` takes a Zod raw
shape (a plain object of Zod validators, not `z.object({...})`) as
`inputSchema`. The SDK converts it to the JSON Schema the client sees and
validates incoming arguments against it before your handler runs — so
`({ location, units })` is already typed and checked.

**`.describe()` earns its place.** Each field's description ships in the schema
the model reads. A parameter named `units` with no description is a coin flip;
one that says `"Temperature unit for the response"` is not.

**Two-channel results.** `content` is what the model reads. `structuredContent`
is what a programmatic client parses. Returning both costs a few tokens and
makes the server useful to either consumer.

**Errors are values, not exceptions.** `{ isError: true, content: [...] }`
returns to the model as readable text it can act on. A thrown exception
propagates as a protocol error the model never sees, and on stdio it can drop
the connection entirely.

**Transports.** `StdioServerTransport` is right for local servers launched by
the client as a subprocess — the common case, and the one Claude Desktop and
Claude Code use. Use the Streamable HTTP transport instead when the server is a
remote, multi-client service; then you own authentication, session state, and
CORS, none of which stdio requires.

## Usage

Register the server with any MCP client. For Claude Code:

```bash
claude mcp add weather --env WEATHER_API_KEY=sk-... -- npx -y mcp-weather-server
```

For Claude Desktop, in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "npx",
      "args": ["-y", "mcp-weather-server"],
      "env": { "WEATHER_API_KEY": "sk-..." }
    }
  }
}
```

Before shipping, drive it manually with the official inspector — it lists your
tools, shows the generated JSON Schema, and lets you invoke each one:

```bash
npm run build && npm run inspect
```

## Best practices

- **Write tool descriptions for the model, not for a changelog.** State the
  trigger condition ("Call this when the user asks about…") and the boundary
  ("Does not provide historical weather"). Trigger conditions measurably
  improve when a model reaches for the right tool.
- **Keep the tool surface small.** Ten sharp tools beat forty overlapping ones.
  Every schema is loaded into context on every request, and near-duplicate tools
  make the choice ambiguous.
- **Return high-signal payloads.** Don't pipe a 4,000-line API response into
  context. Project the fields that matter.
- **Validate at the boundary, then trust.** Zod at the tool edge; plain typed
  functions inside.
- **Version the server.** Clients surface it, and it is the only handle users
  have when reporting a bug.
- **Fail fast on missing configuration.** A server that starts without its API
  key and fails every call wastes a debugging session.

## Common mistakes

| Mistake | What happens | Fix |
| --- | --- | --- |
| `console.log` in a stdio server | Corrupts the JSON-RPC stream; client disconnects with no error | Use `console.error` — stderr is free |
| Throwing from a tool handler | Model sees a protocol failure, cannot recover | Return `{ isError: true, content: [...] }` |
| `z.object({...})` as `inputSchema` | Schema nests one level too deep; arguments never match | Pass the raw shape: `{ location: z.string() }` |
| Omitting `.js` in relative imports | `ERR_MODULE_NOT_FOUND` at runtime, compiles fine | `import { createServer } from "./server.js"` |
| Missing `"type": "module"` | `Cannot use import statement outside a module` | Set it in `package.json` |
| Returning raw upstream JSON | Burns context, buries the answer | Project to the fields the model needs |
| Secrets as tool parameters | The model can see, log, and echo them | Read from `process.env` server-side |

## Performance considerations

- **Schemas are a per-request cost.** Every tool definition is serialized into
  the model's context on every turn. A server with 40 tools taxes each request
  before any work happens. Split large surfaces into multiple focused servers a
  client can enable selectively.
- **Cache what does not change.** Region lists, taxonomies, and schema lookups
  belong behind an in-process cache with a TTL, not a network round trip per
  call.
- **Set timeouts and pass `AbortSignal` through.** A tool call with no timeout
  can hang the agent's turn indefinitely. Thread the signal from the handler
  into `fetch`.
- **Prefer resources over tools for static reference data.** Resources are read
  on demand by the client instead of occupying the tool list.

## Security considerations

An MCP server is a privilege boundary. The arguments are chosen by a model,
which may be acting on untrusted input from a web page, an issue comment, or a
file. Treat every argument as hostile.

- **Confine filesystem access to a root.** Resolve the model-supplied path to
  its canonical form and verify it stays inside your project root — reject
  `..`, symlinks, and absolute paths that escape:

  ```ts
  import { realpath } from "node:fs/promises";
  import { resolve, relative, isAbsolute } from "node:path";

  async function safeResolve(root: string, userPath: string): Promise<string> {
    const candidate = resolve(root, userPath);
    const real = await realpath(candidate).catch(() => candidate);
    const rel = relative(await realpath(root), real);
    if (rel.startsWith("..") || isAbsolute(rel)) {
      throw new Error("Path escapes the permitted root");
    }
    return real;
  }
  ```

- **Never interpolate arguments into a shell.** Use `execFile` with an argument
  array, never `exec` with a template string.
- **Parameterize every query.** Model-chosen values in SQL are SQL injection
  with extra steps.
- **Keep credentials server-side.** Read them from the environment; never accept
  them as tool parameters and never echo them in a result.
- **Gate destructive operations.** Deletes, sends, payments, and writes to
  shared state should require explicit human confirmation in the client rather
  than executing on the model's say-so.
- **Scope the credential minimally.** The server can do whatever its API key
  allows. A read-only key limits the blast radius of a bad turn.

## Related resources

- [Model Context Protocol specification](https://modelcontextprotocol.io)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp)

## Related Gists to create next

1. **MCP Server Testing** — unit-testing tools with the in-memory transport.
2. **MCP Streamable HTTP Transport** — remote servers, auth, and sessions.
3. **Claude Code Best Practices** — `CLAUDE.md`, skills, hooks, subagents.
4. **Anthropic API Integration in TypeScript** — tool use loop and streaming.
5. **AI Chat Application with the Vercel AI SDK** — streaming UI end to end.
