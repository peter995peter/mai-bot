# maimai-bot
一個使用py-cord的Discord maimai機器人

## 功能
### 歌曲相關
- `/song random` - 根據條件隨機抽取歌曲
- `/song list` - 根據條件以每頁 10 首歌列出歌曲
- `/song find` - 搜尋指定歌曲的詳細資訊
- `/song update` - 更新歌曲資料庫

#### 可選條件
可用於 `random` 與 `list` 指令：
  - 歌曲難度(1.0 ~ 15.0)
  - 指定版本(maimai ~ CiRCLE PLUS)
  - 指定類型(STD / DX)
  - 指定區域(日服 / 國際服 / 中國服)

### 帳號綁定
- `/link <好友代碼>` - 使用好友代碼綁定帳號
- `/unlink` - 解除綁定帳號

### 成績查詢
- `/score <歌曲名稱> [難度]` - 查詢自己指定歌曲的分數
- `/top rating <全球/機器人> [數量]` - 查詢全球或綁定者的rating排行
- `/top song <全球/機器人> <歌曲名稱> <難度> [數量]` - 查詢全球或綁定者的歌曲排行
- `/info [玩家]` - 查詢指定玩家綁定的個人資訊

## 需求

- Python 3.10 或以上
- Discord Bot Token
- 一個maimai DX NET的帳號

## 安裝方法
1. 下載專案

```bash
git clone https://github.com/peter995peter/mai-bot.git
cd mai-bot
```

2. 安裝依賴
```bash
pip install -r requirements.txt
```

3. 複製 `.env.example` 為 `.env`
```
DISCORD_TOKEN=你的Discord TOKEN
MaiNet_User=你的maimai DX NET帳號
MaiNet_Pass=你的maimai DX NET密碼
```

4. 啟動機器人

Windows
```bash
python bot.py
```
MacOS / Linux
```bash
python3 bot.py
```
