-- Tag each code block with a human-readable language label, emitted as a
-- \setcodelang{...} just before the block. interviewstyle.sty's code card
-- shows it in the top-right of the macOS-style window title bar.

local DISP = {
  python="Python", py="Python", python3="Python",
  cpp="C++", ["c++"]="C++", cxx="C++", cc="C++",
  c="C", java="Java", kotlin="Kotlin", scala="Scala",
  javascript="JavaScript", js="JavaScript", jsx="JavaScript",
  typescript="TypeScript", ts="TypeScript", tsx="TypeScript",
  go="Go", golang="Go", rust="Rust", rs="Rust", ruby="Ruby", rb="Ruby",
  php="PHP", swift="Swift", csharp="C#", cs="C#",
  sql="SQL", bash="Bash", sh="Shell", shell="Shell", zsh="Shell", console="Shell",
  json="JSON", yaml="YAML", yml="YAML", toml="TOML", xml="XML",
  html="HTML", css="CSS", scss="SCSS",
  dockerfile="Dockerfile", docker="Dockerfile", makefile="Makefile",
  hcl="HCL", terraform="Terraform", tf="Terraform",
  proto="Protobuf", protobuf="Protobuf", graphql="GraphQL",
  promql="PromQL", lua="Lua", r="R", matlab="MATLAB", perl="Perl",
  ini="INI", cfg="Config", conf="Config", text="", txt="", [""]="",
}

local function escape(s)
  -- minimal LaTeX escaping for the label (e.g. C#, C++)
  s = s:gsub("\\", "\\textbackslash{}")
  s = s:gsub("([#%%&_{}$])", "\\%1")
  return s
end

function CodeBlock(cb)
  local cls = cb.classes[1] or ""
  local label = DISP[cls:lower()]
  if label == nil then
    label = cls:sub(1,1):upper() .. cls:sub(2)   -- title-case unknown langs
  end
  local raw = pandoc.RawBlock("latex", "\\setcodelang{" .. escape(label) .. "}")
  return { raw, cb }
end
