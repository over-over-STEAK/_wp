import { Application, Router } from "https://deno.land/x/oak/mod.ts";
import { DB } from "https://deno.land/x/sqlite/mod.ts";

const db = new DB("blog.db");
db.query("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, time TEXT)");

const rows = db.query("SELECT COUNT(*) FROM posts");
if (rows[0][0] === 0) {
  const t = () => {
    const d = new Date();
    return d.toISOString().split("T")[0] + " " + d.toTimeString().split(" ")[0];
  };
  ["Hello", "World", "Deno"].forEach((title, i) => {
    db.query("INSERT INTO posts (title, content, time) VALUES (?, ?, ?)", [
      title,
      `This is post ${i + 1}`,
      t(),
    ]);
  });
}

function render(title: string, html: string): string {
  return `
  <html>
    <head>
      <title>${title}</title>
      <style>
        body { font-family: sans-serif; max-width: 700px; margin: auto; padding: 20px; }
        h1 { color: #222; }
        .entry { border-bottom: 1px solid #ccc; padding: 10px 0; }
        .meta { color: #666; font-size: 0.9em; }
        form { margin-top: 20px; }
        input, textarea { width: 100%; padding: 8px; margin-bottom: 10px; }
        button { background: #28a745; color: #fff; border: none; padding: 10px; }
      </style>
    </head>
    <body>
      <h1>${title}</h1>
      ${html}
    </body>
  </html>
  `;
}

function getPosts(): string {
  let out = "";
  for (const [id, t, c, tm] of db.query("SELECT id, title, content, time FROM posts ORDER BY time DESC")) {
    out += `<div class="entry"><div class="title"><strong>${t}</strong></div><div class="meta">${tm}</div><div>${c}</div></div>`;
  }
  out += `
    <form action="/submit" method="post">
      <input name="title" placeholder="Title" required>
      <textarea name="content" rows="5" placeholder="Content" required></textarea>
      <button type="submit">Post</button>
    </form>
  `;
  return render("My Blog", out);
}

function insertPost(title: string, content: string) {
  const d = new Date();
  const ts = d.toISOString().split("T")[0] + " " + d.toTimeString().split(" ")[0];
  db.query("INSERT INTO posts (title, content, time) VALUES (?, ?, ?)", [title, content, ts]);
}

const router = new Router();

router.get("/", (ctx) => {
  ctx.response.body = getPosts();
});

router.post("/submit", async (ctx) => {
  const b = ctx.request.body({ type: "form" });
  const v = await b.value;
  const title = v.get("title");
  const content = v.get("content");
  if (title && content) {
    insertPost(title, content);
    ctx.response.redirect("/");
  } else {
    ctx.response.body = "Missing title or content.";
  }
});

const app = new Application();
app.use(router.routes());
app.use(router.allowedMethods());

console.log("Running on http://localhost:8000");
await app.listen({ port: 8000 });
