
이전에는 VSCode를 자주 사용했었습니다. 깔끔한 인터페이스와 확장 기능이 편리해서 VSCode 외의 개발 도구는 거의 사용하지 않았습니다. 그런데 최근 확장 기능이 원활하게 동작하지 않았습니다. 일시적인 문제이겠거니 했지만, 시간이 흘러도 같은 문제가 사라지지 않았습니다. 단순한 파일 탐색기 기능도 무한 로딩에 빠져서 사실상 코드 편집 외에 모든 기능은 터미널로 직접 실행해야 했습니다. 저는 결국 VSCode를 버리고 Cursor를 선택했습니다. Cursor는 LLM 지원 기능이 강력해서 개발 생산성에 큰 도움을 주었습니다. 그러나 Cursor는 오래 사용하지 않았습니다. 매달 Claude를 결제하고 있는데, Cursor를 위한 고정 지출이 추가되는 것은 불필요한 중복이라고 생각했습니다.

사실 이전부터 VSCode에 실증을 느끼고 있었습니다. VSCode에 무언가 단점이 있어서가 아니라, 터미널과 vim의 Nerd같은 매력 때문입니다. VSCode에 문제가 생겼을 때 해결을 하지 못한 것이 아니라 이미 마음 떠난 VSCode를 사용하기 위해 노력하고 싶지 않았습니다. 단지 vim을 메인 개발 도구로 사용하기에는 불편하기 때문에 진작 이동하지 않았던 것입니다. Neovim도 막연히 vim이랑 비슷하게 불편할 것이라 생각했습니다.

Neovim의 생태계가 생각 이상으로 훨씬 방대해서 배우기 수월했습니다. Lazyvim 등 잘 만들어진 플러그인 관리 도구도 있었습니다. Lazyvim을 사용하기 위해 겸사겸사 iTerm2와 Nerd Font도 처음 사용해봤습니다. iTerm2은 설정이 다양해서 마음에 들었지만, D2Coding Font는 마음에 들지 않았습니다. 결국 ASCII 외의 문자만 D2Coding으로 하고 영어는 Monaco를 유지했습니다.

Lazyvim은 기능이 너무 많고 복잡했습니다. UI 설정 몇 개 수정하다 보니, 처음부터 제 자신만의 Neovim을 설정하는 게 낫다는 결론을 내렸습니다. 자동완성 기능도 없는 최소한의 Neovim을 구성하고 싶었습니다. 

아래는 저의 init.lua 파일입니다.

```lua
vim.g.mapleader = " "  -- 스페이스를 leader 키로 설정
vim.g.maplocalleader = " "
vim.api.nvim_set_keymap('n', '<leader>e', ':NvimTreeToggle<CR>', { noremap = true, silent = true })

-- background color
vim.cmd("highlight Normal guibg=none")
vim.cmd("highlight NonText guibg=none")
vim.cmd("highlight VertSplit guibg=none")

vim.wo.number = true
vim.o.mouse = 'a'

-- 비주얼 모드에서는 상대 번호 끄기
vim.api.nvim_create_autocmd("ModeChanged", {
  pattern = "*:v",
  callback = function()
    vim.wo.number = false
  end,
})

-- 비주얼 모드에서 빠져나오면 다시 상대 번호 켜기
vim.api.nvim_create_autocmd("ModeChanged", {
  pattern = "v:*",
  callback = function()
    vim.wo.number = true
  end,
})
-- tap
vim.bo.expandtab = true
vim.bo.shiftwidth = 2
vim.bo.softtabstop = 2

-- Clipboard
vim.o.clipboard = 'unnamedplus'  -- 시스템 클립보드를 사용
vim.api.nvim_set_keymap('n', '<C-c>', '"+y', { noremap = true, silent = true })
vim.api.nvim_set_keymap('v', '<C-c>', '"+y', { noremap = true, silent = true })

vim.api.nvim_set_keymap('n', '<C-v>', '"+p', { noremap = true, silent = true })
vim.api.nvim_set_keymap('v', '<C-v>', '"+p', { noremap = true, silent = true })

-- search
vim.o.ignorecase = true
vim.o.smartcase = true

-- nvim-tree 설정

vim.cmd("packadd nvim-tree.lua")
require("nvim-tree").setup({
    view = {
        width = 30, -- 너비 설정
        side = "left", -- 왼쪽에 표시
    },
    renderer = {
        highlight_opened_files = "all", -- 열린 파일 하이라이트
    },
    update_focused_file = {
        enable = true, -- 현재 열려 있는 파일을 트리에서 강조
    },
})

-- nvim-tree 설정
vim.api.nvim_set_keymap('n', '<Space><Left>', ':NvimTreeFocus<CR>', { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<Space><Right>', ':wincmd l<CR>', { noremap = true, silent = true })
```