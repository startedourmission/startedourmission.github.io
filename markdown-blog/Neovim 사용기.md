---
date: 2025-04-18
tags:
  - 개발
aliases:
description: VSCode를 대체하기 위해 Neovim을 사용해 본 경험을 공유합니다. Lazyvim을 거쳐 직접 최소한의 설정을 구성한 과정과 `init.lua` 파일을 공개하고, 가벼움이라는 장점과 마우스 조작 등 단점을 비교하며 느낀 점을 솔직하게 담았습니다.
image: "![[]]"
---
나도 VSCode를 좋아했다. 디자인이 깔끔하고 확장 기능이 다양해서 VSCode 외의 개발 도구는 거의 사용하지 않았다. 어느 날인가부터 확장 기능이 잘 동작하지 않았다. 일시적인 문제겠거니 했지만, 며칠이 흘러도 해결되지 않았다. VSCode를 대체할만한 다른 편집기를 찾아보았다. 나는 발생한 문제를 적극적으로 해결하려는 의지가 없었다.  사실 이전부터 VSCode에 실증을 느끼고 있었다. 

Neovim는 호감형 편집기다. 불필요한 기능 없이 편집 기능에 충실하다. 가볍고 기민하다. 나와 같이 생각하는 사람이 많아서 생태계가 방대하다. 특히 VSCode처럼 확장 플러그인을 설치할 수 있었는데, 유명한 플러그인 관리 도구인 Lazyvim을 사용해보았다. 

Lazyvim을 사용하기 위해 겸사겸사 iTerm2와 Nerd Font도 처음 사용해봤다. iTerm2은 설정이 다양해서 마음에 들었지만, D2Coding Font는 마음에 들지 않았다. 결국 ASCII 외의 문자만 D2Coding으로 하고 영어는 Monaco를 유지했다.

Lazyvim은 기능이 많고 복잡하다. UI 설정 몇 개 수정하다 보니, 처음부터 나만의 Neovim을 설정하는 게 낫다는 결론을 내렸다. 자동완성 기능도 없는 최소한의 Neovim을 구성하고 싶었다. 

아래는 나의 init.lua 파일이다.

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

사실 불편한건 있다. 가장 큰 것은 마우스 조작이 불편하다는 점이다. 아무래도 그래픽 기반이 아니다보니 어색함이 느껴진다. 이 단점은 복사와 붙여넣기를 할 때 두드러진다. 가장 많이 해야하는 작업임에도 불구하고 시간을 잡아먹는 일이 생긴다. 확장 프로그램 역시 한계가 있다. 나는 Jupyter Notebook 환경을 자주 사용하는데, ipynb를 직접 다룰 수 있던 VSCode를 대체하기는 무리다. 

VSCode가 잘 만들어진 도구라는 것을 인정해야겠다. 노트북에 새로운 프로그램 설치하기를 싫어하는 나는 결국 iTerm2도 삭제했다. Neovim은 여전히 가끔 사용하지만, 결국 주력 개발 도구는 VSCode로 돌아왔다. 새로운 편집기를 개발하는 것도 재미있을듯 하다. Neovim에서 느꼈던 장점과 VSCode의 편의성을 합한 무언가를 만들 수 있을까.

