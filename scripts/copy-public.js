const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const src = path.join(root, "portfolio", "public");
const dest = path.join(root, "public");

// intro.png: 루트에 있으면 portfolio/public에 먼저 넣어서 복사 흐름에 포함
const introPngRoot = path.join(root, "intro.png");
if (fs.existsSync(introPngRoot)) {
  const introDest = path.join(src, "intro.png");
  if (!fs.existsSync(src)) fs.mkdirSync(src, { recursive: true });
  fs.copyFileSync(introPngRoot, introDest);
  console.log("intro.png -> portfolio/public");
}

function copyRecursive(srcDir, destDir) {
  if (!fs.existsSync(srcDir)) {
    console.error("Source does not exist:", srcDir);
    process.exit(1);
  }
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }
  const entries = fs.readdirSync(srcDir, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(srcDir, entry.name);
    const destPath = path.join(destDir, entry.name);
    if (entry.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

copyRecursive(src, dest);

// intro.png: 루트에서 public으로 직접 복사 (fallback)
if (fs.existsSync(introPngRoot)) {
  fs.copyFileSync(introPngRoot, path.join(dest, "intro.png"));
  console.log("intro.png -> public");
}

console.log("public folder copied successfully");
