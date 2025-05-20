const http = require("http");
const fs = require("fs");
const path = require("path");

const htmlTemplate = (content) => `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>關於我</title>
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <div class="container">
    <h1>歡迎來到我的個人介紹</h1>
    <ol>
      <li><a href="/name">姓名</a></li>
      <li><a href="/age">年齡</a></li>
      <li><a href="/gender">性別</a></li>
      <li><a href="/university">大學</a></li>
      <li><a href="/ID">學號</a></li>
    </ol>
    ${content}
  </div>
</body>
</html>`;

const server = http.createServer((req, res) => {
  const { url } = req;

  if (url === "/") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(htmlTemplate(""));
  } else if (url === "/name") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(htmlTemplate("<h2>姓名：林家煒</h2>"));
  } else if (url === "/age") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(htmlTemplate("<h2>年齡：19 歲</h2>"));
  } else if (url === "/gender") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(htmlTemplate("<h2>性別：男性</h2>"));
  } else if (url === "/university") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(htmlTemplate("<h2>大學：國立金門大學</h2>"));
  } else if (url === "/ID") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(htmlTemplate("<h2>學號：111210564</h2>"));
  } else if (url === "/styles.css") {
    const cssPath = path.join(__dirname, "styles.css");
    fs.readFile(cssPath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end("CSS not found");
      } else {
        res.writeHead(200, { "Content-Type": "text/css" });
        res.end(data);
      }
    });
  } else {
    res.writeHead(404, { "Content-Type": "text/html" });
    res.end(htmlTemplate("<h2 style='color:red'>404 頁面不存在</h2>"));
  }
});

server.listen(8000, () => {
  console.log("Server running at http://localhost:8000");
});
