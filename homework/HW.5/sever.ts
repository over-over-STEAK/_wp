import { serve } from "https://deno.land/std@0.203.0/http/server.ts";
import { DB } from "https://deno.land/x/sqlite/mod.ts";

const db = new DB("blog.db");

db.query(`
  CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    user TEXT,
    time DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

const initialPosts = [
  { title: "Exam week has arrived", content: "Hopefully I will be successful, I should be able to do all the exams.", user: "By Edi" },
  { title: "Does anyone have this?", content: "If you have an algebra book, I really need it. Meet me at the library today.", user: "By Tana" },
  { title: "Need to eat a lot!", content: "Yes, I need a lot of food intake before the exam.", user: "By Cava" }
];

for (const post of initialPosts) {
  db.query("INSERT INTO posts (title, content, user) VALUES (?, ?, ?)", [
    post.title,
    post.content,
    post.user
  ]);
}

serve(async (req) => {
  const url = new URL(req.url);

  if (req.method === "GET" && url.pathname === "/") {
    const posts = [...db.query("SELECT title, content, user, time FROM posts ORDER BY time DESC")];
    const html = `
      <!DOCTYPE html>
      <html>
        <head><meta charset="UTF-8"><title>My Blog</title></head>
        <body>
          <h1>📝 貼文牆</h1>
          ${posts.map(([title, content, user, time]) => `
            <div style="margin-bottom:1em;">
              <h3>${title}</h3>
              <p>${content}</p>
              <small>${user} | ${time}</small>
            </div>
          `).join("")}
          <hr>
          <h2>➕ 新增貼文</h2>
          <form action="/post" method="POST">
            <input name="title" placeholder="標題" required><br><br>
            <textarea name="content" placeholder="內容" required></textarea><br><br>
            <input name="user" placeholder="署名" required><br><br>
            <button type="submit">送出</button>
          </form>
        </body>
      </html>
    `;
    return new Response(html, { headers: { "Content-Type": "text/html" } });
  }

  if (req.method === "POST" && url.pathname === "/post") {
    const form = await req.formData();
    const title = form.get("title")?.toString() ?? "";
    const content = form.get("content")?.toString() ?? "";
    const user = form.get("user")?.toString() ?? "";

    if (title && content && user) {
      db.query("INSERT INTO posts (title, content, user) VALUES (?, ?, ?)", [title, content, user]);
    }

    return Response.redirect("/", 303);
  }

  return new Response("404 Not Found", { status: 404 });
});
