-- Force every table to fit \linewidth by giving columns proportional widths
-- estimated from the text length of header + body cells. Prevents the
-- overflow/clipping that happens when pandoc emits natural-width columns.

local function cell_len(cell)
  -- cell is a list of blocks; stringify and take length
  local s = pandoc.utils.stringify(cell)
  return utf8.len(s) or #s
end

function Table(tbl)
  local ncol = #tbl.colspecs
  if ncol == 0 then return tbl end

  -- gather max-ish content length per column (use a soft cap so one long
  -- cell doesn't dominate; weight header a bit higher)
  local weight = {}
  for i = 1, ncol do weight[i] = 1 end

  local head = tbl.head
  if head and head.rows then
    for _, row in ipairs(head.rows) do
      for i, c in ipairs(row.cells) do
        weight[i] = math.max(weight[i], cell_len(c.contents) * 1.15)
      end
    end
  end
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do
      for i, c in ipairs(row.cells) do
        if i <= ncol then
          local l = cell_len(c.contents)
          if l > 40 then l = 40 + (l - 40) * 0.45 end  -- soft cap
          weight[i] = math.max(weight[i], l)
        end
      end
    end
  end

  local total = 0
  for i = 1, ncol do
    if weight[i] < 4 then weight[i] = 4 end          -- floor
    total = total + weight[i]
  end

  for i = 1, ncol do
    local frac = weight[i] / total
    if frac < 0.06 then frac = 0.06 end              -- keep readable min
    tbl.colspecs[i][1] = pandoc.AlignDefault
    tbl.colspecs[i][2] = frac
  end
  return tbl
end
